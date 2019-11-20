import pandas as pd
import numpy as np

res = map(lambda x, y: x + y, [1, 2, 3], [4, 5, 6])
print(list(range(1, 12)))
df = pd.DataFrame(np.arange(1, 10))
df['a'] = 1
df['b'] = 3
# df.pop('a')
print(df)
for x in range(1,3):
    print(x)
