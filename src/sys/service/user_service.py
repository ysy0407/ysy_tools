#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2021-12-14 20:17


from flask import session, render_template
from flask_login import login_required, current_user

from src.sys.dao import tool_dao, user_dao


@login_required
def user_home():
    tools = tool_dao.get_user_usable_tools(current_user)
    return render_template('user_home.html', user=current_user, tools=tools)


def load_user(user_id):
    user = user_dao.get_by_id(user_id)
    return user if user else None


if __name__ == '__main__':
    pass
