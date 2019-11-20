# -*- coding: utf-8 -*-

import sys, os
# p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# if p not in sys.path:
#     sys.path.insert(0, p)

import random, pickle, time, requests, subprocess, json

from urllib3.exceptions import RequestError
from qq.facemap import FaceParse, FaceReverseParse
from qq.common import PY3, Partition, JsonLoads, JsonDumps


class BasicQSession(object):

    def Login(self, ):
        self.prepareSession()
        self.waitForAuth()
        self.getPtwebqq()
        self.getVfwebqq()
        self.getUinAndPsessionid()
        self.TestLogin()

    def prepareSession(self):
        self.clientid = 53999199
        self.msgId = 6000000
        self.lastSendTime = 0
        self.QRImgPath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + 'qr.PNG'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9;'
                           ' rv:27.0) Gecko/20100101 Firefox/27.0'),
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

    def getQrcode(self):
        qrcode = self.urlGet(
            'https://ssl.ptlogin2.qq.com/ptqrshow?appid=501004106&e=0&l=M&' +
            's=5&d=72&v=4&t=' + repr(random.random())
        ).content
        print('已获取二维码')
        return qrcode

    def waitForAuth(self):
        # qrcodeManager = QrcodeManager(conf)
        try:
            print(self.getQrcode())
            x, y = 1, 1
            while True:
                time.sleep(3)
                authStatus = self.getAuthStatus()
                print(authStatus)
                if '二维码未失效' in authStatus:
                    if x:
                        print('等待二维码扫描及授权...')
                        x = 0
                elif '二维码认证中' in authStatus:
                    if y:
                        print('二维码已扫描，等待授权...')
                        y = 0
                elif '二维码已失效' in authStatus:
                    print('二维码已失效, 重新获取二维码')
                    # qrcodeManager.Show(self.getQrcode())
                    x, y = 1, 1
                elif '登录成功' in authStatus:
                    print('已获授权')
                    items = authStatus.split(',')
                    self.nick = str(items[-1].split("'")[1])
                    self.qq = str(int(self.session.cookies.get('superuin')[1:]))
                    self.urlPtwebqq = items[2].strip().strip("'")
                    # t = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
                    # self.dbbasename = '%s-%s-contact.db' % (t, self.qq)
                    # self.dbname = conf.absPath(self.dbbasename)
                    # conf.SetQQ(self.qq)
                    break
                else:
                    print('获取二维码扫描状态时出错, html="%s"', authStatus)
                    sys.exit(1)
        finally:
            print("destory")
            # qrcodeManager.Destroy()

    def getAuthStatus(self):
        # by @zofuthan
        url = 'https://ssl.ptlogin2.qq.com/ptqrlogin'
        params = {
            'u1': 'https://web2.qq.com/proxy.html',
            'ptqrtoken': +bknHash(self.session.cookies.get('qrsig'), init_str=0),
            'ptredirect': '0',
            'h': '1',
            't': '1',
            'g': '1',
            'from_ui': '1',
            'ptlang': '2052',
            'action': '0-0-' + str(int(time.time() * 1000)),
            'js_ver': '10282',
            'js_type': '1',
            'login_sig': self.session.cookies.get('pt_login_sig'),
            'pt_uistyle': '40',
            'aid': '501004106',
            'daid': '164',
            'mibao_css': 'm_webqq'
        }
        result = self.urlGet(
            url=url,
            params=params,
            Referer=('https://xui.ptlogin2.qq.com/cgi-bin/xlogin?daid=164&target=self&style=40&pt_disable_pwd=1&'
                     'mibao_css=m_webqq&appid=501004106&enable_qlogin=0&no_verifyimg=1&s_url=https%3A%2F%2Fweb2.qq.com'
                     '%2Fproxy.html&f_url=loginerroralert&strong_login=1&login_state=10&t=20131024001')
        ).content
        return result.decode('utf8')

    def showQRImage(self):
        with open(self.QRImgPath, 'wb') as f:
            f.write(self.getQrcode())
            f.close()

        # 打开二维码
        if sys.platform.find('darwin') >= 0:
            subprocess.call(['open', self.QRImgPath])  # 苹果系统
        elif sys.platform.find('linux') >= 0:
            subprocess.call(['xdg-open', self.QRImgPath])  # linux系统
        else:
            os.startfile(self.QRImgPath)  # windows系统

        print('请使用QQ扫描二维码登录')

    def getPtwebqq(self):
        self.urlGet(self.urlPtwebqq)
        self.ptwebqq = self.session.cookies['ptwebqq']
        print('已获取ptwebqq')

    def getVfwebqq(self):
        self.vfwebqq = self.smartRequest(
            url=('http://s.web2.qq.com/api/getvfwebqq?ptwebqq=%s&'
                 'clientid=%s&psessionid=&t={rand}') %
                (self.ptwebqq, self.clientid),
            Referer=('http://s.web2.qq.com/proxy.html?v=20130916001'
                     '&callback=1&id=1'),
            Origin='http://s.web2.qq.com'
        )['vfwebqq']
        print('已获取vfwebqq')

    def getUinAndPsessionid(self):
        result = self.smartRequest(
            url='http://d1.web2.qq.com/channel/login2',
            data={
                'r': JsonDumps({
                    'ptwebqq': self.ptwebqq, 'clientid': self.clientid,
                    'psessionid': '', 'status': 'online'
                })
            },
            Referer=('http://d1.web2.qq.com/proxy.html?v=20151105001'
                     '&callback=1&id=2'),
            Origin='http://d1.web2.qq.com'
        )
        self.uin = result['uin']
        self.psessionid = result['psessionid']
        self.hash = qHash(self.uin, self.ptwebqq)
        self.bkn = bknHash(self.session.cookies['skey'])
        print('已获取uin和psessionid')

    def TestLogin(self):
        # if not self.session.verify:
        #     disableInsecureRequestWarning()
        try:
            # DisableLog()
            # 请求一下 get_online_buddies 页面，避免103错误。
            # 若请求无错误发生，则表明登录成功
            self.smartRequest(
                url=('http://d1.web2.qq.com/channel/get_online_buddies2?'
                     'vfwebqq=%s&clientid=%d&psessionid=%s&t={rand}') %
                    (self.vfwebqq, self.clientid, self.psessionid),
                Referer=('http://d1.web2.qq.com/proxy.html?v=20151105001&'
                         'callback=1&id=2'),
                Origin='http://d1.web2.qq.com',
                repeatOnDeny=0
            )
        except Exception:
            print("error")
        # finally:
            # EnableLog()

        print('登录成功。登录账号：%s(%s)', self.nick, self.qq)

    def Poll(self):
        try:
            result = self.smartRequest(
                url='https://d1.web2.qq.com/channel/poll2',
                data={
                    'r': JsonDumps({
                        'ptwebqq': self.ptwebqq, 'clientid': self.clientid,
                        'psessionid': self.psessionid, 'key': ''
                    })
                },
                Referer=('http://d1.web2.qq.com/proxy.html?v=20151105001&'
                         'callback=1&id=2'),
                expectedCodes=(0, 100003, 100100, 100012)
            )
            # "{'retcode': 0, 'retmsg': 'ok', 'errmsg': 'error'}"
            if type(result) is dict and \
                    result.get('retcode', 1) == 0 and \
                    result.get('errmsg', '') == 'error':
                print(result)
                raise RequestError
        except RequestError:
            print('接收消息出错，开始测试登录 cookie 是否过期...')
            try:
                self.TestLogin()
            except RequestError:
                print('登录 cookie 很可能已过期')
                raise
            else:
                print('登录 cookie 尚未过期')
                return 'timeout', '', '', ''
        else:
            if (not result) or (not isinstance(result, list)):
                print(result)
                return 'timeout', '', '', ''
            else:
                result = result[0]
                ctype = {
                    'message': 'buddy',
                    'group_message': 'group',
                    'discu_message': 'discuss'
                }[result['poll_type']]
                fromUin = str(result['value']['from_uin'])
                memberUin = str(result['value'].get('send_uin', ''))
                content = FaceReverseParse(result['value']['content'])
                return ctype, fromUin, memberUin, content

    def send(self, ctype, uin, content, epCodes=[0]):
        self.msgId += 1
        sendUrl = {
            'buddy': 'http://d1.web2.qq.com/channel/send_buddy_msg2',
            'group': 'http://d1.web2.qq.com/channel/send_qun_msg2',
            'discuss': 'http://d1.web2.qq.com/channel/send_discu_msg2'
        }
        sendTag = {'buddy': 'to', 'group': 'group_uin', 'discuss': 'did'}
        self.smartRequest(
            url=sendUrl[ctype],
            data={
                'r': JsonDumps({
                    sendTag[ctype]: int(uin),
                    'content': JsonDumps(
                        FaceParse(content) +
                        [['font', {'name': '宋体', 'size': 10,
                                   'style': [0, 0, 0], 'color': '000000'}]]
                    ),
                    'face': 522,
                    'clientid': self.clientid,
                    'msg_id': self.msgId,
                    'psessionid': self.psessionid
                })
            },
            Referer=('http://d1.web2.qq.com/proxy.html?v=20151105001&'
                     'callback=1&id=2'),
            expectedCodes=epCodes
        )

    def SendTo(self, contact, content, resendOn1202=True):
        result = None

        if not hasattr(contact, 'ctype'):
            result = '错误：消息接受者必须为一个 QContact 对象'

        if contact.ctype.endswith('-member'):
            result = '错误：不能给群成员或讨论组成员发消息'

        if PY3:
            if isinstance(content, str):
                content = content
            elif isinstance(content, bytes):
                content = content.decode('utf8')
            else:
                result = '错误：消息内容必须为 str 或 bytes 对象'
        else:
            if isinstance(content, str):
                content = content
            elif isinstance(content, unicode):
                content = content.encode('utf8')
            else:
                result = '错误：消息内容必须为 str 或 unicode 对象'

        if not content:
            result = '错误：不允许发送空消息'

        if result:
            print(result)
            return result

        epCodes = resendOn1202 and [0] or [0, 1202]

        result = '向 %s 发消息成功' % contact
        while content:
            front, content = Partition(content)
            try:
                self.send(contact.ctype, contact.uin, front, epCodes)
            except Exception as e:
                result = '错误：向 %s 发消息失败 %s' % (str(contact), e)
                print(result)
                break
            else:
                print('%s：%s' % (result, front))
        return result

    def smartRequest(self, url, data=None, Referer=None, Origin=None,
                     expectedCodes=(0, 100003, 100100), expectedKey=None,
                     timeoutRetVal=None, repeatOnDeny=2):
        nCE, nTO, nUE, nDE = 0, 0, 0, 0
        while True:
            url = url.format(rand=repr(random.random()))
            html = ''
            errorInfo = ''
            try:
                resp = self.urlGet(url, data, Referer, Origin)
            except (requests.ConnectionError,
                    requests.exceptions.ReadTimeout) as e:
                nCE += 1
                errorInfo = '网络错误 %s' % e
            else:
                html = resp.content if not PY3 else resp.content.decode('utf8')
                if resp.status_code in (502, 504, 404):
                    self.session.get(
                        ('http://pinghot.qq.com/pingd?dm=w.qq.com.hot&'
                         'url=/&hottag=smartqq.im.polltimeout&hotx=9999&'
                         'hoty=9999&rand=%s') % random.randint(10000, 99999)
                    )
                    if url == 'https://d1.web2.qq.com/channel/poll2':
                        return {'errmsg': ''}
                    nTO += 1
                    errorInfo = '超时'
                else:
                    try:
                        rst = JsonLoads(html)
                    except ValueError:
                        nUE += 1
                        errorInfo = ' URL 地址错误'
                    else:
                        result = rst.get('result', rst)

                        if expectedKey:
                            if expectedKey in result:
                                return result
                        else:
                            if 'retcode' in rst:
                                retcode = rst['retcode']
                            elif 'errCode' in rst:
                                retcode = rst['errCode']
                            elif 'ec' in rst:
                                retcode = rst['ec']
                            else:
                                retcode = -1

                            if (retcode in expectedCodes):
                                return result

                        nDE += 1
                        errorInfo = '请求被拒绝错误'

            n = nCE + nTO + nUE + nDE

            if len(html) > 40:
                html = html[:20] + '...' + html[-20:]

            # 出现网络错误、超时、 URL 地址错误可以多试几次
            # 若网络没有问题但 retcode 有误，一般连续 3 次都出错就没必要再试了
            if nCE < 5 and nTO < 20 and nUE < 5 and nDE <= repeatOnDeny:
                print('第%d次请求“%s”时出现 %s，html=%s',
                      n, url.split('?', 1)[0], errorInfo, repr(html))
                time.sleep(0.5)
            elif nTO == 20 and timeoutRetVal:  # by @killerhack
                return timeoutRetVal
            else:
                print('第%d次请求“%s”时出现 %s, html=%s',
                      n, url.split('?', 1)[0], errorInfo, repr(html))
                raise RequestError

    def urlGet(self, url, params=None, data=None, Referer=None, Origin=None):
        Referer and self.session.headers.update({'Referer': Referer})
        Origin and self.session.headers.update({'Origin': Origin})
        timeout = 30 if url != 'https://d1.web2.qq.com/channel/poll2' else 120

        try:
            if data is None:
                return self.session.get(url, params=params, timeout=timeout)
            else:
                return self.session.post(url, params=params, data=data, timeout=timeout)
        except (requests.exceptions.SSLError, AttributeError):
            # by @staugur, @pandolia
            if self.session.verify:
                time.sleep(5)
                print('无法和腾讯服务器建立私密连接，'
                      ' 5 秒后将尝试使用非私密连接和腾讯服务器通讯。'
                      '若您不希望使用非私密连接，请按 Ctrl+C 退出本程序。')
                try:
                    time.sleep(5)
                except KeyboardInterrupt:
                    # Put(sys.exit, 0)
                    sys.exit(0)
                print('开始尝试使用非私密连接和腾讯服务器通讯。')
                self.session.verify = False
                # disableInsecureRequestWarning()
                return self.urlGet(url, params, data, Referer, Origin)
            else:
                raise


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
