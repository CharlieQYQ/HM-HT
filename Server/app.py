"""
创建日期：2021.9.3
作者：乔毅
文件名：app.py
功能：sanic服务
"""

# 导入库
# import sanic.log
from sanic import Sanic
from sanic.response import text
from sanic.exceptions import NotFound, ServerError
from bp_home import bp_home
# from sanic.log import *
# import logging

"""
2022.4.21 为鸿蒙开发后端做调整。在已有功能的基础上做调整。
"""


"""
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("../Logs/test2.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
"""

app = Sanic(__name__)
app.blueprint(bp_home)


@app.listener('before_server_start')
async def init_cache(app, loop):
    print("Starting Server")


@app.listener('after_server_start')
async def start_log(app, loop):
    print("Server Started")


@app.listener('before_server_stop')
async def stop_log(app, loop):
    print("Stopping Server")


@app.listener('after_server_stop')
async def finish_log(app, loop):
    print("Server stopped")


@app.exception(NotFound)
async def not_found(request, exception):
    # logger.info("404 Not Found")
    return text("Room 404 Not Found")


@app.exception(ServerError)
async def server_error(request, exception):
    return text("Server Error")


if __name__ == '__main__':
    app.run(host='0.0.0.0', workers=4, port=8001, debug=False, access_log=True)
