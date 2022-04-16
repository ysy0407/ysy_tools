#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2022-04-12 21:18
# !python3
# -*- coding: utf-8 -*-
"""
Author: tikic@qq.com
Source: https://github.com/cluic/wxauto
License: MIT License
Version: 3.3.5.3
# 因为基于网页版的itchat都已经不能用了，就用了基于uiautomation的wxauto
"""
import uiautomation as uia
import win32gui, win32con
import win32clipboard as wc
import time
import random
import os

AUTHOR_EMAIL = 'tikic@qq.com'
UPDATE = '2021-09-06'
VERSION = '3.3.5.3'

COPYDICT = {}


class WxParam:
    PICTURE_MSG_TYPE = '图片'
    SpecialTypes = ['[文件]', '[图片]', '[视频]', '[音乐]', '[链接]', '[动画表情]']


class WeChat:
    def __init__(self):
        self.UiaAPI = uia.WindowControl(ClassName='WeChatMainWndForPC')
        self.SessionList = self.UiaAPI.ListControl(Name='会话')
        self.EditMsg = self.UiaAPI.EditControl(Name='输入')
        self.SearchBox = self.UiaAPI.EditControl(Name='搜索')
        self.MsgList = self.UiaAPI.ListControl(Name='消息')
        self.SessionItemList = []

    def GetSessionList(self, reset=False):
        '''获取当前会话列表，更新会话列表'''
        self.SessionItem = self.SessionList.ListItemControl()
        SessionList = []
        if reset:
            self.SessionItemList = []
        for i in range(100):
            try:
                name = self.SessionItem.Name
            except:
                break
            if name not in self.SessionItemList:
                self.SessionItemList.append(name)
            if name not in SessionList:
                SessionList.append(name)
            self.SessionItem = self.SessionItem.GetNextSiblingControl()
        return SessionList

    def Search(self, keyword):
        '''
        查找微信好友或关键词
        keywords: 要查找的关键词，str   * 最好完整匹配，不完全匹配只会选取搜索框第一个
        '''
        self.UiaAPI.SetFocus()
        time.sleep(0.2)
        self.UiaAPI.SendKeys('{Ctrl}f', waitTime=1)
        self.SearchBox.SendKeys(keyword, waitTime=1.5)
        self.SearchBox.SendKeys('{Enter}')

    def ChatWith(self, who, RollTimes=None):
        '''
        打开某个聊天框
        who : 要打开的聊天框好友名，str;  * 最好完整匹配，不完全匹配只会选取搜索框第一个
        RollTimes : 默认向下滚动多少次，再进行搜索
        '''
        self.UiaAPI.SwitchToThisWindow()
        RollTimes = 10 if not RollTimes else RollTimes

        def roll_to(who=who, RollTimes=RollTimes):
            for i in range(RollTimes):
                if who not in self.GetSessionList()[:-1]:
                    self.SessionList.WheelDown(wheelTimes=3, waitTime=0.1 * i)
                else:
                    time.sleep(0.5)
                    self.SessionList.ListItemControl(Name=who).Click(simulateMove=False)
                    return 1
            return 0

        rollresult = roll_to()
        if rollresult:
            return 1
        else:
            self.Search(who)
            return roll_to(RollTimes=1)

    def SendMsg(self, msg, clear=True):
        '''向当前窗口发送消息
        msg : 要发送的消息
        clear : 是否清除当前已编辑内容
        '''
        self.UiaAPI.SwitchToThisWindow()
        if clear:
            self.EditMsg.SendKeys('{Ctrl}a', waitTime=0)
        self.EditMsg.SendKeys(msg, waitTime=0)
        self.EditMsg.SendKeys('{Enter}', waitTime=0)

    def SendFiles(self, *filepath, not_exists='ignore'):
        """向当前聊天窗口发送文件
        not_exists: 如果未找到指定文件，继续或终止程序
        *filepath: 要复制文件的绝对路径"""
        global COPYDICT
        key = ''
        for file in filepath:
            file = os.path.realpath(file)
            if not os.path.exists(file):
                if not_exists.upper() == 'IGNORE':
                    print('File not exists:', file)
                    continue
                elif not_exists.upper() == 'RAISE':
                    raise FileExistsError('File Not Exists: %s' % file)
                else:
                    raise ValueError('param not_exists only "ignore" or "raise" supported')
            key += '<EditElement type="3" filepath="%s" shortcut="" />' % file
        if not key:
            return 0
        if not COPYDICT:
            self.EditMsg.SendKeys(' ', waitTime=0)
            self.EditMsg.SendKeys('{Ctrl}a', waitTime=0)
            self.EditMsg.SendKeys('{Ctrl}c', waitTime=0)
            self.EditMsg.SendKeys('{Delete}', waitTime=0)
            while True:
                try:
                    COPYDICT = WxUtils.CopyDict()
                    break
                except:
                    pass
        wc.OpenClipboard()
        wc.EmptyClipboard()
        wc.SetClipboardData(13, '')
        wc.SetClipboardData(16, b'\x04\x08\x00\x00')
        wc.SetClipboardData(1, b'')
        wc.SetClipboardData(7, b'')
        for i in COPYDICT:
            copydata = COPYDICT[i].replace(b'<EditElement type="0"><![CDATA[ ]]>', key.encode()).replace(b'type="0"',
                                                                                                         b'type="3"')
            wc.SetClipboardData(int(i), copydata)
        wc.CloseClipboard()
        self.SendClipboard()
        return 1

    def SendClipboard(self):
        '''向当前聊天页面发送剪贴板复制的内容'''
        self.SendMsg('{Ctrl}v')

    def GetMessageItemArray(self, size=10):
        itemArray = self.MsgList.GetChildren() if size == 0 else self.MsgList.GetChildren()[-size:]
        itemArray.reverse()
        return itemArray

    def GetAllMessage(self):
        '''获取当前窗口中加载的所有聊天记录'''
        MsgDocker = []
        MsgItems = self.GetMessageItemArray(size=0)
        for MsgItem in MsgItems:
            MsgDocker.append(WxUtils.SplitMessage(MsgItem))
        return MsgDocker

    def GetLastMessage(self):
        '''获取当前窗口中最后一条聊天记录'''
        return self.GetLastMessageArray(size=1)[0]

    def GetLastMessageArray(self, size=10):
        '''获取当前窗口中最后几条聊天记录'''
        uia.SetGlobalSearchTimeout(1.0)
        MsgArray = []
        MsgItemArray = self.GetMessageItemArray(size)
        for MsgItem in MsgItemArray:
            MsgArray.append(WxUtils.SplitMessage(MsgItem))
        uia.SetGlobalSearchTimeout(10.0)
        return MsgArray

    def LoadMoreMessage(self, n=0.1):
        '''定位到当前聊天页面，并往上滚动鼠标滚轮，加载更多聊天记录到内存'''
        n = 0.1 if n < 0.1 else 1 if n > 1 else n
        self.MsgList.WheelUp(wheelTimes=int(500 * n), waitTime=0.1)

    def SendScreenshot(self, name=None, classname=None):
        '''发送某个桌面程序的截图，如：微信、记事本...
        name : 要发送的桌面程序名字，如：微信
        classname : 要发送的桌面程序类别名，一般配合 spy 小工具使用，以获取类名，如：微信的类名为 WeChatMainWndForPC'''
        if name and classname:
            return 0
        else:
            hwnd = win32gui.FindWindow(classname, name)
        if hwnd:
            WxUtils.Screenshot(hwnd)
            self.SendClipboard()
            return 1
        else:
            return 0


class WxUtils:

    @staticmethod
    def SplitMessage(msgItem):
        uia.SetGlobalSearchTimeout(0)
        runtimeId = ''.join([str(i) for i in msgItem.GetRuntimeId()])
        msgItemName = msgItem.Name
        msg=None
        try:
            # 昵称和群昵称都有时，是消息
            user_name_item = msgItem.ButtonControl(RegexName=r'^.*$')
            nick_name_item = msgItem.TextControl(RegexName=r'^.*$')
            msg = ('Msg', user_name_item.Name, nick_name_item.Name, msgItemName, runtimeId)
        except LookupError:
            # 当有Name相等的子节点时，窗格：时间，编辑：撤回，按钮：查看更多消息，文本：以下为新消息
            childControlType = msgItem.Control(Name=msgItemName).ControlType
            if childControlType == uia.ControlType.PaneControl:
                msg = ('Time', msgItemName, runtimeId)
            elif msgItemName.endswith('撤回了一条消息') and childControlType == uia.ControlType.EditControl:
                msg = ('Revoke', msgItemName, runtimeId)
            elif msgItemName == '查看更多消息' and childControlType == uia.ControlType.ButtonControl:
                msg = ('More', msgItemName, runtimeId)
            elif msgItemName == '以下为新消息' and childControlType == uia.ControlType.TextControl:
                msg = ('New', msgItemName, runtimeId)
            elif childControlType == uia.ControlType.EditControl:
                msg = ('SYS', msgItemName, runtimeId)
            else:
                msg = ('Unknown', msgItemName, runtimeId)
        uia.SetGlobalSearchTimeout(10.0)
        return msg

    @staticmethod
    def _getSpecialMsgType(msgType):
        return '[{}]'.format(msgType)

    @staticmethod
    def SetClipboard(data, dtype='text'):
        '''复制文本信息或图片到剪贴板
        data : 要复制的内容，str 或 Image 图像'''
        if dtype.upper() == 'TEXT':
            type_data = win32con.CF_UNICODETEXT
        elif dtype.upper() == 'IMAGE':
            from io import BytesIO
            type_data = win32con.CF_DIB
            output = BytesIO()
            data.save(output, 'BMP')
            data = output.getvalue()[14:]
        else:
            raise ValueError('param (dtype) only "text" or "image" supported')
        wc.OpenClipboard()
        wc.EmptyClipboard()
        wc.SetClipboardData(type_data, data)
        wc.CloseClipboard()

    @staticmethod
    def Screenshot(hwnd, to_clipboard=True):
        '''为句柄为hwnd的窗口程序截图
        hwnd : 句柄
        to_clipboard : 是否复制到剪贴板
        '''
        import pyscreenshot as shot
        bbox = win32gui.GetWindowRect(hwnd)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, \
                              win32con.SWP_SHOWWINDOW | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, \
                              win32con.SWP_SHOWWINDOW | win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        win32gui.BringWindowToTop(hwnd)
        im = shot.grab(bbox)
        if to_clipboard:
            WxUtils.SetClipboard(im, 'image')
        return im

    @staticmethod
    def SavePic(msgItem, fileName='{date}-{userName}-{nickName}-{random}', saveDirPath=os.getcwd()):
        """
            根据传入的消息找到子节点中是按钮且Name属性为空的，点击后进行保存，若图片不在当前窗口显示时，会自动滚动
            TODO 每次调用都会创建WeChat对象，有点费资源啊
        :param msgItem: 需要保存的节点
        :param fileName: 指定文件名格式，其中的花括号会转为对应的内容（会将用户名和昵称中的短杠去掉），为空则使用文件原名，在微信里就是：微信图片加日期和时间
        :param saveDirPath: 图片保存的文件夹绝对路径，不存在则创建，默认是当前路径，若不是个文件夹则抛出错误
        :return: 保存成功时返回图片名，非图片的item时返回None
        """
        if msgItem is None or not msgItem.Name == WxUtils._getSpecialMsgType(WxParam.PICTURE_MSG_TYPE):
            return None
        if not os.path.exists(saveDirPath):
            os.mkdir(saveDirPath)
            print('the path is not exist, now make it', saveDirPath)
        if not os.path.isdir(saveDirPath):
            raise Exception('the path is not a dir', saveDirPath)
        wx = WeChat()
        # 图片上边界小于微信聊天窗口界面表示在上方，要往上滚动
        while msgItem.BoundingRectangle.top < wx.MsgList.BoundingRectangle.top+10:
            wx.MsgList.WheelUp(wheelTimes=3, waitTime=0.1)
        # 图片下边界大于微信聊天窗口界面表示在下方，要往下滚动
        while msgItem.BoundingRectangle.bottom > wx.MsgList.BoundingRectangle.bottom-10:
            wx.MsgList.WheelDown(wheelTimes=3, waitTime=0.1)
        msgItem.ButtonControl(Name='').Click()
        Pic = uia.WindowControl(ClassName='ImagePreviewWnd', Name='图片查看')
        Pic.SendKeys('{Ctrl}s')
        SaveAs = Pic.WindowControl(ClassName='#32770', Name='另存为...')
        SaveAsEdit = SaveAs.EditControl(ClassName='Edit', Name='文件名:')
        # SaveButton = Pic.ButtonControl(ClassName='Button', Name='保存(S)')
        PicName, Ex = os.path.splitext(SaveAsEdit.GetValuePattern().Value)
        if not fileName:
            fileName = PicName
        else:
            msg = WxUtils.SplitMessage(msgItem)
            fileName = fileName.replace('{date}', time.strftime('%Y%m%d', time.localtime()))\
                .replace('{userName}', msg[1].replace('-', ''))\
                .replace('{nickName}', msg[2].replace('-', ''))\
                .replace('{random}', str(int(random.uniform(10000, 99999))))
        FilePath = os.path.realpath(os.path.join(saveDirPath, fileName + Ex))
        print('save picture:', FilePath)
        SaveAsEdit.SendKeys(FilePath)
        # 将点击保存键保存改为传入回车键，减少鼠标移动过程以加快速度
        SaveAsEdit.SendKeys('{Enter}')
        # SaveButton.Click()
        Pic.SendKeys('{Esc}')
        return fileName + Ex

    @staticmethod
    def ControlSize(control):
        locate = control.BoundingRectangle
        size = (locate.width(), locate.height())
        return size

    @staticmethod
    def ClipboardFormats(unit=0, *units):
        units = list(units)
        wc.OpenClipboard()
        u = wc.EnumClipboardFormats(unit)
        wc.CloseClipboard()
        units.append(u)
        if u:
            units = WxUtils.ClipboardFormats(u, *units)
        return units

    @staticmethod
    def CopyDict():
        Dict = {}
        for i in WxUtils.ClipboardFormats():
            if i == 0:
                continue
            wc.OpenClipboard()
            try:
                content = wc.GetClipboardData(i)
                wc.CloseClipboard()
            except:
                wc.CloseClipboard()
                raise ValueError
            if len(str(i)) >= 4:
                Dict[str(i)] = content
        return Dict



if __name__ == '__main__':
    wx = WeChat()
    wx.GetSessionList()
    wx.ChatWith('文件传输助手', RollTimes=1)

    # 获取最后100条消息，并打印
    # msgs = wx.GetLastMessageArray(size=100)
    # for msg in msgs:
    #     print(msg)

    # 保存消息中的图片
    msgItemArray = wx.GetMessageItemArray(size=50)
    for item in msgItemArray:
        print(item)
        WxUtils.SavePic(item, fileName='{date}-{nickName}-{random}', saveDirPath=r'C:\data\wx-get-picture\HeSuanJieGuo')

    # 每秒获取最后一条消息并打印，若重复则不打印
    # last_msg_id = None
    # for i in range(100):
    #     msg = wx.GetLastMessage()
    #     if not msg[2] == last_msg_id:
    #         print(msg)
    #         last_msg_id = msg[2]
    #     time.sleep(1)
    pass