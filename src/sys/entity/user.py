#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2021-12-13 21:40

from flask_login import UserMixin


class User(UserMixin):
    id = None
    name = None
    username = None
    password = None
    status = None

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __str__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def status_normal():
        return "NORMAL"


if __name__ == '__main__':
    args = {
        "id": 2,
        "name": "name",
        "username": "username",
        "password": "password",
        "password1": "password",
    }
    user = User(**args)
    print(user)
    print(user.id, user.name, user.username, user.password, user.password1)
    user = User()
    print(user)
    print(user.id, user.name, user.username, user.password)
    pass
