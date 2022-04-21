"""
创建日期：2021.9.2
作者：乔毅
文件名：Message_tools.py
功能：对短信数据进行处理
备注：代码中被注释掉的print()为 测试时调用，控制台输出没有实际意义
"""

# 导入库
import asyncio
import pymysql
import json
from collections import Counter
from Funcs.Func_tools import gen_stop_words, text_seg
import time

"""
2022.4.21 为鸿蒙开发后端做调整。在已有功能的基础上做调整。
"""


# 生成分词和单词编号、短信编号
async def gen_msg_word_id():
    """
    函数名；gen_doc_word_id
    作用：生成分词列表和单词编号、短信编号
    :return:
    """

    # 获取数据库所有元组
    sql = """SELECT msg_id, msg_text FROM msg_info"""
    # 执行查询
    cursor.execute(sql)
    results = cursor.fetchall()
    # 创建变量
    word_list = []
    msg_id, word_id = 0, 0

    # 分词
    for row in results:
        # print(str(row))
        # 对短信进行分词
        seg_msg = text_seg(row['msg_text'], stop_words=stop_words)
        msg_id = row['msg_id']
        # 结果字典
        cur_item_data_1 = {
            'msg_id': msg_id,
            'seg_msg': json.dumps(seg_msg, ensure_ascii=False),
            'seg_msg_counter': json.dumps(Counter(seg_msg), ensure_ascii=False),
            'msg_text': row['msg_text']
        }
        # print(str(cur_item_data_1))
        # 提交结果至数据库
        cursor.execute("""REPLACE INTO msg_seg (msg_id, seg_msg, seg_msg_counter, msg_text) VALUES ('%d', '%s', '%s', '%s')""" % (cur_item_data_1['msg_id'], cur_item_data_1['seg_msg'], cur_item_data_1['seg_msg_counter'], cur_item_data_1['msg_text']))
        db.commit()
        # 更新单词表
        word_list += seg_msg

    # 更新词频
    for key, value in Counter(word_list).items():
        word_id += 1
        cur_item_data_2 = {
            'word_id': word_id,
            'word': key,
            'word_freq': value
        }
        # print(str(cur_item_data_2))
        cursor.execute("""REPLACE INTO word_freq (word_id, word, word_freq) VALUES ('%d', '%s', '%d')""" % (cur_item_data_2['word_id'], cur_item_data_2['word'], cur_item_data_2['word_freq']))
        db.commit()


# 生成倒排索引
async def gen_msg_inverted_index():
    """
    函数名：gen_msg_inverted_index
    作用：生成短信阵列的倒排索引
    要先运行程序生成对应word_id，即要先运行gen_msg_word_id()函数
    :return:
    """
    # 获取word_freq表中的数据
    cursor.execute("""SELECT * FROM word_freq""")
    word_cursor = cursor.fetchall()
    for row in word_cursor:
        # print(row)
        word_id = row['word_id']
        word = row['word']
        word_freq = row['word_freq']
        # 按照word查询符合的seg_msg元组，JSON_CONTAINS()检测JSON中含有的元素
        cursor.execute("""SELECT * FROM msg_seg WHERE JSON_CONTAINS(seg_msg, CONCAT('"', "%s", '"'))""" % word)
        msg_cursor = cursor.fetchall()
        # 创建变量
        cur_word_data, inverted_list = {}, []
        # 记录当前msg_id
        last_msg_id = 0
        for x in msg_cursor:
            # print(x)
            msg_id = x['msg_id']
            # 取msg_id的差值
            cur_msg_id = msg_id - last_msg_id
            # 更新last_msg_id
            last_msg_id = msg_id
            seg_msg_counter = json.loads(x['seg_msg_counter'])
            # print(seg_msg_counter)
            # 加入倒序索引列表
            inverted_list.append((cur_msg_id, seg_msg_counter[word]))
        cur_word_data = {
            'word_id': word_id,
            'word_freq': word_freq,
            'inverted_list': json.dumps(inverted_list, ensure_ascii=False)
        }
        # 存入数据库
        cursor.execute("""REPLACE INTO inverted_index (word_id, word_freq, inverted_list) VALUE ('%d', '%d', '%s')""" % (cur_word_data['word_id'], cur_word_data['word_freq'], cur_word_data['inverted_list']))
        db.commit()
    print("创建索引成功")


if __name__ == '__main__':
    start_time = time.time()
    # 打开数据库连接
    db = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="hm")
    # 创建停用词表
    stop_words = gen_stop_words()
    # cursor创建游标对象
    db.ping(reconnect=True)
    cursor = db.cursor(pymysql.cursors.DictCursor)
    asyncio.get_event_loop().run_until_complete(gen_msg_word_id())
    asyncio.get_event_loop().run_until_complete(gen_msg_inverted_index())
    # el_str = elias_gamma_encode(500)
    # print(elias_gamma_decode(el_str))
    # 关闭连接
    # 关闭游标
    cursor.close()
    db.close()
    end_time = time.time()
    print("Used Time: ", end_time - start_time, " s")
