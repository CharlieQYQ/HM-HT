"""
创建日期：2021.9.2
作者：乔毅
文件名：Message_search.py
功能：通过输入短信搜索余弦相似度高于阈值的短信内容及其附属内容，并存入历史记录
备注：代码中被注释掉的print()为 测试时调用，控制台输出没有实际意义
"""

# 导入库
import asyncio
import sys
import pymysql
import json
from Funcs.Func_tools import gen_stop_words, text_seg, CosineSimilarity
from Funcs.Word2Vec import vector_similarity
from operator import itemgetter
import gensim

"""
2022.4.21 为鸿蒙开发后端做调整。在已有功能的基础上做调整。
"""


sys.path.append("..")

# 生成停止词
stop_words = gen_stop_words()


# 搜索函数
async def msg_search(*, query: str, flag: float, model) -> list:
    """
    函数名：msg_search
    作用：通过输入的短信内容搜索与之相关的短信案例，并存入历史记录
    :param query: 搜索的短信字符串
    :param flag：搜索阈值
    :param model：加载的预训练模型
    :return: results 搜索结果
    """

    results = []
    if flag is None:
        # flag = 0.5
        flag = 0.5
    try:
        # 打开数据库连接
        db = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="hm")
        # cursor创建游标对象,字典类型
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # 2022.2.9
        # 存入查询记录
        # 2022.3.26 将记录保存改为详情页保存
        # cursor.execute("""Insert INTO query_record ( ID, Time, Query ) VALUES ( '%s', NOW(), '%s')""" % (wx_id, query))
        # db.commit()

        # 查询语句分词
        seg_query = text_seg(text=query, stop_words=stop_words)
        # print(seg_query)
        # 创建变量
        word_id_list, msg_id_list = [], []

        # 分词的词组转化为word_id，word_id加载到内存中，节省一次数据库查询
        cursor.execute("""SELECT * FROM word_freq""")
        word_cursor = cursor.fetchall()
        for row in word_cursor:
            if row['word'] in seg_query:
                word_id_list.append(row['word_id'])
        # print(word_id_list)
        # JSON编码
        word_id_list_json = json.dumps(word_id_list, ensure_ascii=False)

        # 根据word_id找出文档
        cursor.execute("""SELECT inverted_list FROM inverted_index WHERE JSON_CONTAINS("%s", JSON_ARRAY(word_id))""" % word_id_list_json)
        index_cursor = cursor.fetchall()
        for row in index_cursor:
            # print(row)
            cur_msg_id = 0
            # 将倒排序表加载入内存
            inverted_list = json.loads(row['inverted_list'])
            for num in range(0, len(inverted_list)):
                cur_msg_id += inverted_list[num][0]
                msg_id_list.append(cur_msg_id)
        # print(msg_id_list)
        msg_id_list_json = json.dumps(msg_id_list, ensure_ascii=False)

        # 根据文档id找出文档详细信息
        cursor.execute("""SELECT msg_info.msg_id, msg_info.msg_text, msg_seg.seg_msg, msg_info.simi_times FROM msg_seg, msg_info WHERE msg_info.msg_id = msg_seg.msg_id AND JSON_CONTAINS("%s", JSON_ARRAY(msg_info.msg_id))""" % msg_id_list_json)
        msg_cursor = cursor.fetchall()
        # print(msg_cursor)
        """
        2022.3.27 修改为Word2Vec方法
        # 对输出结果进行余弦相似度计算
        for row in msg_cursor:
            msg_data = {
                'index': row['msg_text'],
                'value': json.loads(row['seg_msg'])
            }
            # 实例化余弦相似度类
            cos = CosineSimilarity(seg_query, msg_data)
            # 计算词频向量
            vector = cos.create_vector()
            # 计算余弦相似度
            cs_res = cos.calculate_cos(word_vector=vector)
            # print(cs_res)
            if cs_res['value'] >= flag:
                # 加入字典
                row['cs_value'] = cs_res['value']
                row.pop('seg_msg')
                row['simi_times'] += 1
                # print(row)
                # 加入列表
                results.append(row)
        """
        for row in msg_cursor:
            # 计算相似度
            sim = vector_similarity(s1=row['msg_text'], s2=query, model=model)
            msg_data = {
                'msg_id': row['msg_id'],
                'index': row['msg_text'],
                'similarity': "%.2f%%" % (sim*100),
                'simi_times': row['simi_times']
            }
            if sim >= flag:
                results.append(msg_data)

        # 根据阈值使相似次数自增
        for row in results:
            # print(row)
            msg_id = row['msg_id']
            simi_times = row['simi_times'] + 1
            cursor.execute("""UPDATE msg_info SET simi_times='%d' WHERE msg_id='%d'""" % (simi_times, msg_id))
            db.commit()

        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        db.close()

    except Exception as e:
        print("ERROR as ->  ", e)

    # 依据余弦相似度的值进行排序
    results_sorted = sorted(
        results,
        reverse=True,
        key=itemgetter('similarity')
    )

    return results_sorted


if __name__ == '__main__':
    model_file = '../word2vec/news_12g_baidubaike_20g_novel_90g_embedding_64.bin'
    model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=True)
    print("Model Load")
    search_word = "我单位高薪招聘公关先生，请到指定酒店面试，速回电话。"
    res = asyncio.get_event_loop().run_until_complete(msg_search(query=search_word, flag=0.5, model=model))
    print("搜索词为： %s" % search_word)
    for i in range(0, len(res)):
        print(res[i])
