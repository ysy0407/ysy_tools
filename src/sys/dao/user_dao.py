#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2021-12-13 21:19

from src.util.sqlite_util import fetch_one
from src.sys.entity.user import User


def get_by_username_password(username, password):
    user = fetch_one("select id, name, username, status from sys_user where status=? and username=? and password=?",
                     [User.status_normal(), username, password])
    if user:
        return User(**user)
    else:
        return None


def get_by_id(id: int):
    user: dict = fetch_one("select id, name, username, status from sys_user where id=? ", [id])
    if user:
        return User(**user)
    else:
        return None


if __name__ == '__main__':
    print(get_by_username_password("ysy", "ysy"))
    pass
