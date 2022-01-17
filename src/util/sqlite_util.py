#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2021-12-12 17:34


import sqlite3
from src.util.path_util import base_path_join
from config import DB_FILE_NAME

db_file_path = base_path_join(DB_FILE_NAME)


# 用此方法代替原row_factory，可通过列名获取值
def __dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def __get_conn():
    conn = sqlite3.connect(db_file_path)
    conn.row_factory = __dict_factory
    return conn


def execute(sql: str, param: list):
    print(sql, param)
    conn = __get_conn()
    conn.execute(sql, param)
    conn.commit()


def fetch_one(sql: str, param: list) -> dict:
    return __get_conn().execute(sql, param).fetchone()


def fetch_all(sql: str, param: list) -> list:
    return __get_conn().execute(sql, param).fetchall()


def fetch_many(sql: str, param: list, size: int) -> list:
    return __get_conn().execute(sql, param).fetchmany(size)


if __name__ == '__main__':
    print(fetch_all("select id, name, username from sys_user where username=?", ["ysy"]))
    print(fetch_one("select id, name, username from sys_user where username=? and password=?", ["ysy", "ysy"])['id'])
    print(fetch_many("select id, name, username from sys_user where username=?", ["ysy"], 2))
    pass
