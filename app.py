#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2021-12-12 11:20

from flask import Flask
# pip install flask-login
from flask_login import LoginManager

from config import SECRET_KEY, MAX_CONTENT_LENGTH
from src.sys.service.login_service import *
from src.sys.service.tool_service import *
from src.sys.service.user_service import *

app = Flask(__name__, static_url_path="")
# 修改配置项
app.config["SECRET_KEY"] = SECRET_KEY
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
# 初始化系统路由
app.add_url_rule("/", view_func=home_page, methods=['GET'])
app.add_url_rule("/login", view_func=login_page, methods=['GET'])
app.add_url_rule("/login", view_func=login, methods=['POST'])
app.add_url_rule("/logout", view_func=logout, methods=['GET'])
app.add_url_rule("/user_home", view_func=user_home, methods=['GET'])
app.add_url_rule("/all_tools", view_func=all_tools, methods=['GET'])
app.add_url_rule("/use_tool", view_func=use_tool, methods=['GET'])
app.add_url_rule("/execute_tool", view_func=execute_tool, methods=['POST'])
app.add_url_rule("/get_source_code", view_func=get_source_code, methods=['GET'])
# 初始化登录管理
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(load_user)
login_manager.login_message = "你还没有登录"
login_manager.needs_refresh_message = "请刷新"
login_manager.refresh_view = "/"
login_manager.login_view = "/"


@app.route('/hello')
def hello():
    return "hello world!"


if __name__ == '__main__':
    app.run(port=8080)
