import pandas as pd
import pyecharts.options as opts
import requests
from pyecharts.charts import Line, Page
from urllib.parse import urlencode
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:TLS13-AES-256-GCM-SHA384:ECDHE:!COMPLEMENTOFDEFAULT"

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

board_dic = {
    'xny': ['1/gn_xny', '1.515030', -0.08, 0.9, 1.3, False],
    'lj': ['0/new_ljhy', '0.161725', -0.1, 0.9, 1.3, True],
    'xp': ['0/new_dzqj', '0.161903', -0.12, 0.82, 1, True],
    'yl': ['0/new_swzz', '1.512170', -0.12, 0.8, 1.4, False],
    'jr': ['0/new_jrhy', '0.399986', -0.1, 0.9, 0.8, True]
}

dist_dic = {
    'BK0900': 'xny',
    'BK0896': 'lj',
    'BK0891': 'xp',
    'BK0668': 'yl',
    'BK0637': 'jr'
}


def mark_fun(date, action, return_rate, mark_list):
    if action == 'BUY':
        mark_list.append(opts.MarkPointItem(name="", coord=[date, return_rate], value=return_rate, itemstyle_opts=opts.ItemStyleOpts(color='#FF0000')))
    elif action == 'SELL':
        mark_list.append(opts.MarkPointItem(name="", coord=[date, return_rate], value=return_rate, itemstyle_opts=opts.ItemStyleOpts(color='#008000')))
    elif action == 'CLOSE':
        mark_list.append(opts.MarkPointItem(name="", coord=[date, return_rate], value=return_rate, itemstyle_opts=opts.ItemStyleOpts(color='#0000FF')))
    else:
        mark_list.append(opts.MarkPointItem(name="", coord=[date, return_rate], value=return_rate, itemstyle_opts=opts.ItemStyleOpts(color='#FFA500')))


class NorthFunds:
    def __init__(self, limit):
        self.sec_query_url = 'https://searchapi.eastmoney.com/api/Info/Search?token=CCSDCZSDCXYMYZYYSYYXSMDDSMDHHDJT&type=14&pageIndex14=1&pageSize14=100&and14=MultiMatch/Name,Code,PinYin/上证指数/true&returnfields14=Name,Code,MktNum,Classify,SecurityTypeName,ID&isAssociation14=false'
        self.wechat_url = 'http://push.ijingniu.cn/send?key=0af43c6bcac2410d84dad3f91a18dba7&'
        self.stock_url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get?klt=101&fqt=1&end=20500000&iscca=1&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6%2Cf7%2Cf8&fields2=f51%2Cf53&forcect=1'
        self.fund_url = 'https://push2his.eastmoney.com/api/qt/otcfund/kline/get?fields1=f1,f2,f3,f5,f6,f7&fields2=f51,f52&prd=6'
        self.north_his_url = 'https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_MUTUAL_DEAL_HISTORY&sty=TRADE_DATE,NET_DEAL_AMT&filter=(MUTUAL_TYPE%3D%22005%22)&ps=500'
        self.north_rt_url = 'https://push2.eastmoney.com/api/qt/kamtbs.rtmin/get?dpt=app.hsgt&fields1=f1,f3&fields2=f51,f54,f58,f62&ut=b4777e09a0311f6e0734ff19d481afb5'
        # 行业板块增持
        self.board_his_url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/MoneyFlow.ssl_bkzj_zjlrqs?sort=opendate&asc=0'
        self.board_zc_url = 'https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_MUTUAL_BOARD_HOLDRANK&sty=BOARD_CODE,BOARD_INNER_CODE,BOARD_NAME,TRADE_DATE,COMPOSITION_QUANTITY,HOLD_MARKET_CAP,ADD_MARKET_CAP,ADD_SHARES_AMP,MAXHOLD_SECURITY_CODE,MAXHOLD_SECUCODE,MAXHOLD_SECURITY_NAME,MAXADD_SECURITY_CODE,MAXADD_SECUCODE,MAXADD_SECURITY_NAME&callback=&extraCols=&filter=(INTERVAL_TYPE%3D%221%22)(BOARD_CODE%3D%22BK0896%22)&sr=-1,-1&st=TRADE_DATE,COMPOSITION_QUANTITY&token=&var=&source=DataCenter&client=APP'
        self.board_dist_url = 'https://datacenter.eastmoney.com/securities/api/data/get?type=RPT_MUTUAL_BOARD_HOLDRANK&sty=HOLD_MARKET_CAP,BOARD_CODE&callback=&extraCols=&filter=(TRADE_DATE%3D%272021-07-09%27)(BOARD_TYPE%3D%224%22)(INTERVAL_TYPE%3D%221%22)&p=1&ps=100&sr=-1&st=HOLD_MARKET_CAP&token=&var=&source=DataCenter&client=APP'
        self.window = 150
        self.std_n = 2
        self.limit = limit
        self.last_order_dic = {}
        self.position = {k: 0.0 for k in board_dic.keys()}

    # 查询security
    def query_security(self, sec):
        res = requests.get(url=self.sec_query_url.replace('上证指数', sec)).json()['Data']
        return pd.DataFrame(res)

    # 升序
    # date           north_add
    # 2021-02-05       83.93
    # FUND_INFLOW,
    def load_north_his(self):
        res = requests.get(url=self.north_his_url, params={'p': 1}).json()['result']['data']
        if self.limit + self.window > 500:
            res += requests.get(url=self.north_his_url, params={'p': 2}).json()['result']['data']
        if self.limit + self.window > 1000:
            res += requests.get(url=self.north_his_url, params={'p': 3}).json()['result']['data']
        data = pd.DataFrame(res[:self.limit+self.window])
        data.rename(columns={'TRADE_DATE': 'date', 'NET_DEAL_AMT': 'north_add'}, inplace=True)
        data['north_add'] = (data['north_add']/100)
        data['date'] = data['date'].str[:10]
        data.sort_values(by='date', inplace=True)
        return data

    # 单值
    # 23.12
    def load_north_rt(self):
        data = requests.get(self.north_rt_url).json()['data']['s2n']
        data = [x for x in data if len(x) > 15].pop()
        data = round(eval(data.split(',').pop()) / 10000, 2)
        return data

    # 升序
    # date       board_add
    # 2021-02-05   15.21
    def load_board_his(self, board_code, alias):
        params = {
            'page': 1,
            'num': self.limit + self.window,
            'bankuai': board_code
        }
        data = requests.get(self.board_his_url, params=params).json()
        data = pd.DataFrame(data)
        data.rename(columns={'opendate': 'date', 'r0_net': 'board_add'}, inplace=True)
        data[alias+'_board_add'] = (data['board_add'].astype('float')/100000000)
        data = data[['date', alias+'_board_add']]
        data.sort_values(by='date', inplace=True)
        return data

    # 升序
    # date       alias_board_add
    # 2021-02-05   15.21
    def load_board_zc(self, board_code, alias):
        params = {
            'p': 1,
            'ps': self.limit + self.window,
        }
        data = requests.get(self.board_zc_url.replace('BK0896', board_code), params=params).json()['result']['data']
        data = pd.DataFrame(data)
        data['date'] = data['TRADE_DATE'].str[:10]
        data[alias+'_board_add'] = (data['ADD_MARKET_CAP'].astype('float')/100000000).round(decimals=2)
        data = data[['date', alias+'_board_add']]
        data.sort_values(by='date', inplace=True)
        return data

    def load_board_rt(self):
        pass

    # {'ljhy': 0.6, 'dzqj': 0.4}
    # 2019-11-21
    def get_dist_pct(self, date):
        res = requests.get(self.board_dist_url.replace('2021-07-09', date)).json()['result']['data']
        res = [x for x in res if x['BOARD_CODE'] in dist_dic.keys()][:1]
        # total = sum([x['HOLD_MARKET_CAP'] for x in res])
        # res = {dist_dic[x['BOARD_CODE']]: round(x['ADD_MARKET_CAP']/total, 1) for x in res}
        res = {dist_dic[res[0]['BOARD_CODE']]: 1}
        # res = {x: 1/len(board_dic) for x in board_dic.keys()}
        return res

    # 升序
    #       date   open  close
    # 2010-06-29  0.970  0.979
    # prd: 1,2,4,5,6,8 -> 3月，6月，1年，3年，5年，成立来
    def load_close(self, security, alias):
        params = {
            'secid': security,
            'lmt': self.limit,
        }
        url = self.stock_url if security.split('.')[0] != '150' else self.fund_url
        res = requests.get(url=url, params=params).json()['data']['klines']
        data = pd.DataFrame(res, columns=['klines'])
        data = data['klines'].str.split(',', expand=True)
        data.columns = ['date', 'close']
        # data[alias+'_open'] = data['open'].astype('float')
        data[alias+'_close'] = data['close'].astype('float')
        data.drop(columns=['close'], inplace=True)
        return data

    # 这里可以测试近几日的均值，而不是当日的值
    # upper mean lower
    def get_boll(self, north_data, alias):
        roll_data = north_data[alias+'_add'].rolling(self.window)
        mean_data = roll_data.mean()
        std_data = roll_data.std()
        north_data[alias+'_upper'] = (mean_data + self.std_n * std_data).round(decimals=2)
        # north_data[alias+'_mean'] = mean_data.round(decimals=2)
        north_data[alias+'_lower'] = (mean_data - self.std_n * std_data).round(decimals=2)

    # 1, 1.1, 1.2
    def get_stage_rate(self, north_data, curr_date, alias, last_order_date):
        ordered_window = north_data[(north_data['date'] <= curr_date) & (north_data['date'] > last_order_date)][alias+'_close']
        window_start = ordered_window.iloc[0]
        widow_end = ordered_window.iloc[-1]
        stage_rate = round((widow_end - window_start) / window_start, 3)
        lose_rate = (widow_end - ordered_window.max()) / window_start
        return stage_rate, lose_rate

    def action_fun(self, x, north_data):
        inc_sig_list = []
        pos_pct = None
        for alias, pos in self.position.items():
            inc_sig_list.append(pos * (x[alias + '_close'] - x[alias + '_close_last']))
        for alias, board_list in board_dic.items():
            signal = None
            if x[alias+'_add'] > 0 and x[alias+'_add'] / x[alias+'_upper'] > board_list[3] and self.position[alias] <= 0 and sum(self.position.values()) < 1:
                if not pos_pct:
                    pos_pct = self.get_dist_pct(x.date)
                if pos_pct.get(alias) and pos_pct[alias] > 0:
                    self.position[alias] = pos_pct[alias]
                    self.last_order_dic[alias] = x.date
                    signal = 'BUY'
            elif x[alias+'_add'] < 0 and x[alias+'_add'] / x[alias+'_lower'] > board_list[4] and self.position[alias] > 0:
                self.position[alias] = 0
                last_order_date = self.last_order_dic.pop(alias)
                signal = 'SELL'
                stage_rate, lose_rate = self.get_stage_rate(north_data, x.date, alias, last_order_date)
                # print(alias, last_order_date, x.date, stage_rate, 'SELL')
            # 强平
            if self.position[alias] > 0 and not self.last_order_dic[alias] == x.date:
                stage_rate, lose_rate = self.get_stage_rate(north_data, x.date, alias, self.last_order_dic[alias])
                if lose_rate < board_list[2]:
                    self.position[alias] = 0
                    signal = 'CLOSE'
                    # last_order_date = self.last_order_dic.pop(alias)
                    # print(alias, last_order_date, x.date, stage_rate, 'CLOSE', lose_rate)
            inc_sig_list.append(signal)
            # if x.date == north_data['date'].iloc[-1] and self.last_order_dic.get(alias):
            #     last_order_date = self.last_order_dic[alias]
            #     stage_rate, lose_rate = self.get_stage_rate(north_data, x.date, alias, last_order_date)
                # print(alias, last_order_date, x.date, stage_rate)
            if x.date == north_data['date'].iloc[-1]:
                if not signal:
                    signal = "Morning"
                params = {
                    "head": signal+'-'+alias.upper()+'-'+x.date,
                    "body": "A:%s H:%s L:%s" % (x[alias+'_add'], x[alias+'_upper'], x[alias+'_lower'])
                }
                # print(params)
                # if signal != 'Morning' or alias == 'lj':
                #     requests.get(self.wechat_url + urlencode(params))
        return inc_sig_list

    def get_action(self):
        north_data = self.load_north_his()
        for alias, board_list in board_dic.items():
            board_his_data = self.load_board_his(board_list[0], alias)
            # board_his_data = self.load_board_zc(board_list[6], alias)
            north_data = north_data.merge(board_his_data, how='inner', on='date')
            if board_list[5]:
                north_data[alias+'_add'] = ((north_data[alias+'_board_add']/1.5) + north_data['north_add']).round(decimals=2)
            else:
                north_data[alias+'_add'] = north_data['north_add'].round(decimals=2)
            # north_data.drop(columns=[alias+'_board_add'], inplace=True)
            self.get_boll(north_data, alias)

        north_data.dropna(subset=[list(board_dic.keys())[0]+'_upper'], inplace=True)
        north_data.drop(columns=['north_add'], inplace=True)

        for alias, board_list in board_dic.items():
            north_data = north_data.merge(self.load_close(board_list[1], alias), how='inner', on='date')
            north_data[alias+'_close'].fillna(method='ffill', inplace=True)
            north_data[alias+'_close_last'] = north_data[alias+'_close'].shift(1)
        action_df = north_data.apply(self.action_fun, north_data=north_data, axis=1, result_type='expand')
        return north_data, action_df

    def draw(self, north_data, action_df):
        i = 0
        for alias, board_list in board_dic.items():
            north_data[alias + '_inc'] = action_df[i]
            i += 1
        for alias, board_list in board_dic.items():
            north_data[alias+'_m'] = action_df[i]
            i += 1

        north_data['R'] = 0.0
        north_data['m'] = None
        for alias, board_list in board_dic.items():
            north_data['R'] += north_data[alias + '_inc'].cumsum() * 100 / north_data[alias + '_close'].iloc[0]
            north_data['m'] = north_data['m'].fillna(north_data[alias+'_m'])
        north_data = north_data.round({'R': 1})
        return north_data
        mark_opts = []
        north_data.dropna(subset=['m']).apply(lambda x: mark_fun(x.date, x.m, x.return_rate, mark_opts), axis=1)
        markpoint_opts = opts.MarkPointOpts(data=mark_opts, symbol_size=25, label_opts=opts.LabelOpts(position="inside", color="#fff", font_size=6))
        first_alias = list(board_dic.keys())[0]
        bench_list = ((north_data[first_alias + '_close']-north_data[first_alias + '_close_last']).cumsum()*100/north_data[first_alias + '_close'].iloc[0]).tolist()

        multi_line = (
            Line()
            .add_xaxis(north_data['date'].tolist())
            .add_yaxis('R', north_data['R'].tolist(), is_symbol_show=False, markpoint_opts=markpoint_opts, linestyle_opts=opts.LineStyleOpts(color='#FF0000'))
            .add_yaxis('bj', bench_list, is_symbol_show=False, linestyle_opts=opts.LineStyleOpts(color='#000000'))
            .set_global_opts(
                title_opts=opts.TitleOpts(title='North'),
                xaxis_opts=opts.AxisOpts(is_scale=True),
                yaxis_opts=opts.AxisOpts(type_="value", name="Rate(%)", position="right"),
                tooltip_opts=opts.TooltipOpts(trigger='axis'),
                datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%", range_start=0, range_end=100)]
            )
        )

        page = Page(layout=Page.DraggablePageLayout)
        page.add(multi_line)

        for alias, board_list in board_dic.items():
            close_line = (
                Line()
                .add_xaxis(north_data['date'].tolist())
                .add_yaxis('close', north_data[alias+'_close'].tolist(), is_symbol_show=False, yaxis_index=0, linestyle_opts=opts.LineStyleOpts(color='#FF0000'))
                .extend_axis(yaxis=opts.AxisOpts(type_="value", name="ADD", position="left"))
                .add_yaxis('add', north_data[alias+'_add'].tolist(), is_symbol_show=False, yaxis_index=1, linestyle_opts=opts.LineStyleOpts(color='#000000'))
                .add_yaxis('upper', north_data[alias+'_upper'].tolist(), is_symbol_show=False, yaxis_index=1, linestyle_opts=opts.LineStyleOpts(color='#FFA500'))
                .add_yaxis('lower', north_data[alias+'_lower'].tolist(), is_symbol_show=False, yaxis_index=1, linestyle_opts=opts.LineStyleOpts(color='#1E90FF'))
                .set_global_opts(
                    title_opts=opts.TitleOpts(title=alias),
                    xaxis_opts=opts.AxisOpts(is_scale=True),
                    yaxis_opts=opts.AxisOpts(type_="value", name="Close", position="right"),
                    tooltip_opts=opts.TooltipOpts(trigger='axis'),
                    datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%", range_start=0, range_end=100)]
                )
            )
            page.add(close_line)
        page.render('north_funds.html')
        return north_data


# 2:50-3:00每25秒比对一次实时数据,满足条件通知
# 当天9:00计算boll,通知
# baijiu:0.399997/0.161725, wanjia:0.161903, yiliao:1.512170, xny:1.515030
if __name__ == '__main__':
    northFunds = NorthFunds(200)
    north_df, action_df = northFunds.get_action()
    mer_df = northFunds.draw(north_df, action_df)
    mer_df = mer_df.filter(regex=r'date|m|R', axis=1)
    mer_df['m'].iloc[-1] = '-'
    print(mer_df.dropna(subset=['m']).fillna(value='-').drop(columns=['m']))
    # print(northFunds.query_security('990001'))
    # print(northFunds.load_close('125.990001','a'))

