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

# logging.basicConfig(filename='D:/tmp/apscheduler.log', level=logging.INFO)


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


if __name__ == '__main__':
    # 90.BK0459
    res = requests.get('http://push2his.eastmoney.com/api/qt/stock/fflow/daykline/get?lmt=0&klt=101&fields1=f1%2Cf2%2Cf3%2Cf7&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61%2Cf62%2Cf63%2Cf64%2Cf65&secid=90.BK0459')
    res = res.json()['data']['klines']
    res = pd.DataFrame(res, columns=['klines'])
    data = res['klines'].str.split(',', expand=True)
    data.to_csv('D:/data/dz/2020-12-2021-04.csv')






