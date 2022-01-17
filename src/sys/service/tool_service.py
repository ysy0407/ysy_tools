#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2021-12-14 20:06


import os
import shutil
from flask import request, render_template, send_file
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from src.sys.dao import tool_dao
from src.sys.entity.tool import Tool
from src.sys.entity.user import User
from src.util.path_util import base_path_join
from src.util.logger_util import logger
from src.util.reflect_util import get_function_by_path
from config import TOOL_EXECUTE_FUNCTION_NAME, FILE_DIR_PATH


@login_required
def all_tools():
    return render_template("all_tools.html", user=current_user, tools=tool_dao.get_all_tools())


@login_required
def use_tool():
    user: User = current_user
    tool: Tool = tool_dao.get_by_id(int(request.args.get("tool_id")), user.id)
    if tool:
        return render_template("use_tool.html", user=user, tool=tool,
                               execute_params=tool_dao.get_tool_execute_params(tool.id))
    else:
        tools = tool_dao.get_user_usable_tools(user)
        return render_template('user_home.html', user=user, tools=tools, bad_message="您没有权限使用该工具，或该工具不存在")


@login_required
def execute_tool():
    user: User = current_user
    tool: Tool = tool_dao.get_by_id(int(request.args.get("tool_id")), user.id)
    if not tool:
        tools = tool_dao.get_user_usable_tools(user)
        return render_template('user_home.html', user=user, tools=tools, bad_message="您没有权限使用该工具，或该工具不存在")
    # 动态获取执行方法
    tool_execute_function = get_function_by_path(
        tool.get_tool_module_path(),
        TOOL_EXECUTE_FUNCTION_NAME
    )
    # 获取方法执行参数
    tool_execute_params = tool_dao.get_tool_execute_params(tool.id)
    if not tool_execute_function:
        return render_template("use_tool.html", user=user, tool=tool, execute_params=tool_execute_params,
                               bad_message="工具（%s）配置不正确，请联系管理员处理" % tool.tool_file_name)
    # 若用户的文件目录存在则删除，之后再创建，避免存储文件过多
    user_file_path = base_path_join(FILE_DIR_PATH, user.username)
    if os.path.exists(user_file_path):
        logger.info("user file path exists, remove the path: %s", user_file_path)
        shutil.rmtree(user_file_path)
    os.mkdir(user_file_path)
    # 获取方法执行参数
    function_params = dict()
    try:
        for tool_execute_param in tool_execute_params:
            if tool_execute_param.type_is_file():
                file = request.files[tool_execute_param.key]
                if tool_execute_param.required and not file:
                    raise ValueError("%s 为必填项" % tool_execute_param.name)
                filename = secure_filename(file.filename)
                if not tool_execute_param.check_file_type(filename):
                    raise ValueError("%s 文件格式应为：%s" % (tool_execute_param.name, tool_execute_param.file_types))
                file_save_path = base_path_join(FILE_DIR_PATH, user.username, filename)
                logger.info("save file: %s", file_save_path)
                file.save(file_save_path)
                function_params[tool_execute_param.key] = file_save_path
            else:
                function_params[tool_execute_param.key] = request.form[tool_execute_param.key]
                if tool_execute_param.required and not function_params[tool_execute_param.key]:
                    raise ValueError("%s 为必填项" % tool_execute_param.name)
    except ValueError as value_error:
        logger.error("get execute params appear value error: %s", value_error)
        return render_template("use_tool.html", user=user, tool=tool, execute_params=tool_execute_params, bad_message=value_error)
    except Exception as e:
        logger.exception("get execute params appear exception: %s", e)
        return render_template("use_tool.html", user=user, tool=tool, execute_params=tool_execute_params, bad_message=e)
    # 获取工具执行完成返回的结果文件路径
    try:
        function_result_file_path = tool_execute_function(function_params)
        logger.info("return result file path: %s", function_result_file_path)
        tool_dao.add_tool_use_times(tool.id, user.id)
        return send_file(function_result_file_path, as_attachment=True)
    except Exception as e:
        logger.exception("execute function appear exception: %s", e)
        return render_template("use_tool.html", user=user, tool=tool, execute_params=tool_execute_params, bad_message=e)
    pass


@login_required
def get_source_code():
    user: User = current_user
    tool: Tool = tool_dao.get_by_id(int(request.args.get("tool_id")), user.id)
    if not tool:
        tools = tool_dao.get_user_usable_tools(user)
        return render_template('user_home.html', user=user, tools=tools, bad_message="您没有权限使用该工具，或该工具不存在")
    logger.info("return source code: %s", tool.tool_file_name)
    return send_file(tool.get_tool_source_code_path(), as_attachment=int(request.args.get("show_on_browser")) != 1)


if __name__ == '__main__':
    pass
