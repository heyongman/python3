import json
import time

import pandas as pd
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
import numpy as np
import pyecharts.options as opts
from pyecharts.charts import Line
import os
import requests
from urllib.parse import quote, urlencode

import decimal as D
# logging.basicConfig(filename='D:/tmp/apscheduler.log', level=logging.INFO)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    raise Exception('aaa')


def job1():
    print('job1')


def two_array():
    li = [[1,2],[3,4],[5,6]]
    li = np.array(li)
    data = li[:,0]
    print(data)

def df_append():
    series = pd.Series(['2020-02-01','2020-02-02','2020-02-03','2020-02-04',])
    data = pd.DataFrame(series,columns=['date'])
    data['v1'] = None
    data['v2'] = None
    data = data.append([1,2,3])
    print(data)


def echarts_test():
    date_list = [1,2,3,4,5]
    c = (
        Line()
        .add_xaxis(date_list)
        .add_yaxis('lower', date_list, is_symbol_show=False)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="North"),
            xaxis_opts=opts.AxisOpts(is_scale=True),
            tooltip_opts=opts.TooltipOpts(trigger='axis'),
            datazoom_opts=[opts.DataZoomOpts(pos_bottom="-2%")]
        )
        .render("echarts_test.html")
    )

board_dic = {
    'dzqj': ['0/new_dzqj', '0.161903', -0.14, 0.82, 1, True],
    'ljhy': ['0/new_ljhy', '0.399997', -0.1, 0.9, 1.3, True],
    'swzz': ['0/new_swzz', '0.399989', -0.14, 0.8, 1.4, False],
    'xny': ['1/gn_xny', '0.399808', -0.15, 0.9, 1.3, False],
    'jrhy': ['0/new_jrhy', '1.512800', -0.15, 0.9, 1.3, True]
}

def filter_test():
    df = pd.DataFrame(np.random.randint(1, 10, (2, 3)), columns=['asd_aa','as_b','aca'])
    df = df.filter(regex=r'.*(?<!aa)$', axis=1)
    print(df)


if __name__ == '__main__':
    param = {
        'a':1,
        'v':'ad ada' + json.dumps({'as_ad': 1.1})
    }
    print(str({'as_ad': 1.1}))
    print(urlencode(param,encoding='utf-8'))
    print(quote(param['v']))

