#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2022-04-14 12:48


# 基因互补dict
GENE_COMPLEMENT_DICT = {
    'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N',
    'a': 't', 't': 'a', 'g': 'c', 'c': 'g', 'n': 'n'
}


def run(file_path):
    """
        将文件中的每行的内容进行基因反向互补
    :param file_path:
    :return: 结果txt文件路径
    """
    result_file_path = file_path.replace('.txt', '-result.txt')
    with open(file_path, 'r') as f:
        lines = f.readlines()
        print('lines', len(lines))
        # 将传入的字符每个都在dict中找到对应的，并获取其key拼接为字符串，最后再反转，并在结尾加上换行符
        result_list = list(map(lambda s: ''.join([GENE_COMPLEMENT_DICT[c] for c in s.replace('\n', '')])[::-1] + '\n', lines))
    # 将结果写入文件
    with open(result_file_path, 'w') as f:
        f.writelines(result_list)
    return result_file_path


def execute(params: dict):
    return run(params["file_path"])


if __name__ == '__main__':
    run(r'C:\data\split_txt\seq.txt')
    pass
