import datetime
import pandas as pd

data = [['2411', '2021-01-22', 520.0, 514.4953],
        ['2412', '2021-01-22', 520.0, 517.1636],
        ['2413', '2021-01-25', 520.0, 495.4339],
        ['2414', '2021-01-25', 520.0, 509.6982],
        ['2415', '2021-01-26', 520.0, 535.4756],
        ['2416', '2021-01-26', 520.0, 510.8383],
        ['2417', '2021-01-27', 520.0, 517.7327],
        ['2418', '2021-01-27', 520.0, 505.0584],
        ['2419', '2021-01-28', 520.0, 542.3838],
        ['2420', '2021-01-28', 520.0, 531.6154]]

df = pd.DataFrame(data, columns=['no', 'day', 'quota_daily', 'quota_daily_balance'])
df['net_amount'] = df['quota_daily'] - df['quota_daily_balance']
print(df['day'].iloc[2])

# df = df.groupby('day')[['net_amount']].sum()
# print(df)
#
# print("2021-01-27 00:00:00"[:10])
