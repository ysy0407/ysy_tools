#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2021-12-13 21:52


from config import TOOL_MODULE_NAME, SRC_MODULE_NAME
from src.util.path_util import base_path_join


class Tool(object):
    id = None
    name = None
    desc = None
    tool_file_name = None
    use_total_times = None
    user_use_times = None
    user_last_use_time = None

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __str__(self) -> str:
        return str(self.__dict__)

    def get_tool_source_code_path(self):
        return base_path_join(SRC_MODULE_NAME, TOOL_MODULE_NAME, self.tool_file_name)

    def get_tool_module_path(self):
        return SRC_MODULE_NAME + "." + TOOL_MODULE_NAME + "." + self.tool_file_name.replace(".py", "")


class ToolExecuteParam(object):
    id = None
    tool_id = None
    key = None
    name = None
    type = None
    file_types = None
    desc = None
    required = None

    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __str__(self) -> str:
        return str(self.__dict__)

    @staticmethod
    def __file_types_split__():
        """
            返回问价类型分隔符
        :return: ","
        """
        return ","

    def type_is_file(self):
        """
            返回表示type是文件字符串
        :return: "file"
        """
        return self.type == "file"

    def check_file_type(self, filename):
        """
            检查文件名称是否符合要求
        :param filename:
        :return:
        """
        file_type_check_result = False
        for file_type in self.file_types.split(ToolExecuteParam.__file_types_split__()):
            file_type_check_result = filename.endswith(file_type)
            # 任意一种文件格式匹配则跳出
            if file_type_check_result:
                break
        return file_type_check_result


if __name__ == '__main__':
    pass
