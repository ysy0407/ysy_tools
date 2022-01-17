#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2021-12-12 22:11

"""日志类"""

import logging
from logging import handlers
from src.util import path_util
from config import LOGS_DIR_NAME, APP_NAME


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    @staticmethod
    def init(file_name, level='info', when='D', backup_count=30,
             fmt='%(asctime)s-%(threadName)s-%(filename)s[%(lineno)d]-%(levelname)s: %(message)s'):
        if not hasattr(Logger, 'logger'):
            logger = logging.getLogger(file_name)
            format_str = logging.Formatter(fmt)  # 设置日志格式
            logger.setLevel(Logger.level_relations.get(level))  # 设置日志级别
            sh = logging.StreamHandler()  # 往屏幕上输出
            sh.setFormatter(format_str)  # 设置屏幕上显示的格式
            # 往文件里写入#指定间隔时间自动生成文件的处理器
            th = handlers.TimedRotatingFileHandler(filename=file_name, when=when, backupCount=backup_count,
                                                   encoding='utf-8')
            # 实例化TimedRotatingFileHandler
            # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
            # S 秒 M 分 H 小时 D 天 W 每星期（interval==0时代表星期一） midnight 每天凌晨
            th.setFormatter(format_str)  # 设置文件里写入的格式
            logger.addHandler(sh)  # 把对象加到logger里
            logger.addHandler(th)
            return logger


# 初始化Logger类的logger
logger = Logger.init(file_name=path_util.base_path_join(LOGS_DIR_NAME, APP_NAME + ".log"))

if __name__ == '__main__':
    logger.info('用户名：{0} 密码：{1}'.format('self.username', 'self.password'))

