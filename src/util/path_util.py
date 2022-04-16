#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2021-12-12 22:11

"""路径工具类"""

import os
from typing import Union, AnyStr

from config import APP_NAME

__NOW_DIR = os.path.dirname(os.path.abspath(__file__))
"""项目根目录"""
BASE_PATH: Union[str] = __NOW_DIR[0:__NOW_DIR.find(APP_NAME) + len(APP_NAME)]

# 图片后缀
IMAGE_SUFFIX = ['jpg', 'png', 'jpeg', 'bmp']

def base_path_join(*paths: AnyStr) -> str:
    """
        将项目根目录加上传入的路径
    :type paths: object
    :return:
    """
    return os.path.join(BASE_PATH, *paths)


def is_image(image_path):
    return not image_path.startswith('~$') and os.path.splitext(image_path)[1][1:] in IMAGE_SUFFIX


if __name__ == '__main__':
    print(is_image(r'test.jpg'))
    print(is_image(r'test.txt'))
    pass
