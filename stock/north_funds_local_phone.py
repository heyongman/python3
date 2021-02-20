import pandas as pd
import datetime
import time
import requests

LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)


class northFunds:
    def __init__(self, security, limit, board_code=None, is_draw=True):
        self.wechat_url = 'https://sc.ftqq.com/SCU137291T1327f5bb4e61f6158d59e50c2dcb52945fdef799e88a8.send?text=%s&desp=S:%.2f  MF:%.2f H:%.2f L:%.2f'
        self.wechat_url = 'http://push.ijingniu.cn/send?key=0af43c6bcac2410d84dad3f91a18dba7&head=%s&body=S:%.2f  MF:%.2f H:%.2f L:%.2f'
        self.stock_url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get?klt=101&fqt=1&end=20500000&iscca=1&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6%2Cf7%2Cf8&fields2=f51%2Cf53&forcect=1'
        self.fund_url = 'https://push2his.eastmoney.com/api/qt/otcfund/kline/get?fields1=f1,f2,f3,f5,f6,f7&fields2=f51,f52&prd=6'
        self.north_url = 'https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_MUTUAL_DEAL_HISTORY&sty=TRADE_DATE,FUND_INFLOW,NET_DEAL_AMT&filter=(MUTUAL_TYPE%3D%22005%22)&ps=500'
        self.today_north_deal_url = 'https://push2.eastmoney.com/api/qt/kamtbs.rtmin/get?dpt=app.hsgt&fields1=f1,f3&fields2=f51,f54,f58,f62&ut=b4777e09a0311f6e0734ff19d481afb5'
        self.today_north_used_url = 'https://push2.eastmoney.com/api/qt/kamt.rtmin/get?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55,f56&ut=3b5081bd09aef3998739f9435fa5a3d2'
        self.north_board_url = 'https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_MUTUAL_BOARD_HOLDRANK&sty=TRADE_DATE,HOLD_MARKET_CAP,MAXHOLD_SECUCODE,BOARD_NAME&callback=&extraCols=&filter=(TRADE_DATE%3D%272021-02-05%27)(BOARD_TYPE%3D%222%22)(INTERVAL_TYPE%3D%221%22)&p=1&ps=10&sr=-1&st=HOLD_MARKET_CAP&source=DataCenter&client=APP'
        self.north_board_url = 'https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_MUTUAL_BOARD_HOLDRANK&sty=TRADE_DATE,ADD_MARKET_CAP,BOARD_NAME&callback=&extraCols=&filter=(INTERVAL_TYPE%3D%221%22)(BOARD_CODE%3D%22802006%22)&sr=-1,-1&st=TRADE_DATE,COMPOSITION_QUANTITY'
        self.sec_query_url = 'https://searchapi.eastmoney.com/api/Info/Search?token=CCSDCZSDCXYMYZYYSYYXSMDDSMDHHDJT&type=14&pageIndex14=1&pageSize14=100&and14=MultiMatch/Name,Code,PinYin/上证指数/true&returnfields14=Name,Code,MktNum,Classify,SecurityTypeName,ID&isAssociation14=false'
        self.window = 150
        self.board_code = board_code
        self.north_index_name = 'ADD_MARKET_CAP' if self.board_code else 'FUND_INFLOW'
        self.is_draw = is_draw
        self.security = security
        self.boll_upper = None
        self.boll_lower = None
        self.limit = limit
        self.trans_date = self.load_trans_date()  # 升序

    def load_trans_date(self):
        url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get?klt=101&fqt=1&end=20500000&iscca=1&fields1=f1&fields2=f51&forcect=1&secid=1.000300'
        res = requests.get(url, params={'lmt': self.limit}).json()['data']['klines']
        data = pd.Series(res)
        return data

    # 降序
    # TRADE_DATE  FUND_INFLOW(亿)  NET_DEAL_AMT(亿)
    # 2021-02-05        110.82          83.93
    def load_north_data(self):
        res = requests.get(url=self.north_url, params={'p': 1}).json()['result']['data']
        data = pd.DataFrame(res)
        data['FUND_INFLOW'] = data['FUND_INFLOW']/100
        data['NET_DEAL_AMT'] = data['NET_DEAL_AMT']/100
        data['TRADE_DATE'] = data['TRADE_DATE'].str[:10]
        if data['TRADE_DATE'].iloc[0] != self.trans_date.iloc[-1]:
            data.append({'TRADE_DATE': self.trans_date.iloc[-1], 'FUND_INFLOW': 1, 'NET_DEAL_AMT': 1}, ignore_index=True)
        return data

    # 亿
    def load_today_north(self):
        data = requests.get(self.today_north_deal_url).json()['data']['s2n']
        data = [x for x in data if len(x) > 15].pop()
        data = round(eval(data.split(',').pop()) / 10000, 2)
        return data

    def compute_boll(self, north_data, curr_date):
        # NET_DEAL_AMT,FUND_INFLOW
        date_name = 'TRADE_DATE'
        stdev_n = 2
        pre_data = north_data[north_data[date_name] <= curr_date]
        # 分组求和
        pre_data = pre_data.iloc[:self.window]
        if len(pre_data) < self.window:
            print('ERROR: compute_boll: length of pre_data is %s' % len(pre_data))
            return
        # print(pre_data)
        mid = pre_data[self.north_index_name].mean()
        stdev = pre_data[self.north_index_name].std()
        upper = mid + stdev_n * stdev
        lower = mid - stdev_n * stdev
        mf = pre_data[self.north_index_name].iloc[0]
        real_date = pre_data[date_name].iloc[0]
        self.boll_upper = round(upper, 2)
        self.boll_lower = round(lower, 2)
        return real_date, round(mf, 2), self.boll_upper, self.boll_lower

    def realtime_signal(self):
        if not self.boll_lower:
            curr_date = datetime.datetime.now().strftime('%Y-%m-%d')
            north_data = self.load_north_data()
            self.compute_boll(north_data, curr_date)

        while True:
            mf = self.load_today_north()
            scale = mf / self.boll_upper if mf > 0 else mf / self.boll_lower
            if scale > 0.9:
                signal = '清' if mf > 0 else '下'
                requests.get(self.wechat_url % (signal, scale, mf, self.boll_upper, self.boll_lower))
            if datetime.datetime.now().minute < 50:
                break
            time.sleep(25)

    def last_signal(self):
        # logging.info('run_morning')
        north_data = self.load_north_data()
        curr_date = datetime.datetime.now().strftime('%Y-%m-%d')
        real_date, mf, upper, lower = self.compute_boll(north_data, curr_date)
        scale = mf / upper if mf > 0 else mf / lower
        if scale > 0.9:
            signal = '清' if mf > 0 else '下'
        else:
            signal = 'Morning'
        requests.get(self.wechat_url % (signal, scale, mf, self.boll_upper, self.boll_lower))


# 2:50-3:00每25秒比对一次实时数据,满足条件通知
# 当天9:00计算boll,通知
# baijiu:0.399997/0.161725, wanjia:0.161903, xique:150.002079, nuoan:150.320007,zhongou:003096, 中小盘:150.110011
# yinliao:802006, ruanjian:802051
if __name__ == '__main__':
    northFunds = northFunds('0.161903', 1)
    northFunds.last_signal()
    # northFunds.realtime_signal()
