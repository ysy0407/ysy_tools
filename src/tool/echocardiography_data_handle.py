#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2021-03-13 19:20

import os
import csv
import time
import argparse


class Handle(object):

    def __init__(self, read_path, need_handle_parameter, result_csv_headers):
        self.read_path = read_path
        self.write_path = self.read_path.replace('.csv', '_result.csv')
        self.need_handle_parameter = need_handle_parameter
        self.result_csv_headers = result_csv_headers
        self.min_row_len = 5

    def execute(self):
        print('handle starting')
        start_time = int(round(time.time() * 1000))
        with open(self.write_path, 'w', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(self.result_csv_headers)
            f_csv.writerows(
                self.get_avg_result_list(self.get_src_result_list())
            )
        print('result write path:', self.write_path)
        print("handle over, use time:", int(round(time.time() * 1000)) - start_time, "ms")
        return self.write_path

    def get_src_result_list(self):
        src_result_list = list()
        read_detail_data_flag = False  # 是否读取具体数据
        last_result_data = list()
        # 根据Series Name为一组数据，循环读取
        with open(self.read_path, encoding="utf-8") as f:
            f_csv = csv.reader(f)
            for row in f_csv:
                # 若行数据长度小于5则填充空数据，直到行数据长度为5
                if len(row) < self.min_row_len:
                    for i in range(self.min_row_len - len(row)):
                        row.append('')
                if not read_detail_data_flag:
                    # 一段新的数据，重置获取Series Name，及数据
                    if 'Series Name' == row[0]:
                        last_result_data = [row[1]]
                        for i in range(len(self.need_handle_parameter)):
                            last_result_data.append([])
                    # 当读取到Measurement表示可以开始读取具体数据
                    elif 'Measurement' == row[0]:
                        read_detail_data_flag = True
                    # 当读取到No measurements found表示没有具体数据
                    elif 'No measurements found' == row[0]:
                        # 将数据数据清零，避免加入结果列
                        last_result_data = []
                        read_detail_data_flag = False
                else:
                    parameter_index = -1
                    try:
                        parameter_index = self.need_handle_parameter.index(row[2])
                    except ValueError as v:
                        pass
                    # 若当前参数需要处理则将Value放入对应的list
                    if parameter_index >= 0:
                        last_result_data[parameter_index + 1].append(float(row[4]))
                    # 当开始读取具体数据后第一次读取到空字符串表示该段数据读取完毕，求平均数
                    elif '' == row[0]:
                        read_detail_data_flag = False
                        src_result_list.append(last_result_data)
            # 不为0时才放入结果list，为0表示没有具体数据
            if len(last_result_data) != 0:
                src_result_list.append(last_result_data)
        return src_result_list

    def get_avg_result_list(self, src_result_list):
        avg_result_list = list()
        for src_result_element in src_result_list:
            result_data_avg = [src_result_element[0].replace('月', '-').replace('日', '')]
            print('src', src_result_element)
            for i in range(len(self.need_handle_parameter)):
                # 可能有这个Series Name，但是某个需要统计的没有数据，此时填充0
                if len(src_result_element[i + 1]) == 0:
                    result_data_avg.append(0)
                else:
                    result_data_avg.append(format(sum(src_result_element[i + 1]) / len(src_result_element[i + 1]), '.2f'))
            print('avg', result_data_avg)
            avg_result_list.append(result_data_avg)
        return avg_result_list


def execute(params: dict):
    file_path = params["file_path"]
    return Handle(
        # 需要处理的文件路径，'C:\\Users\什锦小沐\\Desktop\郑丽霞\超声数据处理\\2021-06-22-21-04-09.csv'
        file_path,
        # 需要处理的参数，当parameter为列表中值时，会根据Series Name求平均数
        ['Ejection Fraction', 'Fractional Shortening'],
        # 结果文件的标题
        ['Series Name', 'Avg Ejection Fraction(%)', 'Avg Fractional Shortening(%)']
    ).execute()


'''
    安装python3.7.9环境
    进入CMD窗口（Win+R，输入cmd，回车）
    输入命令：
        python 脚本路径 -r 需要进行超声数据处理的csv文件路径
        如：python C:\python\zlx_echocardiography_data_handle.py - r C:\python\2021-06-22-21-04-09.csv
    回车
    处理好的结果在源文件目录以_result.csv的文件

'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    read_path_help = "需要进行超声数据处理的csv文件路径"
    parser.add_argument('-r', '--read_path', help=read_path_help)
    args = parser.parse_args()
    if not os.path.isfile(args.read_path):
        print(read_path_help, "文件不存在：", args.read_path)
    elif not args.read_path.endswith('.csv'):
        print(args.read_path, "文件不是csv格式")
    else:
        Handle(
            # 需要处理的文件路径，'C:\\Users\什锦小沐\\Desktop\郑丽霞\超声数据处理\\2021-06-22-21-04-09.csv'
            args.read_path,
            # 需要处理的参数，当parameter为列表中值时，会根据Series Name求平均数
            ['Ejection Fraction', 'Fractional Shortening'],
            # 结果文件的标题
            ['Series Name', 'Avg Ejection Fraction(%)', 'Avg Fractional Shortening(%)']
        ).execute()

    # Handle(
    #     # 需要处理的文件路径，
    #     'C:\\Users\什锦小沐\\Desktop\郑丽霞\超声数据处理\\2021-06-30-15-30-29.csv',
    #     # 需要处理的参数，当parameter为列表中值时，会根据Series Name求平均数
    #     ['Ejection Fraction', 'Fractional Shortening'],
    #     # 结果文件的标题
    #     ['Series Name', 'Avg Ejection Fraction(%)', 'Avg Fractional Shortening(%)']
    # ).execute()
