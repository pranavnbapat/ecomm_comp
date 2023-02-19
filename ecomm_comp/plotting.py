import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# create a new directory for the output charts
output_dir = "data/price_comparison_charts"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# get a list of all CSV files in the directory
data_dir = "data"
csv_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]

# iterate over each CSV file
for file in csv_files:
    # read the CSV file into a pandas DataFrame
    df = pd.read_csv(os.path.join(data_dir, file))

    # create a box plot and line plot for the prices, grouped by source
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    sns.boxplot(x="source", y="prices", data=df, ax=ax1)
    sns.lineplot(x="prices", y="source", data=df, ax=ax2)

    # add text to the box plot to show the number of products from each source
    counts = df["source"].value_counts()
    for i, source in enumerate(counts.index):
        ax1.text(i, 1.05*df["prices"].max(), "{}: {}".format(source, counts[source]), ha="center")

    ax1.set_title("Box plot for {}".format(file))
    ax1.set_xlabel("Source")
    ax1.set_ylabel("Price")

    ax2.set_title("Line plot for {}".format(file))
    ax2.set_xlabel("Timestamp")
    ax2.set_ylabel("Price")
    ax2.legend(loc="best")

    fig.savefig(os.path.join(output_dir, file.replace(".csv", "_plots.jpg")))
    plt.close()



# Importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Creating dummy data
products = ['Product A', 'Product B', 'Product C', 'Product D', 'Product E']
prices_amazon = [10.0, 15.0, 20.0, 25.0, 30.0]
prices_bol = [12.0, 14.0, 22.0, 28.0, 32.0]
timestamps = pd.date_range(start='2022-02-01', periods=5)

# Creating data frame
data = pd.DataFrame({
    'products': products,
    'prices': prices_amazon,
    'source': 'Amazon',
    'timestamp': timestamps
})
data = data.append(pd.DataFrame({
    'products': products,
    'prices': prices_bol,
    'source': 'Bol',
    'timestamp': timestamps
}), ignore_index=True)

# Line plot
sns.lineplot(x='timestamp', y='prices', hue='source', data=data)
plt.xlabel('Timestamp')
plt.ylabel('Price')
plt.title('Product Prices Comparison')
plt.show()

# Bar plot
sns.barplot(x='products', y='prices', hue='source', data=data)
plt.xlabel('Products')
plt.ylabel('Price')
plt.title('Product Prices Comparison')
plt.show()

# Scatter plot
sns.scatterplot(x='prices', y='products', hue='source', data=data)
plt.xlabel('Price')
plt.ylabel('Products')
plt.title('Product Prices Comparison')
plt.show()

# Box plot
sns.boxplot(x='prices', y='products', hue='source', data=data)
plt.xlabel('Price')
plt.ylabel('Products')
plt.title('Product Prices Comparison')
plt.show()




# Importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Creating dummy data
product = 'Product A'
prices_amazon = [10.0, 12.0, 15.0, 18.0, 20.0, 22.0, 25.0, 28.0, 30.0, 35.0]
prices_bol = [12.0, 13.0, 14.0, 16.0, 22.0, 25.0, 28.0, 30.0, 32.0, 34.0]
timestamps = pd.date_range(start='2022-02-01', periods=10)

# Creating data frame
data = pd.DataFrame({
    'product': [product] * 10,
    'prices': prices_amazon + prices_bol,
    'source': ['Amazon'] * 10 + ['Bol'] * 10,
    'timestamp': list(timestamps) * 2
})

# Line plot
sns.lineplot(x='timestamp', y='prices', hue='source', data=data)
plt.xlabel('Timestamp')
plt.ylabel('Price')
plt.title('Price Comparison for ' + product)
plt.show()
