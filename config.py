#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2021-12-12 22:28

# 应用名称
APP_NAME = 'ysy_tools'
# 数据库文件名称
DB_FILE_NAME = 'ysy_tools.sqlite3'
# 日志目录名称
LOGS_DIR_NAME = 'logs'
# 文件目录，用于用户上传及下载文件
FILE_DIR_PATH = "file"
# 根模块名，用于动态获取工具执行和源码下载
SRC_MODULE_NAME = "src"
# 工具模块名，用于动态获取工具执行和源码下载
TOOL_MODULE_NAME = "tool"
# 工具执行方法名称，用于动态获取工具执行
TOOL_EXECUTE_FUNCTION_NAME = "execute"
# 用于加解密session的秘钥
SECRET_KEY = "ysy_love_zlx"
# 限制请求报文最大长度为50MB
MAX_CONTENT_LENGTH = 50 * 1024 * 1024


if __name__ == '__main__':
    pass
