#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2021-12-13 21:54


from src.util.sqlite_util import fetch_all, fetch_one, execute
from src.sys.entity.user import User
from src.sys.entity.tool import Tool, ToolExecuteParam


def get_user_usable_tools(user: User) -> list:
    """
        获取当前用户可用的工具
    :rtype: Tool
    :param user: 当前用户
    :return:
    """
    # 将查询到的结果循环生成Tools对象并放入list中进行返回
    return list(map(lambda result: Tool(**result), fetch_all(
        "select tool.id, tool.name, tool.desc, tool.tool_file_name, "
        "usable_tools.times as user_use_times, usable_tools.last_time as user_last_use_time "
        "from sys_tool tool "
        "join sys_user_usable_tools usable_tools on tool.id = usable_tools.tool_id and usable_tools.user_id = ?",
        [user.id])))


def get_all_tools() -> list:
    """
        获取全部工具
    :rtype: Tool
    :return: 
    """
    # 将查询到的结果循环生成Tools对象并放入list中进行返回
    return list(map(lambda result: Tool(**result), fetch_all(
        "select id, name, desc, tool_file_name, use_total_times from sys_tool ",
        []
    )))


def get_by_id(tools_id: int, user_id: int) -> Tool:
    tool: dict = fetch_one(
        "select id, name, desc, tool_file_name "
        "from sys_tool "
        "where id=("
        "select tool_id from sys_user_usable_tools where tool_id=? and user_id = ?"
        ")",
        [tools_id, user_id]
    )
    if tool:
        return Tool(**tool)
    else:
        return None


def get_tool_execute_params(tools_id: int) -> list:
    """
        根据工具ID获取其所有执行参数
    :param tools_id:
    :return:
    """
    # 将查询到的结果循环生成ToolExecuteParam对象并放入list中进行返回
    return list(map(lambda result: ToolExecuteParam(**result), fetch_all(
        "select id, tool_id, key, name, type, file_types, desc, required "
        "from sys_tool_execute_param "
        "where tool_id = ?",
        [tools_id]
    )))


def add_tool_use_times(tools_id: int, user_id: int):
    """
        增加工具的用户使用次数和总使用次数
    :param tools_id:
    :param user_id:
    """
    execute("update sys_tool "
            "set use_total_times = use_total_times + 1 "
            "where id = ?",
            [tools_id])
    execute("update sys_user_usable_tools set times = times + 1, "
            "last_time = datetime(strftime('%s','now'), 'unixepoch', 'localtime') "
            "where tool_id = ? and user_id = ?",
            [tools_id, user_id])


if __name__ == '__main__':
    add_tool_use_times(1, 1)
    args = {
        "id": 1,
        "name": "name",
        "username": "username",
        "password": "password",
        "password1": "password",
    }
    print(get_user_usable_tools(User(**args)))
    for tool in get_user_usable_tools(User(**args)):
        print(tool)
    # print(get_user_usable_tools(User(**args))[0])
    # print(get_by_id(1, 1))
    pass
