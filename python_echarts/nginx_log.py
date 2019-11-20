from pyecharts import Bar
from pyecharts import Line
import pandas as pd

df = pd.read_csv("/Users/mac/he/data/account_info.csv")
attr = []
v = []

for x in df.BALANCE:
    attr.append(x)
for y in df.C:
    v.append(y)

line = Line("账户余额分布")
# line.add("数量", attr, v, is_smooth=True, mark_line=["max", "average"])
line.add("人数", attr, v, mark_line=["max", "average"])
line.render()
