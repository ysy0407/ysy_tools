#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: ysy
# @Time: 2022-04-14 10:50

import requests
import base64

'''
通用文字识别 https://ai.baidu.com/ai-doc/OCR/zk3h7xz52
'''


class BaiDuApi(object):

    def __init__(self, client_id, client_secret):
        self.client_id = client_id  # 官网获取的应用的AK（API Key）
        self.client_secret = client_secret  # 为官网获取的应用的SK（Secret Key）
        self.access_token, self.expires_in = self._get_access_token()
        print('access_token:', self.access_token, ', expires_in(s):', self.expires_in)

    def _get_access_token(self):
        host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={0}&client_secret={1}'.format(
            self.client_id,
            self.client_secret
        )
        print('get_access_token host:', host)
        response = requests.get(host)
        print(response)
        if response:
            print(response.json())
            # 要获取的Access Token，Access Token的有效期(秒为单位，有效期30天)
            return response.json()['access_token'], response.json()['expires_in']
        else:
            raise Exception('get access_token error: ', str(response.content))

    def ocr(self, file_path):
        # 二进制方式打开图片文件
        f = open(file_path, 'rb')
        # 图片转为base64编码
        img = base64.b64encode(f.read())

        print('ocr file path:', file_path)
        response = requests.post(
            "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=" + self.access_token,
            data={"image": img},
            headers={'content-type': 'application/x-www-form-urlencoded'}
        )
        if response:
            print('ocr response:', response.json())
            # [{'words': '姓名'}, {'words': '张三'}, {'words': '证件号码'}] 转为 ['姓名', '张三', '证件号码']
            return list(map(lambda e: e['words'], response.json()['words_result']))
        else:
            raise Exception('ocr appear error:',  str(response.content))


if __name__ == '__main__':
    bai_du_api = BaiDuApi('g1S8iIbqBGGe8xKlAmWEC6DA', 'W3Kwt7XrN72PWXdsFhfDLMjoIL99D9TS')
    print(bai_du_api.ocr(r'C:\data\wx-get-picture\HeSuanJieGuo\file_zh_name_clear\f94336a48822db66c645346215bd4b69.jpg'))
    pass