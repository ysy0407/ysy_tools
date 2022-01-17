#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2021-12-26 16:44


import time


def timestamps_to_datetime(timestamps=int(time.time())):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamps))


if __name__ == '__main__':
    print(timestamps_to_datetime(1640536755))
    print(timestamps_to_datetime())
    pass
