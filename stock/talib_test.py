import pandas_datareader.data as web
import datetime
import pandas as pd
import numpy as np
import talib

stockname='000001.SS'
pd.set_option('display.max_columns', None)

start = datetime.datetime(2020,1,1)#获取数据的起始时间
end = datetime.date.today()#获取数据的中止时间
stock = web.DataReader(stockname,"yahoo",start,end)
# print(stock.head())#显示5行数据
close = [float(x) for x in stock['Close']]
high = [float(x) for x in stock['High']]
low = [float(x) for x in stock['Low']]
#计算5日均价
stock['MA5'] = talib.MA(np.array(close), timeperiod=5)
stock['RSI'] = talib.RSI(np.array(close), timeperiod=14)

print(stock[['Close','Volume','MA5','RSI']])
