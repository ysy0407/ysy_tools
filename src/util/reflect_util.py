#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2021-12-14 22:04

import importlib
from inspect import isfunction
from src.util.logger_util import logger


def get_function_by_path(module_path: str, function_name: str):
    """
        根据模块路径和方法名获取对应方法
    :param module_path: 模块路径，如：src.util.reflect_util
    :param function_name: 方法名称，如：get_function_by_path
    :return:
    """
    try:
        module = importlib.import_module(module_path)
        if hasattr(module, function_name):
            function = getattr(module, function_name)
            if isfunction(function):
                return function
            else:
                logger.error("the function_name: %s not a function in module_path: %s", function_name, module_path)
                return None
        else:
            logger.error("not find by python_file_path：%s, function_name: %s", module_path, function_name)
            return None
    except ModuleNotFoundError:
        logger.error("not find module by module_path: %s", module_path)
        return None


if __name__ == '__main__':
    function_result = get_function_by_path("src.tool.replace_sequences", "test")
    print(type(function_result))
    function_result()
