import pandas as pd
import datetime
import numpy as np

pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.width', 5000)


def fee_fun(amount, date_diff, is_buy):
    if is_buy:
        fee = 0.0015
    elif date_diff < 7:
        fee = 0.015
    elif date_diff < 30:
        fee = 0.0075
    # elif date_diff < 30:
    #     fee = 0.005
    else:
        fee = 0.005
    return fee * abs(amount)


if __name__ == '__main__':
    data = pd.read_csv(r'C:\Users\heyon\Desktop\trans.txt', sep='\t', thousands=',')
    data['last_date'] = data['date'].shift(1)
    data['date_diff'] = (pd.to_datetime(data['date']) - pd.to_datetime(data['last_date'])).dt.days
    data['is_buy'] = data['amount'].apply(lambda x: True if float(x) > 0 else False)
    data['total_fees'] = data.apply(lambda x: fee_fun(x.amount, x.date_diff, x.is_buy), axis=1)
    print(data)
    print(data['total_fees'].sum())
    print(data['fees'].sum())
