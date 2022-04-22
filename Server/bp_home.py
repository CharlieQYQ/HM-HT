"""
创建日期：2021.9.3
作者：乔毅
文件名：bp_home.py
功能：sanic后端服务蓝图
"""

# 导入库
import sys
from sanic import Blueprint
from sanic.response import json, text
import logging
import datetime
# import asyncio
import gensim

# 导入自建函数
from Funcs.Message_search import msg_search
from Funcs.Message_info import msg_info_search
from Funcs.Query_record import query_record
from Funcs.User_star import add_star, get_user_star_list, remove_star
from Funcs.Get_Category import get_category
from Funcs.User_auth import user_login, user_register

"""
2022.4.21 为鸿蒙开发后端做调整。在已有功能的基础上做调整。
"""


# 配置日志
# 获取当前时间以命名日志文件
time_str = datetime.datetime.now().strftime('%Y-%m-%d')
# 创建日志
logger = logging.getLogger(__name__)
# 设置日志等级
logger.setLevel(level=logging.INFO)
# 设置解决器
# handler = logging.FileHandler("/root/HM-HT/Logs/%s.log" % time_str)
handler = logging.FileHandler("../Logs/%s.log" % time_str)
handler.setLevel(logging.INFO)
# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 新建蓝图
bp_home = Blueprint('bp_home')
# 开启异步特性
enable_async = sys.version_info >= (3, 6)

# 2022.3.27
# 加载模型
# model_file = '/root/HM-HT/Server/word2vec/news_12g_baidubaike_20g_novel_90g_embedding_64.bin'
model_file = './word2vec/news_12g_baidubaike_20g_novel_90g_embedding_64.bin'
model = gensim.models.KeyedVectors.load_word2vec_format(model_file, binary=True)
print("Model Load")
logger.info("Model Loaded")


# 设置路由
@bp_home.route('/')
async def index(request):
    return text('index page')


# 信息检索
@bp_home.route('/msg_search')
async def message_search(request):
    logger.info(request)
    try:
        query = str(request.args.get('msg', '')).strip()
        result = await msg_search(query=query, flag=0.3, model=model)
        logger.info(result)
        return json(result, ensure_ascii=False)
    except Exception as e:
        logger.error(e)
        return text(str(e))


# 案例信息查询
@bp_home.route('/msg_info')
async def message_info(request):
    logger.info(request)
    try:
        msg_id = int(request.args.get('msg_id', ''))
        user_id = str(request.args.get('user_id', '')).strip()
        result = await msg_info_search(msg_id=msg_id, user_id=user_id)
        logger.info(result)
        return json(result, ensure_ascii=False)
    except Exception as e:
        logger.error(e)
        return text(str(e))


# 查询历史记录
@bp_home.route('/query_record')
async def history_query(request):
    logger.info(request)
    try:
        user_id = str(request.args.get('user_id', '')).strip()
        result = await query_record(user_id=user_id)
        logger.info(result)
        return json(result, ensure_ascii=False)
    except Exception as e:
        logger.error(e)
        return text(str(e))


# 添加用户收藏
@bp_home.route('/add_star')
async def user_add_star(request):
    logger.info(request)
    try:
        user_id = str(request.args.get('user_id', '')).strip()
        msg_id = int(request.args.get('msg_id', ''))
        result = await add_star(user_id=user_id, msg_id=msg_id)
        logger.info(result)
        return json(result)
    except Exception as e:
        logger.error(e)
        return text(str(e))


# 删除用户收藏
@bp_home.route('/remove_star')
async def user_remove_star(request):
    logger.info(request)
    try:
        user_id = str(request.args.get('user_id', '')).strip()
        msg_id = int(request.args.get('msg_id', ''))
        result = await remove_star(user_id=user_id, msg_id=msg_id)
        logger.info(result)
        return json(result)
    except Exception as e:
        logger.error(e)
        return text(str(e))


# 获取用户收藏列表
@bp_home.route('/get_star')
async def get_star(request):
    logger.info(request)
    try:
        user_id = str(request.args.get('user_id', '')).strip()
        result = await get_user_star_list(user_id=user_id)
        logger.info(result)
        return json(result, ensure_ascii=False)
    except Exception as e:
        logger.error(e)
        return text(str(e))


# 获取分类数据
@bp_home.route('/get_category')
async def get_kind(request):
    logger.info(request)
    try:
        kind = int(request.args.get('kind', ''))
        result = await get_category(category=kind)
        logger.info(result)
        return json(result, ensure_ascii=False)
    except Exception as e:
        logger.error(e)
        return False


# 用户注册
@bp_home.route('/user_register')
async def register(request):
    logger.info(request)
    try:
        user_id = str(request.args.get('user_id', '')).strip()
        user_password = str(request.args.get('password', '')).strip()
        result = await user_register(user_id=user_id, user_password=user_password)
        logger.info(result)
        return json(result, ensure_ascii=False)
    except Exception as e:
        logger.error(e)
        return json({'state': False, 'message': "服务错误"}, ensure_ascii=False)


# 用户登录
@bp_home.route('/user_login')
async def login(request):
    logger.info(request)
    try:
        user_id = str(request.args.get('user_id', '')).strip()
        user_password = str(request.args.get('password', '')).strip()
        result = await user_login(user_id=user_id, user_password=user_password)
        logger.info(result)
        return json(result, ensure_ascii=False)
    except Exception as e:
        logger.error(e)
        return json({'state': False, 'message': "服务错误"}, ensure_ascii=False)
