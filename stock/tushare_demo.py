import tushare as ts
import requests

ts.set_token('095b4fa24e3eb5f2532186bea22500119b41ca09de958fa041beccb1')
# df = ts.pro_bar(ts_code='161903.SZ', adj='qfq', start_date='20210101', end_date='20210131', asset='FD')
# print(df)

res = requests.get('https://www.baidu.com')
print(res)

