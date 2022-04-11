#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2022-04-11 10:49


import os
import re
from win32com import client as wc
from docx import Document


def run(word_dir_path):
    # 创建图片输出文件夹
    picture_dir = os.path.join(word_dir_path, 'picture')
    print('picture_dir:', picture_dir)
    if not os.path.exists(picture_dir):
        os.mkdir(picture_dir)
    # 将doc转为docx
    # word = wc.Dispatch("Word.Application")
    # for file_name in os.listdir(word_dir_path):
    #     # 找出文件中以.doc结尾并且不以~$开头的文件（~$是为了排除临时文件的）
    #     if file_name.endswith('.doc') and not file_name.startswith('~$'):
    #         print('doc to docx handle file:', file_name)
    #         doc = word.Documents.Open(os.path.join(word_dir_path, file_name))
    #         # # 将文件名与后缀分割
    #         rename = os.path.splitext(file_name)
    #         # 将文件另存为.docx
    #         doc.SaveAs(os.path.join(word_dir_path,  rename[0] + '.docx'), 12)  # 12表示docx格式
    #         doc.Close()
    # word.Quit()
    # 从docx中获取图片
    for file_name in os.listdir(word_dir_path):
        # 找出文件中以.docx结尾并且不以~$开头的文件（~$是为了排除临时文件的）
        if file_name.endswith('.docx') and not file_name.startswith('~$'):
            print('get picture handle file:', file_name)
            document = Document(os.path.join(word_dir_path, file_name))
            dict_rel = document.part._rels
            for rel in dict_rel:
                rel = dict_rel[rel]
                if "image" in rel.target_ref:
                    img_name = re.findall("/(.*)", rel.target_ref)[0]
                    if os.sep in file_name:
                        new_name = file_name.split('\\')[-1]
                    else:
                        new_name = file_name.split('/')[-1]
                    with open(os.path.join(picture_dir, f'{new_name}-' + '.' + f'{img_name}'), "wb") as f:
                        f.write(rel.target_part.blob)


def execute(params: dict):
    # 执行获取结果，返回结果文件路径
    return run(params["word_dir_path"])


if __name__ == '__main__':
    run(r'C:\Users\什锦小沐\Desktop\尹豪强\word图片提取')
    pass
