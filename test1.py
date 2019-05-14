import pickle
import pandas as pd
import numpy as np
#f = open('douban_12.pkl','rb')
#ft = open('douban_12.txt', 'w')
print("开始")
"""for line in f:
    #linef=pickle.load(line)
    for i in range(20):
        linef = str(line)
        ft.write(linef)
    break
df = pd.read_pickle("douban_12.pkl")
print("完成")
print(df)"""

df = pd.read_csv("2.csv",encoding = "utf-8")
#df=df.drop(['Unnamed: 0','Unnamed: 0.1','user_name','short','votes','user_count'],axis=1)
print("前几条：",df.head())
print("后几条：",df.tail())

for row in df.itertuples():
    if pd.isnull(getattr(row, 'movie_id')) or pd.isnull(getattr(row, 'user_id')) or pd.isnull(getattr(row, 'rate')):
        print("第%d行进来了！" %getattr(row,  'index'))
        df = df.drop(getattr(row, 'index'))
        print("第%d行删除了了！" % getattr(row, 'index'))
df.to_csv("3.csv")

