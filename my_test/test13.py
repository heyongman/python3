import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data1 = pd.Series([1, 2, 3, 4])
data2 = pd.Series(['a', 'b'])
df = pd.DataFrame(data1)
df['b'] = data2
df1 = df.drop('b', axis=1)
df.pop('b')
df.drop(0, inplace=True)
print(df.loc[df['b'] >= 'a'])
print(df)
print(df.loc[1])
print(df.iloc[:2])
df = pd.DataFrame(np.random.randint(1, 20, size=(5, 3)))
df.columns = ['a', 'b', 'c']


# print(df.query('a > 1'))
def f(x):
    print('x：%s' % x)
    if x > 10:
        return 10
    else:
        return x
    # return x + y


print(df)
print()
# print(df.pipe(f, 2))
# print(df.pipe((lambda x, y: x + y), 2))
print(df.apply(np.mean))
# print(df.apply(lambda x: [5, 6], axis=1, result_type='expand'))
print(df['a'].apply(lambda x: 5 if x > 10 else x))
print(df.applymap(lambda x: 5 if x > 10 else x))
df.sort_index()
print(df.loc[:, ['a', 'b']])
print(df.a)
df = pd.DataFrame(np.random.randn(10, 4), index=pd.date_range('2018/12/18', periods=10), columns=list('ABCD'))
df.plot()

df = pd.DataFrame(np.random.rand(10, 4), columns=['a', 'b', 'c', 'd'])
df.plot.bar()
plt.show()
