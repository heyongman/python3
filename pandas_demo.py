import pandas as pd
import numpy as np

df = pd.DataFrame(columns=['证件号码', '档案编号', '驾驶人照片'])
# 字段数要对应上
df.loc[1] = [1, 2, 3]
li = [1,2,3,4]
last = li[-1]
print(last)
print(li[1:])

for i in range(1,4):
    print(i,li[i])