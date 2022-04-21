"""
创建日期：2021.9.3
作者：乔毅
文件名：Message_info.py
功能：通过短信编号查询短信的相关信息
备注：代码中被注释掉的print()为 测试时调用，控制台输出没有实际意义
"""

# 导入库
# import json
import asyncio
import pymysql

"""
2022.4.21 为鸿蒙开发后端做调整。在已有功能的基础上做调整。
"""


# 查询函数
async def msg_info_search(msg_id: int, user_id: str) -> dict:
    """
    函数名：msg_info_search
    作用：通过输入的短信编号查询短信相关信息
    :param msg_id: 短信编号
    :param user_id：用户id
    :return: result_dict：结果字典
    """

    result_dict = {}
    try:
        # 打开数据库连接
        db = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="hm")
        # 创建字典类型游标
        cursor = db.cursor(pymysql.cursors.DictCursor)
        # 查询元组
        cursor.execute("""SELECT msg_analysis, msg_text, simi_times, kind_name, law_text, solution_text FROM msg_info, law_info, kind_info, msg_solutions WHERE FIND_IN_SET(msg_solutions.solution_id,kind_info.solutions) AND msg_id='%s' AND msg_kind=kind_id AND FIND_IN_SET(law_info.law_id,kind_info.law_id)""" % msg_id)
        result_list = cursor.fetchall()
        # print(result_list)
        # 整合法条和解决方法
        law_list, solution_list = [], []
        for row in result_list:
            law_list.append(row['law_text'])
            solution_list.append(row['solution_text'])

        # 2022.4.19 返回数据加入收藏情况
        sql2 = """SELECT * FROM user_star WHERE ID = %s AND msg_id = %s """
        # 通过返回结果个数判断是否存在此条收藏记录
        is_star = cursor.execute(sql2, [user_id, msg_id])
        star = False
        # 0条结果为没有收藏，1条结果为已收藏，其他情况不可能出现
        if is_star == 0:
            star = False
        elif is_star == 1:
            star = True

        # 整理字典
        result_dict = {
            'msg_text': result_list[0]['msg_text'],
            'msg_analysis': result_list[0]['msg_analysis'],
            'simi_times': result_list[0]['simi_times'],
            'kind_name': result_list[0]['kind_name'],
            'laws': list(set(law_list)),
            'solutions': list(set(solution_list)),
            'is_star': star
        }

        # 2022.3.26 存入浏览记录
        sql = """INSERT INTO query_record ( ID, Time, Msg_id ) VALUES ( %s, NOW(), %s)"""
        cursor.execute(sql, [user_id, int(msg_id)])
        db.commit()
    except Exception as e:
        print(e)

    return result_dict


if __name__ == '__main__':
    User_id = "QY_APP_TEST"
    result = asyncio.get_event_loop().run_until_complete(msg_info_search(msg_id=15, user_id=User_id))
    print(result)
