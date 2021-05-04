import pandas as pd
import datetime
import time
import pyecharts.options as opts
from pyecharts.charts import Line
import requests
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

LOG_FORMAT = "%(levelname)s - %(asctime)s - %(message)s"
logging.basicConfig(filename='D:/tmp/apscheduler.log', level=logging.INFO, format=LOG_FORMAT)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)


def mark_fun(date, action, return_rate, mark_list):
    if action == 'buy':
        mark_list.append(opts.MarkPointItem(name="", coord=[date, return_rate], value=return_rate, itemstyle_opts=opts.ItemStyleOpts(color='#FF0000')))
    elif action == 'sell':
        mark_list.append(opts.MarkPointItem(name="", coord=[date, return_rate], value=return_rate, itemstyle_opts=opts.ItemStyleOpts(color='#008000')))
    elif action == 'close':
        mark_list.append(opts.MarkPointItem(name="", coord=[date, return_rate], value=return_rate, itemstyle_opts=opts.ItemStyleOpts(color='#0000FF')))
    else:
        mark_list.append(opts.MarkPointItem(name="", coord=[date, return_rate], value=return_rate, itemstyle_opts=opts.ItemStyleOpts(color='#FFA500')))

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
        self.north_board_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssl_bkzj_zjlrqs?sort=opendate&asc=0'
        self.sec_query_url = 'https://searchapi.eastmoney.com/api/Info/Search?token=CCSDCZSDCXYMYZYYSYYXSMDDSMDHHDJT&type=14&pageIndex14=1&pageSize14=100&and14=MultiMatch/Name,Code,PinYin/上证指数/true&returnfields14=Name,Code,MktNum,Classify,SecurityTypeName,ID&isAssociation14=false'
        self.window = 150
        self.board_code = board_code
        self.lose_limit = -0.14 if self.board_code == '0/new_dzqj' else -0.1
        self.buy_limit = 0.82 if self.board_code == '0/new_dzqj' else 0.9
        self.sell_limit = 1 if self.board_code == '0/new_dzqj' else 1.3
        self.north_index_name = 'ADD_MARKET_CAP' if self.board_code else 'NET_DEAL_AMT'
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

    def query_security(self, sec):
        res = requests.get(url=self.sec_query_url.replace('上证指数', sec)).json()['Data']
        return pd.DataFrame(res)

    # 降序
    # TRADE_DATE  FUND_INFLOW(亿)  NET_DEAL_AMT(亿)
    # 2021-02-05        110.82          83.93
    def load_north_data(self):
        res1 = requests.get(url=self.north_url, params={'p': 1}).json()['result']['data']
        res2 = requests.get(url=self.north_url, params={'p': 2}).json()['result']['data']
        res3 = requests.get(url=self.north_url, params={'p': 3}).json()['result']['data']
        if res1[0]['TRADE_DATE'][:10] != self.trans_date.iloc[-1]:
            res = [{'TRADE_DATE': self.trans_date.iloc[-1], 'FUND_INFLOW': self.load_today_north()*100, 'NET_DEAL_AMT': 100}] + res1 + res2 + res3
        else:
            res = res1 + res2 + res3
        data = pd.DataFrame(res)
        data['FUND_INFLOW'] = data['FUND_INFLOW']/100
        data['NET_DEAL_AMT'] = data['NET_DEAL_AMT']/100
        data['TRADE_DATE'] = data['TRADE_DATE'].str[:10]
        if data['TRADE_DATE'].iloc[0] != self.trans_date.iloc[-1]:
            data.append({'TRADE_DATE': self.trans_date.iloc[-1], 'FUND_INFLOW': 1, 'NET_DEAL_AMT': 1}, ignore_index=True)
        return data

    #       date  close
    # 2020-06-29  0.979
    # 2020-06-30  0.992
    # prd: 1,2,4,5,6,8 -> 3月，6月，1年，3年，5年，成立来
    def load_k_data(self):
        params = {
            'secid': self.security,
            'lmt': self.limit + 10,
        }
        url = self.stock_url if self.security.split('.')[0] != '150' else self.fund_url
        res = requests.get(url=url, params=params).json()['data']['klines'][-self.limit-10:]
        data = pd.DataFrame(res, columns=['klines'])
        # print(data)
        data = data['klines'].str.split(',', expand=True)
        data.columns = ['date', 'close']
        data['close'] = data['close'].astype('float')
        # 过滤掉trans date以外的数据
        data = pd.DataFrame(self.trans_date[-self.limit:], columns=['date']).merge(data, how='left', on='date')
        return data

    # 亿
    def load_today_north(self):
        data = requests.get(self.today_north_deal_url).json()['data']['s2n']
        data = [x for x in data if len(x) > 15].pop()
        data = round(eval(data.split(',').pop()) / 10000, 2)
        return data

    def load_board_hold(self):
        params = {
            'page': 1,
            'num': self.limit + self.window,
            'bankuai': self.board_code
        }
        data = requests.get(self.north_board_url, params=params).json()
        data = pd.DataFrame(data)
        data.rename(columns={'opendate': 'TRADE_DATE', 'r0_net': 'ADD_MARKET_CAP'}, inplace=True)
        data['ADD_MARKET_CAP'] = data['ADD_MARKET_CAP'].apply(lambda x: round(eval(x)/100000000, 2))
        data = data[['TRADE_DATE', 'ADD_MARKET_CAP']]
        return data

    # 降序
    # 交易日期    ,增持市值       ,板块名
    # TRADE_DATE,ADD_MARKET_CAP,BOARD_NAME
    # 2021-02-05,13.61         ,饮料
    def load_north_board_hold(self):
        params = {
            'p': 1,
            'ps': self.limit + self.window
        }
        data = requests.get(self.north_board_url.replace('802006', self.board_code), params=params).json()['result']['data']
        data = pd.DataFrame(data)
        data['TRADE_DATE'] = data['TRADE_DATE'].apply(lambda x: x[:10])
        data['ADD_MARKET_CAP'] = data['ADD_MARKET_CAP'].apply(lambda x: round(x/100000000, 2))
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
        mid = pre_data[self.north_index_name].mean()
        stdev = pre_data[self.north_index_name].std()
        upper = mid + stdev_n * stdev
        lower = mid - stdev_n * stdev
        mf = pre_data[self.north_index_name].iloc[0]
        real_date = pre_data[date_name].iloc[0]
        self.boll_upper = round(upper, 2)
        self.boll_lower = round(lower, 2)
        return real_date, round(mf, 2), self.boll_upper, self.boll_lower

    def draw_boll(self):
        north_data = self.load_board_hold() if self.board_code else self.load_north_data()
        north_data = north_data.merge(self.load_north_data(), how='left', on='TRADE_DATE')
        north_data['ADD_MARKET_CAP'] = north_data['ADD_MARKET_CAP'] + north_data['NET_DEAL_AMT']*1.5
        # print(north_data)
        k_data = self.load_k_data()
        boll_list = []
        mark_list = []
        full = False
        trans_date_slice = self.trans_date[-self.limit:]
        for curr_date in trans_date_slice:
            # north holiday not update,keep last value
            real_date, mf, upper, lower = self.compute_boll(north_data, curr_date)
            # if curr_date != real_date:
            #     mf = 0.0
            # 这里先添加full，所以计算boll时为小于等于当前日期（计算收益是根据full来的，相当于今天知道结果，明天才能操作）
            boll_list.append([curr_date, mf, upper, lower, full])

            if mf > 0 and mf / upper > self.buy_limit and not full:
                full = True
                mark_list.append([curr_date, 'buy'])
            elif mf < 0 and mf / lower > self.sell_limit and full:
                full = False
                mark_list.append([curr_date, 'sell'])
            #     强制平仓
            if full:
                last_order_date = mark_list[-1][0]
                ordered_window = k_data[(k_data['date'] <= curr_date) & (k_data['date'] >= last_order_date)]['close']
                window_start = ordered_window.iloc[0]
                widow_end = ordered_window.iloc[-1]
                lose_rate = (widow_end - ordered_window.max())/window_start
                if lose_rate < self.lose_limit:
                    print(curr_date, lose_rate)
                    full = False
                    mark_list.append([curr_date, 'close'])

        date_df = pd.DataFrame(trans_date_slice, columns=['date'])
        boll_df = pd.DataFrame(boll_list, columns=['date', 'mf', 'upper', 'lower', 'full'])
        mark_df = pd.DataFrame(mark_list, columns=['date', 'mark'])
        # mark_df['mark'] = ''

        merged_df = date_df\
            .merge(boll_df, how='left', on='date')\
            .merge(k_data, how='left', on='date')\
            .merge(mark_df, how='left', on='date')
        merged_df['close'].fillna(method='ffill', inplace=True)  # ffill bfill -> 前填充 后填充
        merged_df['close'].fillna(method='bfill', inplace=True)  # ffill bfill -> 前填充 后填充

        first = merged_df['close'].iloc[0]
        merged_df['last_close'] = merged_df['close'].shift(1)
        merged_df['inc_net'] = merged_df.apply(lambda x: x.close - x.last_close if x.full else 0, axis=1)
        merged_df['return_rate'] = merged_df['inc_net'].cumsum() * 100 / first
        merged_df['bench'] = (merged_df['close'] - first) * 100 / first
        # merged_df['diff'] = merged_df['return_rate'] - merged_df['bench']
        merged_df = merged_df.round({'return_rate': 1, 'bench': 1})
        mark_opts = []
        merged_df.dropna(subset=['mark']).apply(lambda x: mark_fun(x.date, x.mark, x.return_rate, mark_opts), axis=1)
        markpoint_opts = opts.MarkPointOpts(data=mark_opts, symbol_size=25, label_opts=opts.LabelOpts(position="inside", color="#fff", font_size=6))
        merged_df.drop(columns=['full', 'mark', 'inc_net'])
        print(merged_df)

        multi_line = (
            Line()
            .add_xaxis(merged_df['date'].tolist())
            .add_yaxis('return_rate', merged_df['return_rate'].tolist(), is_symbol_show=False, markpoint_opts=markpoint_opts, yaxis_index=0, linestyle_opts=opts.LineStyleOpts(color='#FF0000'))
            .add_yaxis('bench', merged_df['bench'].tolist(), is_symbol_show=False, yaxis_index=0, linestyle_opts=opts.LineStyleOpts(color='#CD5C5C'))
            .extend_axis(yaxis=opts.AxisOpts(type_="value", name="MF", position="right", ))
            .add_yaxis('mf', merged_df['mf'].tolist(), is_symbol_show=False, yaxis_index=1, linestyle_opts=opts.LineStyleOpts(color='#D3D3D3'))
            .add_yaxis('upper', merged_df['upper'].tolist(), is_symbol_show=False, yaxis_index=1, linestyle_opts=opts.LineStyleOpts(color='#D3D3D3'))
            .add_yaxis('lower', merged_df['lower'].tolist(), is_symbol_show=False, yaxis_index=1, linestyle_opts=opts.LineStyleOpts(color='#D3D3D3'))
            .set_global_opts(
                xaxis_opts=opts.AxisOpts(is_scale=True),
                yaxis_opts=opts.AxisOpts(type_="value", name="Rate", position="left"),
                tooltip_opts=opts.TooltipOpts(trigger='axis'),
                datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%", range_start=90, range_end=100)]
            )
            .render('north_funds.html')
        )

        # close_line = (
        #     Line()
        #     .add_xaxis(merged_df['date'].tolist())
        #     .add_yaxis('close', merged_df['close'].tolist(), is_symbol_show=False)
        #     .set_global_opts(
        #         xaxis_opts=opts.AxisOpts(is_scale=True),
        #         yaxis_opts=opts.AxisOpts(type_="value", name="Rate", position="left"),
        #         tooltip_opts=opts.TooltipOpts(trigger='axis'),
        #         datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%", range_start=90, range_end=100)]
        #     )
        #     .render('north_funds_close.html')
        # )

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
        logging.info('run_morning')
        north_data = self.load_north_data()
        curr_date = datetime.datetime.now().strftime('%Y-%m-%d')
        real_date, mf, upper, lower = self.compute_boll(north_data, curr_date)
        scale = mf / upper if mf > 0 else mf / lower
        if scale > 0.9:
            signal = '清' if mf > 0 else '下'
        else:
            signal = 'Morning'
        requests.get(self.wechat_url % (signal, scale, mf, self.boll_upper, self.boll_lower))
        self.draw_boll()


# 2:50-3:00每25秒比对一次实时数据,满足条件通知
# 当天9:00计算boll,通知
# baijiu:0.399997/0.161725, wanjia:0.161903, xique:150.002079, nuoan:150.320007,zhongou:003096, 中小盘:150.110011
# yinliao:802006, ruanjian:802051
if __name__ == '__main__':
    northFunds = northFunds('0.161903', 300, board_code='0/new_dzqj')
    # northFunds.board_code = '0/new_dzqj'  # 0/new_ljhy 0/new_dzqj
    northFunds.draw_boll()
    # print(northFunds.query_security('005176'))
    # northFunds.last_signal()

    # scheduler = BlockingScheduler()
    # scheduler.add_job(northFunds.last_signal, 'cron', day_of_week='1-5', hour=9)
    # scheduler.add_job(northFunds.realtime_signal, 'cron', day_of_week='1-5', hour=14, minute=50)
    # scheduler.start()
