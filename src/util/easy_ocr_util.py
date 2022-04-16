#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2022-04-12 09:10

import os
import time
import csv
import hashlib
import shutil
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple easyocr
# 下载模型：https://www.jaided.ai/easyocr/modelhub/
# 需要的模型：craft_mlt_25k、zh_sim_g2、english_g2
# 下载模型比较慢时，可以用服务器wget --no-check-certificate下载
import easyocr
import easyocr.utils as utils
# cuda模块使用GPU，处理更快，安装成功检查：print(cuda.gpus)，输出：<Managed Device 0>
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numba
# from numba import cuda
# 参考文档https://blog.csdn.net/juzicode00/article/details/122243330


# 路径中不能有中文
def run(picture_dir_path):
    name_mapper_file_path = os.path.join(picture_dir_path, 'ocr_result.csv')
    print('name_mapper_file_path', name_mapper_file_path)
    result_list = []
    # 创建reader对象，中文简体：ch_sim，中文繁体：ch_tra，英文：en
    reader = easyocr.Reader(lang_list=['ch_sim', 'en'], download_enabled=False, gpu=False)
    for file_name in os.listdir(picture_dir_path):
        # 找出文件中不以~$开头的文件（~$是为了排除临时文件的）
        if not file_name.endswith('.csv') and not file_name.startswith('~$'):
            file_path = os.path.join(picture_dir_path, file_name)
            print(file_path)
            start_time = int(round(time.time()))
            # 读取图像，若无detail=0，输出：边框坐标、文本、识别概率:([[16, 428], [60, 428], [60, 454], [16, 454]], '美团', 0.9121357490301221)
            result = reader.readtext(file_path, detail=0)
            # 结果
            print('use time:', int(round(time.time())) - start_time, 's, result:', result)
            result_list.append([file_name, str(result)])
    with open(name_mapper_file_path, 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(['文件名', 'OCR结果'])
        f_csv.writerows(result_list)


def file_name_clear(picture_dir_path):
    result_dir = os.path.join(picture_dir_path, 'file_zh_name_clear')
    print('result_dir', result_dir)
    name_mapper_file_path = os.path.join(result_dir, 'file_name_mapper.csv')
    print('name_mapper_file_path', name_mapper_file_path)
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    file_name_mapper = []
    for file_name in os.listdir(picture_dir_path):
        src_file_path = os.path.join(picture_dir_path, file_name)
        if os.path.isdir(src_file_path):
            continue
        name, ex = os.path.splitext(file_name)
        final_file_name = hashlib.md5(name.encode('utf-8')).hexdigest() + ex
        # 将文件名内的中文替换为空字符串
        file_name_mapper.append([file_name, final_file_name])
        result_file_path = os.path.join(result_dir, final_file_name)
        if os.path.exists(result_file_path):
            print('file exist:', result_file_path)
        else:
            shutil.copyfile(src_file_path, result_file_path)
    with open(name_mapper_file_path, 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(['原文件名', '现文件名'])
        f_csv.writerows(file_name_mapper)


def execute(params: dict):
    # 执行获取结果，返回结果文件路径
    return run(params["picture_dir_path"])


if __name__ == '__main__':
    run(r'C:\data\wx-get-picture\HeSuanJieGuo\file_zh_name_clear')
    # file_zh_name_clear(r'C:\data\wx-get-picture\HeSuanJieGuo')


    pass
