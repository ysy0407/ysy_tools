#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : songyuanyu

from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

from src.util.logger_util import Logger
import csv


logger = Logger.init(file_name='../../logs/oxford.log')


class Oxford2(object):

    def __init__(self, chrome_path, paper_save_dir):
        # 本地的谷歌浏览器启动地址
        self.chrome_path = chrome_path
        # 文档保存地址
        self.paper_save_dir = paper_save_dir
        # 主域名
        self.home_domain = "https://academic.oup.com"
        # 主地址
        self.home_url = self.home_domain + "/nar/search-results?f_TocHeadingTitle=Database+Issue&fl_SiteID=5127&rg_ArticleDate=01%2f01%2f2020+TO+12%2f31%2f2021&page="
        # 详情页链接保存的csv路径
        self.page_info_csv_path = paper_save_dir + '\\download_page_info.csv'
        # 下载文档链接保存的csv路径
        self.paper_info_csv_path = paper_save_dir + '\\download_paper_info.csv'
        # 下载文档链接csv表头
        self.paper_info_csv_headers = ["title", "published", "download_paper_url"]
        # 浏览器驱动
        self.browser_driver = self.browser_init(False)

    # 翻页，获取详情页链接，并保存至csv
    def get_page_urls(self, cur_page, last_page):
        download_page_urls = []  # 获取下载页面的链接地址
        while cur_page <= last_page:
            logger.info("第%d页" % cur_page)
            logger.info(self.home_url + str(cur_page))
            res = requests.get(self.home_url + str(cur_page), headers=self.get_http_header())
            # logger.info(res.content)
            soup = BeautifulSoup(res.content)
            for aElement in soup.find_all(name="a", class_="article-link at-sr-article-title-link"):
                download_page_url = self.home_domain + aElement['href']
                logger.info(download_page_url)
                download_page_urls.append(download_page_url)
                self.write_csv(self.paper_info_csv_path, download_page_url)
            cur_page += 1
            logger.info(len(download_page_urls))
            sleep(3)

    # 读取csv保存的详情页链接，打开后获取下载文档链接，并将下载文档链接保存至csv
    def get_paper_urls(self, continue_num=0):
        download_paper_urls = []  # 获取下载文章的链接地址
        self.write_csv(self.paper_info_csv_path, self.paper_info_csv_headers)
        with open(self.paper_info_csv_path, 'r', newline='', encoding='utf-8') as f:
            csv_lines = csv.reader(f)
            i = 0
            for download_page_url in csv_lines:
                i += 1
                # 从断点处获取，跳过前n条
                if i < continue_num:
                    continue
                res = requests.get(download_page_url[0], headers=self.get_http_header())
                # logger.info(res.content)
                # 使用BeautifulSoup解析获取到的html
                soup = BeautifulSoup(res.content)
                download_paper_url = self.home_domain + soup.find(name="a", class_="al-link pdf article-pdfLink")['href']
                csv_line = [
                    # 标题前后会有制表位或换行，进行替换
                    soup.find(name="h1",
                              class_="wi-article-title article-title-main accessible-content-title at-articleTitle").text
                        .replace('\r\n                        ', '')
                        .replace("\r\n ", "")
                        .replace("\n ", ""),
                    soup.find(name="div", class_="citation-date").text,
                    download_paper_url
                ]
                logger.info(csv_line)
                self.write_csv(self.paper_info_csv_path, csv_line)
                download_paper_urls.append(download_paper_url)
                sleep(3)

        logger.info(len(download_paper_urls))

    # 打开保存下载文档链接的csv，通过链接下载文档
    def download_paper(self, continue_num=0):
        with open(self.paper_info_csv_path, 'r', newline='', encoding='utf-8') as f:
            csv_lines = csv.reader(f)
            i = 0
            for download_paper_info in csv_lines:
                i += 1
                # 从断点处获取，跳过前n条
                if i < continue_num:
                    continue
                try:
                    sleep(10)
                    self.browser_driver.get(download_paper_info[2])
                    logger.info("download success, url: " + download_paper_info[2])
                except Exception as e:
                    logger.info("download fail, url: " + download_paper_info[2])

    # 初始化浏览器，isWait：是否等待后续加载
    def browser_init(self, is_wait):
        # 初始化谷歌浏览器驱动参数
        options = webdriver.ChromeOptions()
        # 本地的谷歌浏览器启动地址
        options.binary_location = self.chrome_path
        prefs = {
            'profile.default_content_settings_popups': 0,
            # 文件默认下载保存地址
            'download.default_directory': self.paper_save_dir
        }
        options.add_experimental_option('prefs', prefs)
        browser = webdriver.Chrome(chrome_options=options)
        if is_wait:
            browser.implicitly_wait(10)
        return browser

    # 获取http请求头部，尽量填写页面浏览器请求时的所有Header参数
    def get_http_header(self):
        return {
            'Host': 'academic.oup.com',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'None',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'Oxford_AcademicMachineID=637702101365526898; OUP_SessionId=xtqeb5uwxgcejcuzen3byins; __gads=ID=b81be4cf09cd9e6b:T=1634613348:S=ALNI_MYULZcJ2wKMnwMvA8z87akf64aQkg; _gid=GA1.2.262735334.1634613348; SaneID=6PYkWUTWKas-cwPtchO; oup-cookie=1_19-10-2021; JSESSIONID=F6581C5500043E362B48B787FF1525FF; TheDonBot=C5A4B943CA2D082CB05BE6C64597AE91; __atuvc=35%7C42; __atuvs=616eec1e11d76f8c000; _ga_GLF90ZEMKF=GS1.1.1634656635.4.1.1634659358.0; _ga=GA1.2.1177316820.1634613348; _gat_UA-78288099-3=1',
        }

    # 将内容写入csv，a+：使用追加模式
    def write_csv(self, path, content):
        with open(path, 'a+', newline='', encoding='utf-8') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(content)



if __name__ == "__main__":
    # 初始化参数
    oxford2 = Oxford2(
        "C:\Program Files\Google\Chrome\Application\chrome.exe",
        "C:\\Users\什锦小沐\Desktop\尹豪强\oxford"

    )
    # 获取详情页链接
    oxford2.get_page_urls(1, 13)
    # 获取文档下载链接
    oxford2.get_paper_urls()
    # 下载文档
    oxford2.download_paper()

