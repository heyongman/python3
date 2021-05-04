# from machine import Timer
# from machine import Pin
# from machine import reset
# import esp
import network
# import _thread
import utime
import ntptime
import urequests as requests
import math
# import gc
import ujson

# import requests
# import json as ujson


def do_connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('.')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            utime.sleep_ms(100)
    print('network config:', wlan.ifconfig())


def ntp_time():
    ntptime.NTP_DELTA = 3155644800
    ntptime.host = 'ntp1.aliyun.com'
    ntptime.settime()


def mean(data):
    return sum(data) / len(data)


def stdev(data, xbar=None):
    if xbar is None:
        xbar = sum(data) / len(data)
    total = total2 = 0
    for x in data:
        total += (x - xbar) ** 2
        total2 += (x - xbar)
    total -= total2 ** 2 / len(data)
    return math.sqrt(total / (len(data) - 1))


class northFunds:
    def __init__(self, security, limit, board_code=None):
        self.wechat_url = 'http://push.ijingniu.cn/send?key=0af43c6bcac2410d84dad3f91a18dba7&head=%s&body=S:%.2f  MF:%.2f H:%.2f L:%.2f'
        self.stock_url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get?klt=101&fqt=1&end=20500000&iscca=1&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6%2Cf7%2Cf8&fields2=f51%2Cf53&forcect=1&lmt=150&secid='
        self.north_url = 'https://datacenter.eastmoney.com/securities/api/data/get?p=1&ps=300&type=RPT_MUTUAL_DEAL_HISTORY&sty=TRADE_DATE,NET_DEAL_AMT&filter=(MUTUAL_TYPE%3D%22005%22)'
        self.today_north_deal_url = 'https://push2.eastmoney.com/api/qt/kamtbs.rtmin/get?dpt=app.hsgt&fields1=f1,f3&fields2=f51,f54,f58,f62&ut=b4777e09a0311f6e0734ff19d481afb5'
        self.north_board_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssl_bkzj_zjlrqs?sort=opendate&asc=0&page=1&num=50&bankuai=0%2F'
        self.window = 150
        self.board_code = board_code
        self.lose_limit = -0.14 if self.board_code == '0/new_dzqj' else -0.1
        self.buy_limit = 0.82 if self.board_code == '0/new_dzqj' else 0.9
        self.sell_limit = 1 if self.board_code == '0/new_dzqj' else 1.3
        self.north_index_name = 'ADD_MARKET_CAP' if self.board_code else 'NET_DEAL_AMT'
        self.security = security
        self.boll_upper = None
        self.boll_lower = None
        self.limit = limit
        self.full = False
        self.last_order_date = None
        self.init = False

    # 降序
    # {'2021-02-05': 83.93,,,}
    def load_north_data(self):
        res = requests.get(url=self.north_url)
        res = ujson.loads(res.read())['result']['data']
        res = {x.get('TRADE_DATE')[:10]: x.get('NET_DEAL_AMT') / 100 for x in res}
        return res

    # 降序
    # [('2021-02-05', 83.93),,,]
    def load_board_data(self):
        data = []
        for i in range(1, 6):
            res = requests.get(self.north_board_url.replace('page=1', 'page=' + str(i)) + self.board_code)
            res = ujson.loads(res.read())
            data += [(x.get('opendate'), eval(x.get('r0_net')) / 100000000) for x in res]
        return data

    # 升序
    # [['2020-09-16', '1.568'],,,]
    def load_close_data(self):
        res = requests.get(url=self.stock_url + self.security)
        res = ujson.loads(res.read())['data']['klines']
        res = [x.split(',') for x in res]
        return res

    # total_fund(降序): ('2021-01-01', 65)
    def compute_boll(self, date, total_fund):
        stdev_n = 2
        # 小于当前日期的资金列表
        pre_data = [x[1] for x in total_fund if x[0] < date]
        # 分组求和
        if len(pre_data) < self.window:
            print('ERROR: compute_boll: length of pre_data is %s' % len(pre_data))
            return
        mid = mean(pre_data)
        std = stdev(pre_data, mid)
        upper = mid + stdev_n * std
        lower = mid - stdev_n * std
        mf = pre_data[0]
        self.boll_upper = round(upper, 2)
        self.boll_lower = round(lower, 2)
        return round(mf, 2), self.boll_upper, self.boll_lower

    def action_compute(self, curr_date, total_fund, close_data):
        mf, upper, lower = self.compute_boll(curr_date, total_fund)
        action = None
        if mf > 0 and mf / upper > self.buy_limit and not self.full:
            action = 'buy'
            self.full = True
            self.last_order_date = curr_date
        elif mf < 0 and mf / lower > self.sell_limit and self.full:
            self.full = False
            action = 'sell'

        #  强制平仓
        if self.full:
            ordered_window = [eval(x[1]) for x in close_data if self.last_order_date <= x[0] <= curr_date]
            window_start = ordered_window[0]
            widow_end = ordered_window[-1]
            lose_rate = (widow_end - max(ordered_window)) / window_start
            if lose_rate < self.lose_limit:
                print('close', curr_date, lose_rate)
                self.full = False
                action = 'close'
        return action

    def run(self):
        north_data = self.load_north_data()
        # gc.collect()
        close_data = self.load_close_data()
        # gc.collect()
        board_data = self.load_board_data()
        # gc.collect()
        # 合并金额
        total_fund = []
        for x, y in board_data:
            north = north_data.get(x)
            north = 0 if not north else north
            fund = y + 1.5 * north
            total_fund.append((x, round(fund, 2)))

        # 初始化
        if self.init:
            close_data = close_data[-1:]
        else:
            self.init = True
        for x in close_data:
            curr_date = x[0]
            action = self.action_compute(curr_date, total_fund, close_data)
            if action:
                print(curr_date, action)
            # 今天的上一个交易日有操作
            if curr_date == close_data[-1][0] and action:
                print('当日操作', curr_date, action)


# 当天为上一天的数据
# baijiu:0.399997/0.161725, wanjia:0.161903, xique:150.002079, nuoan:150.320007,zhongou:003096, 中小盘:150.110011
if __name__ == '__main__':
    do_connect('ziroom3004-1', '4001001111')
    ntp_time()
    northFunds = northFunds('0.161903', 150, board_code='new_dzqj')
    # northFunds.board_code = '0/new_dzqj'  # new_ljhy new_dzqj
    northFunds.run()
