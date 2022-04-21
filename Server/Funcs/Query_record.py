"""
创建日期：2022.2.9
作者：乔毅
文件名：Query_record.py
功能：通过微信ID获取该用户的搜索历史
备注：代码中被注释掉的print()为 测试时调用，控制台输出没有实际意义
"""

# 导入库
import pymysql
import asyncio
import sys
import time
import datetime

"""
2022.4.21 为鸿蒙开发后端做调整。在已有功能的基础上做调整。
"""


sys.path.append("..")


async def query_record(user_id: str) -> list:
    """
    函数名：Query_record
    作用：根据微信ID获取用户所有搜索记录并返回
    :param user_id:用户ID
    :return:result_list:记录列表
    """

    # 结果列表
    result_list = []
    try:
        # 打开数据库连接
        db = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="hm")
        # cursor创建游标对象,字典类型
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # 依据微信ID查询数据库
        # 2022.3.16 如果直接把sql合并到execute里面，会报错
        sql = """SELECT query_record.Msg_id, Time, msg_info.msg_text FROM query_record, msg_info WHERE ID = %s AND query_record.Msg_id = msg_info.msg_id"""
        cursor.execute(sql, user_id)
        record_cursor = cursor.fetchall()

        # 整理结果
        for row in record_cursor:
            # print(row)
            record_data = {
                'msg_id': row['Msg_id'],
                'time': row['Time'].strftime('%Y-%m-%d %H:%M:%S'),
                'msg_text': row['msg_text']
            }
            result_list.append(record_data)

        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        db.close()

        sorted_result_list = sorted(
            result_list,
            key=lambda k: datetime.datetime.strptime(k.get('time'), '%Y-%m-%d %H:%M:%S'),
            reverse=True
        )
        return sorted_result_list
    except Exception as e:
        print("ERROR as -> ", e)


if __name__ == '__main__':
    User_id = "ovQCm4jh-FgYKARxJZ6_imgaYEOE"
    res = asyncio.get_event_loop().run_until_complete(query_record(user_id=User_id))
    for i in range(0, len(res)):
        print(res[i])


