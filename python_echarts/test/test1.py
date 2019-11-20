import pandas as pd

ds = pd.read_csv("/Users/mac/he/data/account_info.csv")
print(ds.info())
print()
print(ds.columns)
