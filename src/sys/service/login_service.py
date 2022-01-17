#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2021-12-12 11:29

from flask import request, render_template, redirect
from flask_login import login_user, logout_user, login_required, current_user

from src.sys.dao import user_dao
from src.sys.entity.user import User
from src.util.logger_util import logger


def home_page():
    return render_template("home.html")


def login_page():
    return render_template("login.html")


def login():
    logger.info('login param: %s', request.form)
    username = request.form['username']
    password = request.form['password']
    user: User = user_dao.get_by_username_password(
        username,
        password
    )
    logger.info('login user find: %s', user)
    if user:
        # 将用户id保存到session中，用于后面获取
        login_user(user)
        return redirect("user_home")
    return render_template('login.html', bad_message='用户名或密码或状态错误', username=username)


@login_required
def logout():
    logout_user()
    return redirect("/")


if __name__ == '__main__':
    pass
