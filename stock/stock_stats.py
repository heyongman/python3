import math
import pandas as pd
import numpy as np
import tushare as ts
import datetime
import matplotlib.pyplot as plt
import stockstats


if __name__ == '__main__':
    code = "000001"
    begin_time = '2020-02-01'
    end_time = '2020-06-15'
    # pro = ts.pro_api('095b4fa24e3eb5f2532186bea22500119b41ca09de958fa041beccb1')
    # data = pro.query('stock_basic', exchange='SSE', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    # data = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')
    # data = pro.query('daily', ts_code='000001.SH', start_date='20180701', end_date='20180718')
    # data = pro.query(api_name='daily',ts_code='000001.SZ',start_date='20190601', end_date='20190615')
    stock = ts.get_hist_data(code, start=begin_time, end=end_time)
    # stock["date"] = stock.index.values  # 增加日期列。
    # stock = stock.sort_index(0)  # 将数据按照日期排序下。
    ts.is_holiday()
    print(stock)
    # 初始化统计类
    # stockStat = stockstats.StockDataFrame.retype(pd.read_csv('002032.csv'))
    # stockStat = stockstats.StockDataFrame.retype(stock)
    # print("init finish .")

# 交易量
# def volume():
    # volume delta against previous day
    # The Volume Delta (Vol ∆)
    # stockStat[['volume','volume_delta']].plot(figsize=(20,10), grid=True)
    # plt.show()
    #交易量的delta转换。交易量是正，volume_delta把跌变成负值。
    # stockStat[['close','close_delta']].plot(subplots=True, figsize=(20,10), grid=True)
    # plt.show()
