import os
import re
import time
import sys
import subprocess
import requests
import xml.dom.minidom
from bs4 import BeautifulSoup
import json


class LiuZhi(object):
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'}
        self.QRImgPath = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'webQr.jpg'
        self.uuid = ''
        self.tip = 0
        self.base_uri = ''
        self.redirect_uri = ''
        self.skey = ''
        self.wxsid = ''
        self.wxuin = ''
        self.pass_ticket = ''
        self.deviceId = 'e000000000000000'
        self.BaseRequest = {}
        self.ContactList = []
        self.My = []
        self.SyncKey = ''

    def login(self):
        self.base_uri = 'http://jw.lzzy.net/st/login.aspx'
        data = {
            '__VIEWSTATE': '/wEPDwUJOTYxNDY3OTc0D2QWAgIBD2QWBAIBDw8WBB4JQmFja0NvbG9yCfPQANAeBF8hU0ICCGRkAgcPEGQPFgECARYBBQnovoXlr7zlkZhkZBgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAQUNQnV0dG9uX+eZu+mZhnMNcR0lmESxFiRZBM9v+ge1afmn',
            '__VIEWSTATEGENERATOR': 'D2D9F043',
            '__EVENTVALIDATION': '/wEWCQKksLT7BQLep8vjCAKu8uE5AvKm2soEAvLJzeAMAvWZ8TkC6fHPnw8CwsjN4QICyKiipgHVGPoy3AjhpfHxMai6zxnc2XoWVA==',
            'Rad_角色': '学生',
            'txt_卡学号': '20153122',
            'txt_密码': 'ghjkklml'
        }
        response = self.session.post(self.base_uri, data=data, verify=False)
        data = response.content.decode('utf-8')
        print(data)

        html = BeautifulSoup(data, 'html.parser')

        # print(html.select('title'))

        return True

    def get_title(self):
        self.redirect_uri = 'https://www.lzzy.net/xwzx/xww/xyyw/content_44282'
        response = self.session.get(self.redirect_uri, verify=False)
        data = response.content.decode('utf-8')
        # print(data)
        html = BeautifulSoup(data, 'html.parser')

        print(html.select('title'))

    def main(self):
        if not self.login():
            print('登录失败')
            return


if __name__ == '__main__':
    liuzhi = LiuZhi()
    liuzhi.main()
