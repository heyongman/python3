import sys


def bknHash(skey, init_str=5381):
    hash_str = init_str
    for i in skey:
        hash_str += (hash_str << 5) + ord(i)
    hash_str = int(hash_str & 2147483647)
    return hash_str


pt_login_sig = 'OBTwVJ1iHXWm0S7RtCuzONb5mcwGRCxQTvCNY5a*0S*Bk1tXvW569aol*M3-QyAP'
print(bknHash(pt_login_sig, init_str=0))  # 379528394

py3 = sys.version_info[0] == 3
print(py3 and 1 or 2)

res = "ptuiCB('0','0','https://ptlogin2.web2.qq.com/check_sig?pttype=1&uin=545589629&service=ptqrlogin&nodirect=0&ptsigx=77106ca8a3c8e5421ab091b844f22d2b548e1058f72f8324b36a08f25ce8833473f9c2960a972ef619ada244c0ec497c605ed929d14ae90fd2237d7fa89d83fe&s_url=https%3A%2F%2Fweb2.qq.com%2Fproxy.html&f_url=&ptlang=2052&ptredirect=100&aid=501004106&daid=164&j_later=0&low_login_hour=0&regmaster=0&pt_login_type=3&pt_aid=0&pt_aaid=16&pt_light=0&pt_3rd_aid=0','0','登录成功！', '学校塌了便是晴天')"
splits = res.split(",")
print(splits[2].strip("'"))

s = "superuin=o0545589629;Path=/;Domain=ptlogin2.qq.com;"

import requests

BCOOKIES = {
    "superuin": "o0545589629",
    "Path": "/"
}
skus = ['103125239']
ssrequest = requests.session()
requests.utils.add_dict_to_cookiejar(ssrequest.cookies, BCOOKIES)
url = "http://www.xxx.com"
cookie = ssrequest.cookies
print(cookie.get("superuin")[2:])
