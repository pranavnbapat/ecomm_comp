import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/filtered.csv")

amazon_df = df[df["source"] == "amazon"]
bol_df = df[df["source"] == "bol"]

amazon_list = amazon_df["prices"].to_list()
bol_list = bol_df["prices"].to_list()

# Subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# Line plot
ax1.plot(amazon_list, label='Amazon')
ax1.plot(bol_list, label='Bol')
ax1.set_xlabel('Index')
ax1.set_ylabel('Price')
ax1.set_title('Line Plot of Prices')
ax1.legend()

# Box plot
ax2.boxplot([amazon_list, bol_list])
ax2.set_xticklabels(['Amazon', 'Bol'])
# ax2.set_xlabel('Index')
ax2.set_ylabel('Price')
ax2.set_title('Box Plot of Prices')

plt.tight_layout()
plt.show()
