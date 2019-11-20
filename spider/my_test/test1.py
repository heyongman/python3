import os
import requests
import ping3

# url = "https://drive.google.com/uc?authuser=0&id=0B0uaIHNp_zaqV21JNmNldXR1bU0&export=download"
proxies = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
}

server = ["107.170.197.213",
          "142.93.88.37"
          ]

server_delay = {}
for s in server:
    t = ping3.ping(s, timeout=1)
    if not t:
        t = 1
    server_delay.setdefault(s, t)

a = sorted(server_delay.items(), key=lambda x: x[1])

print(a)

# for k, v in server_delay.items():
#     print(k, v)
url = "https://www.google.com"
res = requests.get(url, timeout=10, proxies=proxies)

# with open("D:\\test_file") as f:
#     f.write(res)
#     f.close()
