"""
创建日期：2022.4.21
作者：乔毅
文件名：User_auth.py
功能：用户身份认证相关函数
备注：代码中被注释掉的print()为 测试时调用，控制台输出没有实际意义
"""

import pymysql
import asyncio

"""
2022.4.21 为鸿蒙开发新建函数
"""


# 用户注册函数
async def user_register(user_id: str, user_password: str) -> dict:
    """
    函数名：user_register
    作用：注册用户信息
    :param user_id:用户ID
    :param user_password:用户密码，经SHA256加密后的字符串
    :return:result_dict:执行状态
    """

    # 构建返回字典
    result_dict = {
        'state': False,
        'message': "default False"
    }

    # 打开数据库连接
    db = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="hm")
    # cursor创建游标对象,字典类型
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # 首先，检查用户名是否存在
    sql1 = """SELECT user_id FROM user_info WHERE user_id = %s"""
    is_exist = cursor.execute(sql1, user_id)
    # 结果条数不为0，即已存在该用户名
    if is_exist != 0:
        result_dict['state'] = False
        result_dict['message'] = "用户名已存在"
        cursor.close()
        db.close()
        return result_dict
    else:
        # 不存在记录，则插入用户记录
        sql2 = """INSERT INTO user_info (user_id, user_password) VALUES (%s, %s)"""
        cursor.execute(sql2, [user_id, user_password])
        db.commit()
        # 确认已存在该记录
        is_insert = cursor.execute(sql1, user_id)
        if is_insert != 1:
            result_dict['state'] = False
            result_dict['message'] = "注册用户时失败，请重试"
            db.rollback()
            cursor.close()
            db.close()
            return result_dict
        else:
            result_dict['state'] = True
            result_dict['message'] = "注册成功"
            cursor.close()
            db.close()
            return result_dict


# 用户登陆函数
async def user_login(user_id: str, user_password: str) -> dict:
    """
    函数名：user_login
    作用：用户登录函数
    :param user_id:用户ID
    :param user_password:用户密码，经SHA256加密后的字符串
    :return:result_dict:执行状态
    """

    # 构建返回字典
    result_dict = {
        'state': False,
        'message': "default False"
    }

    # 打开数据库连接
    db = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="hm")
    # cursor创建游标对象,字典类型
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # 避免数据库密码出现在内存中，所有比对在数据库进行
    # 首先，检验是否存在用户名是否存在
    sql1 = """SELECT user_id FROM user_info WHERE user_id = %s"""
    is_exist = cursor.execute(sql1, user_id)
    if is_exist != 1:
        # 不存在用户名
        result_dict['state'] = False
        result_dict['message'] = "用户名不存在"
        cursor.close()
        db.close()
        return result_dict
    else:
        # 若用户名存在，则匹配用户名和密码
        sql2 = """SELECT user_id FROM user_info WHERE user_id = %s AND user_password = %s"""
        is_correct = cursor.execute(sql2, [user_id, user_password])
        if is_correct == 1:
            # 匹配正确，即登录成功
            result_dict['state'] = True
            result_dict['message'] = "登录成功"
            cursor.close()
            db.close()
            return result_dict
        else:
            # 此时匹配失败，只有可能是密码错误
            result_dict['state'] = False
            result_dict['message'] = "密码错误"
            cursor.close()
            db.close()
            return result_dict

