#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2022-04-12 16:13

import re
import shutil
from openpyxl import Workbook
from openpyxl.drawing.image import Image
from src.util.my_wx_auto import *
from src.util.bai_du_api_util import *
from src.util.common_util import *
from src.util.path_util import *

# 图片插入在Excel中的宽高
IMAGE_SIZE = (72, 156)
# 图片单元格的宽高
IMAGE_CELL_SIZE = (12, 120)


def save_wx_picture(pic_save_dir, group_name, last_msg_size):
    """
        保存微信聊天图片
    :param pic_save_dir: 图片保存路径
    :param group_name: 微信的群名称
    :param last_msg_size: 从最后多少条消息
    :return: 返回保存的图片名list
    """
    wx = WeChat()
    wx.GetSessionList()
    wx.ChatWith(group_name, RollTimes=1)

    # 保存消息最后size中的图片
    msgItemArray = wx.GetMessageItemArray(size=last_msg_size)
    pic_name_list = list()
    for item in msgItemArray:
        pic_name = WxUtils.SavePic(item, fileName='{date}-{nickName}-{random}', saveDirPath=pic_save_dir)
        if pic_name:
            pic_name_list.append(pic_name)
    print('pic list size:', len(pic_name_list))
    return pic_name_list


def get_room_number(pic_name):
    """
        根据图片名获取房间号，将图片名使用'-'分隔取第二个，再替换掉非数字的就是房间号
    :param pic_name: 格式如{date}-{nickName}-{random}的图片名
    :return:
    """
    return re.sub('[^0-9]', '', pic_name.split('-')[1])


class HandleAntigenPicture(object):
    '''将微信聊天图片，保存到excel中，并将群昵称处理为房间号'''

    # 表头
    HEADER_ROW = ['房间号', '抗原检测图片']
    
    def __init__(self, handle_base_dir, result_excel_name='antigen_result.xlsx') -> None:
        self.handle_base_dir = handle_base_dir
        self.no_room_number_dir = os.path.join(handle_base_dir, 'no_room_number')
        self.bai_du_api = None
        self.result_excel_path = os.path.join(handle_base_dir, result_excel_name)
        self.workbook = None
        self.result_sheet = None

    def _init_result_sheet(self):
        print('init result excel', self.result_excel_path)
        self.workbook = Workbook()
        self.result_sheet = self.workbook.worksheets[0]
        self.result_sheet.column_dimensions['B'].width = IMAGE_CELL_SIZE[0]
        for i, header in enumerate(self.HEADER_ROW):
            self.result_sheet.cell(1, i + 1, header)

    def write_result(self, row, room_number, pic_path):
        """
            将一行抗原结果写入excel
        :param row: 行号
        :param room_number: 房间号
        :param pic_path: 核酸截图路径
        """
        if not self.workbook:
            self._init_result_sheet()
        print('row :', row, room_number, pic_path)
        self.result_sheet.row_dimensions[row].height = IMAGE_CELL_SIZE[1]
        self.result_sheet.cell(row, 1, room_number)
        image = Image(pic_path)
        image.width, image.height = IMAGE_SIZE
        self.result_sheet.add_image(image, anchor='B' + str(row))

    def _save_result_sheet(self):
        print('save result excel', self.result_excel_path)
        self.workbook.save(self.result_excel_path)
        self.workbook.close()

    def save_to_excel(self, pic_name_list=None):
        self._init_result_sheet()
        for i, pic_name in enumerate(pic_name_list if pic_name_list else os.listdir(self.handle_base_dir)):
            if is_image(pic_name):
                pic_path = os.path.join(self.handle_base_dir, pic_name)
                room_number = get_room_number(pic_name)
                if not room_number:
                    no_room_number_pic_path = os.path.join(self.no_room_number_dir, pic_name)
                    print('pic_name:', pic_name, 'can\'t get room number, move to', no_room_number_pic_path)
                    shutil.copyfile(pic_path, no_room_number_pic_path)
                    continue
                self.write_result(i + 2, room_number, pic_path)
        self._save_result_sheet()

    def run(self, group_name, last_msg_size):
        pic_name_list = save_wx_picture(self.handle_base_dir, group_name, last_msg_size)
        # pic_name_list = ['20220413-409室-7003.jpg']
        print(pic_name_list)
        self.save_to_excel(pic_name_list)


class HandleNucleicPicture(object):
    '''使用ocr识别核酸检测结果的截图，并保存到excel中，并将群昵称处理为房间号'''

    # ocr结果中必须有的词语，若没有表示非核酸检测结果截图
    OCR_HAS_WORDS_LIST = ['姓名', '证件号码', '核酸']
    # 表头
    HEADER_ROW = ['房间号', '姓名', '是否阴性', '核酸结果文字', '核酸截图']

    def __init__(self, handle_base_dir, result_excel_name='nucleic_result.xlsx') -> None:
        self.handle_base_dir = handle_base_dir
        self.no_room_number_dir = os.path.join(handle_base_dir, 'no_room_number')
        self.bai_du_api = None
        self.result_excel_path = os.path.join(handle_base_dir, result_excel_name)
        self.workbook = None
        self.result_sheet = None

    def picture_ocr_handle(self, pic_name):
        if not self.bai_du_api:
            self.bai_du_api = BaiDuApi('g1S8iIbqBGGe8xKlAmWEC6DA', 'W3Kwt7XrN72PWXdsFhfDLMjoIL99D9TS')
        ocr_result_list = self.bai_du_api.ocr(os.path.join(self.handle_base_dir, pic_name))
        # 若ocr结果中含有以下文字表示是核酸检测的截图
        if all_in_list(HandleNucleicPicture.OCR_HAS_WORDS_LIST, ocr_result_list):
            # 获取'姓名'的后一个词语为姓名
            name = ocr_result_list[ocr_result_list.index('姓名') + 1]
            # 获取'检测结'的后一个词语，且'阴'在其中则为true。因有的使用了大字版的微信，“检测结果”一行显示不完就成了“检测结”
            result_word = ocr_result_list[any_in_list(['检测结'], ocr_result_list)[1] + 1]
            return name, '阴' in result_word, result_word
        else:
            return None, None, None

    def _init_result_sheet(self):
        print('init result excel', self.result_excel_path)
        self.workbook = Workbook()
        self.result_sheet = self.workbook.worksheets[0]
        self.result_sheet.column_dimensions['D'].width = 12
        self.result_sheet.column_dimensions['E'].width = IMAGE_CELL_SIZE[0]
        for i, header in enumerate(self.HEADER_ROW):
            self.result_sheet.cell(1, i + 1, header)

    def _save_result_sheet(self):
        print('save result excel', self.result_excel_path)
        self.workbook.save(self.result_excel_path)
        self.workbook.close()

    def write_result(self, row, room_number, name, result, result_word, pic_path):
        """
            将一行ocr结果写入excel
        :param row: 行号
        :param room_number: 房间号
        :param name: 姓名
        :param result: 是否阴性
        :param result_word: 核酸结果文字
        :param pic_path: 核酸截图路径
        """
        if not self.workbook:
            self._init_result_sheet()
        print('row :', row, room_number, name, result, result_word, pic_path)
        self.result_sheet.row_dimensions[row].height = IMAGE_CELL_SIZE[1]
        self.result_sheet.cell(row, 1, room_number)
        self.result_sheet.cell(row, 2, name)
        self.result_sheet.cell(row, 3, result)
        self.result_sheet.cell(row, 4, result_word)
        image = Image(pic_path)
        image.width, image.height = IMAGE_SIZE
        self.result_sheet.add_image(image, anchor='E' + str(row))

    def save_to_excel(self, pic_name_list=None):
        self._init_result_sheet()
        for i, pic_name in enumerate(pic_name_list if pic_name_list else os.listdir(self.handle_base_dir)):
            if is_image(pic_name):
                pic_path = os.path.join(self.handle_base_dir, pic_name)
                room_number = get_room_number(pic_name)
                if not room_number:
                    no_room_number_pic_path = os.path.join(self.no_room_number_dir, pic_name)
                    print('pic_name:', pic_name, 'can\'t get room number, move to', no_room_number_pic_path)
                    shutil.copyfile(pic_path, no_room_number_pic_path)
                    continue
                name, result, result_word = self.picture_ocr_handle(pic_path)
                # name, result, result_word = ('周仲韵<', True, '【阴性】')
                if not name:
                    print('pic_name:', pic_name, 'is not a covid-19 test picture')
                    continue
                self.write_result(i + 2, room_number, name, result, result_word, pic_path)
                if not result:
                    print('pic_name:', pic_name, 'name: ', name, 'is not negative, result_word:', result_word)
        self._save_result_sheet()

    def run(self, group_name, last_msg_size):
        pic_name_list = save_wx_picture(self.handle_base_dir, group_name, last_msg_size)
        # pic_name_list = ['20220413-409室-7003.jpg']
        print(pic_name_list)
        self.save_to_excel(pic_name_list)


if __name__ == '__main__':
    # handleAntigenPicture = HandleAntigenPicture(r'C:\data\wx-get-picture\KangYuanJieGuo-test')
    # handleAntigenPicture.run('30弄2号楼业主群', 50)
    handleNucleicPicture = HandleNucleicPicture(r'C:\data\wx-get-picture\HeSuanJieGuo-test')
    handleNucleicPicture.save_to_excel()
    # handleNucleicPicture.run('管一二街坊清美', 50)
    pass
