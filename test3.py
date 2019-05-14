import pandas as pd


df = pd.read_csv("4.csv",encoding = "utf-8")
print("前几条：",df.head())
print("后几条：",df.tail())
df=df.drop(['Unnamed: 0'],axis=1)
print("前几条：",df.head())
print("后几条：",df.tail())
df.to_csv("4.csv")