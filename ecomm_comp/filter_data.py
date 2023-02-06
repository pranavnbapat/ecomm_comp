import pandas as pd

df = pd.read_csv("data/samsung smartwatch_2023-02-05 01_02_55.csv")

search = ["smartwatch"]

for i in search:
    temp_df = df['products'].str.contains(i)

df = df[temp_df]
print(df.head())
df.to_csv("data/filtered.csv", index=False)
