#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : songyuanyu

import os
import time
from openpyxl import load_workbook


# 根据第一个sheet获取替换的数据dict，key：第一列的值，value：第二列的值
def get_replace_dict(replace_sheet):
    result_dict = dict()
    src_id_col = replace_sheet['A']
    replace_id_col = replace_sheet['B']
    for i in range(1, len(src_id_col)):
        src_id_cell = src_id_col[i]
        replace_id_cell = replace_id_col[i]
        if src_id_cell is not None and src_id_cell.value is not None and str(src_id_cell.value).strip():
            result_dict[str(src_id_cell.value).strip()] = str(replace_id_cell.value).strip()
    print('替换的dict：', result_dict)
    return result_dict


# 根据第二个sheet和替换的数据进行替换
def replace_seq_data(seq_data_sheet, replace_dict):
    seq_data_col = seq_data_sheet['A']
    for i in range(1, len(seq_data_col)):
        seq_data_cell = seq_data_col[i]
        if seq_data_cell is not None and seq_data_cell.value is not None and str(seq_data_cell.value).strip():
            seq_data_cell_str = str(seq_data_cell.value).strip()
            # 若存在（:）则分隔后分别替换，若不存在则按整个cell的值进行替换
            if ':' in seq_data_cell_str:
                # 取出分隔后实际的seq
                seq_data_array = seq_data_cell_str.split(':')
                # 若dict中存在该key则进行替换，否则使用原值
                seq_data_cell.value = str(replace_dict.get(seq_data_array[0]) if seq_data_array[0] in replace_dict else seq_data_array[0]) \
                                      + ':' \
                                      + str(replace_dict.get(seq_data_array[1]) if seq_data_array[1] in replace_dict else seq_data_array[1])
            else:
                seq_data_cell.value = str(replace_dict.get(seq_data_cell_str) if seq_data_cell_str in replace_dict else seq_data_cell_str)


# 执行
def run(file_path):
    print('当前处理文件：', file_path)
    start_time = int(time.time())
    workbook = load_workbook(file_path)
    seq_sheets = workbook.worksheets
    replace_seq_data(seq_sheets[1], get_replace_dict(seq_sheets[0]))
    workbook.save(file_path)
    print("耗时：", int(time.time()) - start_time, "second")


def execute(params: dict):
    file_path = params["file_path"]
    run(file_path)
    return file_path


'''
    将excel中第二个sheet的第一列的字符串，以第二个sheet的第一列为key，第二列为value进行替换
'''
if __name__ == "__main__":
    # 若为目录则循环目录中的文件，否则直接执行
    path = 'C:\PycharmProjects\Sany\src\yhq\\file\G_22_replace.xlsx'
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for file in files:
                run(os.path.join(root, file))
    else:
        run(path)
