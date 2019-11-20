# -*- coding:utf-8 -*-

import os
import re
import time
import sys
import subprocess
import requests
import xml.dom.minidom
import json
import random
import traceback


class QQLogin(object):
    def __init__(self):
        self.session = requests.session()
        self.session.headers.update({
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9;'
                           ' rv:27.0) Gecko/20100101 Firefox/27.0'),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })
        self.QRImgPath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + 'qr.PNG'
        self.pt_login_sig = ''
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

    def main(self):

        if not self.get_pt_login_sig():
            print('获取login_sig失败')
            return

        self.showQRImage()

        while self.checkLogin() != '200':
            pass

        # os.remove(self.QRImgPath)

        # if not self.login():
        #     print('登录失败')
        #     return

    def get_pt_login_sig(self):
        # https://xui.ptlogin2.qq.com/cgi-bin/xlogin
        url = 'https://ui.ptlogin2.qq.com/cgi-bin/login'
        params = {
            'appid': '501004106',
            'daid': '164',
            'enable_qlogin': '0',
            'f_url': 'loginerroralert',
            'login_state': '10',
            'mibao_css': 'm_webqq',
            'no_verifyimg': '1',
            'pt_disable_pwd': '1',
            's_url': 'https://web2.qq.com/proxy.html',
            'strong_login': '1',
            'style': '40',
            't': '20131024001',
            'target': 'self'
        }

        response = self.session.get(url, params=params)
        self.cookies = response.cookies
        header = response.headers
        pattern = r'pt_login_sig=(\S+);'
        try:
            self.pt_login_sig = re.search(pattern, str(header)).group(1)
            return True
        except Exception:
            print(traceback.format_exc())
            return False

    def showQRImage(self):
        # https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=2&l=M&s=3&d=72&v=4&t=0.2587821381860622&daid=164&pt_3rd_aid=0
        url = 'https://ssl.ptlogin2.qq.com/ptqrshow'
        params = {
            'appid': '501004106',
            'e': '2',
            'l': 'M',
            's': '3',
            'd': '72',
            'v': '4',
            't': str(random.random())[0:18],
            'daid': '164',
            'pt_3rd_aid': '0'
        }
        response = self.session.get(url, params=params)

        with open(self.QRImgPath, 'wb') as f:
            f.write(response.content)
            f.close()
        # 打开二维码
        if sys.platform.find('darwin') >= 0:
            subprocess.call(['open', self.QRImgPath])  # 苹果系统
        elif sys.platform.find('linux') >= 0:
            subprocess.call(['xdg-open', self.QRImgPath])  # linux系统
        else:
            os.startfile(self.QRImgPath)  # windows系统

        print('请使用QQ扫描二维码登录')

    def checkLogin(self):
        time.sleep(3)
        # url = 'https://ssl.ptlogin2.qq.com/ptqrlogin'
        url = 'https://ssl.ptlogin2.qq.com/ptqrlogin?ptqrtoken='
        str(bknHash(self.cookies.get('qrsig'), init_str=0))
        '&webqq_type=10&remember_uin=1&login2qq=1&aid=501004106'
        '&u1=http%3A%2F%2Fw.qq.com%2Fproxy.html%3Flogin2qq%3D1%26'
        'webqq_type%3D10&ptredirect=0&ptlang=2052&daid=164&'
        'from_ui=1&pttype=1&dumy=&fp=loginerroralert&action=0-0-'
        repr(random.random() * 900000 + 1000000)
        '&mibao_css=m_webqq&t=undefined&g=1&js_type=0'
        '&js_ver=10141&login_sig=%s&pt_randsalt=0'

        params = {
            'u1': 'https://web2.qq.com/proxy.html',
            'ptqrtoken': +bknHash(self.session.cookies.get('qrsig'), init_str=0),
            'ptredirect': '0',
            'h': '1',
            't': '1',
            'g': '1',
            'from_ui': '1',
            'ptlang': '2052',
            'action': '0-0-'+str(int(time.time()*1000)),
            'js_ver': '10282',
            'js_type': '1',
            'login_sig': self.pt_login_sig,
            'pt_uistyle': '40',
            'aid': '501004106',
            'daid': '164',
            'mibao_css': 'm_webqq'
        }
        self.session.headers.update({'Referer': 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?daid=164&target=self&style=40&pt_disable_pwd=1&mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=https%3A%2F%2Fweb2.qq.com%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001'})
        print(self.session.headers)
        response = self.session.get(url)
        target = response.content.decode('utf-8')
        print(target)
        if '二维码未失效' in target:
            return '202'
        elif '二维码已失效' in target:
            return '203'
        elif '登录成功' in target:
            return '200'
        else:
            return '201'


def qHash(x, K):
    N = [0] * 4
    for T in range(len(K)):
        N[T % 4] ^= ord(K[T])

    U, V = 'ECOK', [0] * 4
    V[0] = ((x >> 24) & 255) ^ ord(U[0])
    V[1] = ((x >> 16) & 255) ^ ord(U[1])
    V[2] = ((x >> 8) & 255) ^ ord(U[2])
    V[3] = ((x >> 0) & 255) ^ ord(U[3])

    U1 = [0] * 8
    for T in range(8):
        U1[T] = N[T >> 1] if T % 2 == 0 else V[T >> 1]

    N1, V1 = '0123456789ABCDEF', ''
    for aU1 in U1:
        V1 += N1[((aU1 >> 4) & 15)]
        V1 += N1[((aU1 >> 0) & 15)]

    return V1


def bknHash(skey, init_str=5381):
    hash_str = init_str
    for i in skey:
        hash_str += (hash_str << 5) + ord(i)
    hash_str = int(hash_str & 2147483647)
    return hash_str


if __name__ == '__main__':
    print('开始')
    qq = QQLogin()
    qq.main()
