"""
创建日期：2022.2.10
作者：乔毅
文件名：User_star.py
功能：添加用户收藏
备注：代码中被注释掉的print()为 测试时调用，控制台输出没有实际意义
"""

# 导入库
import pymysql
import sys
import asyncio
# import json

"""
2022.4.21 为鸿蒙开发后端做调整。在已有功能的基础上做调整。
"""


sys.path.append("..")


async def add_star(user_id: str, msg_id: int) -> bool:
    """
    函数名：add_star
    作用：根据用户微信ID和案例编号添加用户收藏
    :param user_id:用户ID
    :param msg_id:案例ID
    :return:state:成功状态
    """

    # 打开数据库连接
    db = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="hm")
    # cursor创建游标对象,字典类型
    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        # 插入收藏记录到数据库
        sql = """INSERT INTO user_star (ID, msg_id) VALUES (%s, %s)"""
        state = cursor.execute(sql, [user_id, msg_id])
        db.commit()
        cursor.close()
        db.close()
        return state == 1
    except Exception as e:
        db.rollback()
        db.close()
        print(e)
        return False


async def remove_star(user_id: str, msg_id: int) -> bool:
    """
    函数名：remove_star
    作用：根据用户ID和案例编号删除用户收藏
    :param user_id:用户ID
    :param msg_id:案例ID
    :return:state:成功状态
    """

    # 打开数据库连接
    db = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="hm")
    # cursor创建游标对象,字典类型
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # 检测是否存在该条记录
    sql1 = """SELECT * FROM user_star WHERE ID = %s AND msg_id = %s"""
    is_exist = cursor.execute(sql1, [user_id, msg_id])
    # 如果存在，则删除
    if is_exist == 1:
        try:
            sql2 = """DELETE FROM user_star WHERE ID = %s AND msg_id = %s"""
            cursor.execute(sql2, [user_id, msg_id])
            db.commit()
            cursor.close()
            db.close()
            return True
        except:
            db.rollback()
            cursor.close()
            db.close()
            return False
    else:
        cursor.close()
        db.close()
        return False


async def get_user_star_list(user_id: str) -> list:
    """
    函数名：get_user_star_list
    作用：通过用户微信ID获取其收藏列表
    :param user_id:用户ID
    :return: result_list：结果列表，每一项是一个字典
    """

    # 结果字典
    result_list = []

    # 打开数据库连接
    db = pymysql.connect(host="localhost", port=3306, user="root", password="root", database="hm")
    # 创建字典类型游标
    cursor = db.cursor(pymysql.cursors.DictCursor)

    # 查询用户数据
    sql = """SELECT msg_info.msg_id, msg_info.msg_text FROM user_star, msg_info WHERE user_star.ID = %s AND user_star.msg_id = msg_info.msg_id"""
    count = cursor.execute(sql, user_id)
    # 如果为空数据，即用户没有加过收藏，即返回空列表
    if count == 0:
        cursor.close()
        db.close()
        return result_list
    else:
        result = cursor.fetchall()
        for row in result:
            data = {
                'msg_id': row['msg_id'],
                'msg_text': row['msg_text']
            }
            result_list.append(data)
        cursor.close()
        db.close()
        return result_list


if __name__ == '__main__':
    User_id = 'QY_APP_TEST'
    Msg_id = 15
    res = asyncio.get_event_loop().run_until_complete(add_star(user_id=User_id, msg_id=Msg_id))
    # res = asyncio.get_event_loop().run_until_complete(remove_star(user_id=User_id, msg_id=Msg_id))
    # res = asyncio.get_event_loop().run_until_complete(get_user_star_list(user_id=User_id))
    print(res)

