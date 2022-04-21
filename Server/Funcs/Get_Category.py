"""
创建日期：2022.4.8
作者：乔毅
文件名：Get_Category.py
功能：按类别返回对应分类的案例内容
备注：代码中被注释掉的print()为 测试时调用，控制台输出没有实际意义
"""

import json
import pymysql

"""
2022.4.21 为鸿蒙开发后端做调整。在已有功能的基础上做调整。
"""


# 获取制定案例函数
async def get_category(category: int) -> list:
    """
    函数名：get_category
    作用：返回输入类别的所有案例信息
    :param category: 类别编号
    :return: results 搜索结果
    """

    # 所有正确的类别序号
    all_kind = [1, 2, 3, 4, 5, 6, 7]
    # 判断输入类别是否正确
    if category not in all_kind:
        return [False]

    # 打开数据库连接
    db = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="hm")
    # cursor创建游标对象,字典类型
    cursor = db.cursor(pymysql.cursors.DictCursor)
    # 执行语句
    sql = """SELECT msg_id, msg_text, simi_times, kind_name FROM msg_info, kind_info WHERE msg_info.msg_kind = kind_info.kind_id AND kind_info.kind_id = %s"""
    cursor.execute(sql, category)
    # 处理结果
    res = cursor.fetchall()
    result = []
    for row in res:
        data = {
            'msg_id': row['msg_id'],
            'msg_text': row['msg_text'],
            'simi_times': row['simi_times'],
            'kind_name': row['kind_name'],
            'kind_id': category
        }
        result.append(data)
    return result
