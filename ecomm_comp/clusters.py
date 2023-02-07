import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

df = pd.read_csv("data/samsung smartwatch_2023-02-06 18_11_45.csv")
prices = df[["prices"]]

kmeans = KMeans(n_clusters=3, init="k-means++", max_iter=300, n_init=10, random_state=0)
labels = kmeans.fit_predict(prices)

df['cluster'] = labels

cluster_0 = df[df['cluster'] == 0]
cluster_1 = df[df['cluster'] == 1]
cluster_2 = df[df['cluster'] == 2]

labels = kmeans.labels_

plt.scatter(x=df['prices'], y=[0 for i in range(len(df["prices"]))], c=labels)
plt.show()

new_df = pd.concat([cluster_0, cluster_2])
new_df.sort_values(by=["products"])
new_df.to_csv("data/filtered.csv", index=False)
