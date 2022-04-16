#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2022-04-15 09:25


def all_in_list(small_list, big_list):
    """
        若小数组全部在大数组中存在则返回true，否则返回false
    :param small_list:
    :param big_list:
    :return:
    """
    if small_list is None or big_list is None or len(small_list) > len(big_list):
        return False
    for small_e in small_list:
        if small_e not in big_list:
            return False
    return True


def any_in_list(word_list, the_list):
    """
        若word_list任意一个存在于the_list中则返回对应的索引
    :param word_list:
    :param the_list:
    :return: 找到：（word_list索引, the_list索引），没找到：None
    """
    for i, val in enumerate(the_list):
        for j, word in enumerate(word_list):
            if word in val:
                return j, i
    return None


if __name__ == '__main__':
    print(all_in_list([1, 2, 3], [1, 2, 3, 4, 5]))
    print(all_in_list([1, 2, 3], [1, 3, 4, 5]))
    print(any_in_list(['核酸'], ['测试', '核酸结果：']))
    pass
