import time
import pandas as pd
from tqdm import tqdm

df = pd.read_csv("data/filtered.csv")

df_amazon = df[df['source'] == "amazon"]
df_bol = df[df['source'] == "bol"]

new_df = pd.DataFrame(columns=["amazon_product", "bol_product", "amazon_price", "bol_price", "amazon_link", "bol_link",
                               "similarity_score"])

amazon_product = []
bol_product = []
amazon_price = []
bol_price = []
amazon_link = []
bol_link = []
word_similarity = []


def compare_lists(list1, list2):
    set1 = set(list1.split())
    set2 = set(list2.split())
    match_count = len(set1.intersection(set2))
    total_count = len(set1) + len(set2)
    return 100 * match_count / total_count


for index, value in tqdm(df_amazon.iterrows()):
    for index2, value2 in df_bol.iterrows():
        amazon_product.append(value["products"])
        bol_product.append(value2["products"])
        amazon_price.append(value["prices"])
        bol_price.append(value2["prices"])
        amazon_link.append(value["links"])
        bol_link.append(value2["links"])
        word_similarity.append(compare_lists(value["products"], value2["products"]))
    time.sleep(0.1)


new_df["amazon_product"] = amazon_product
new_df["bol_product"] = bol_product
new_df["amazon_price"] = amazon_price
new_df["bol_price"] = bol_price
new_df["amazon_link"] = amazon_link
new_df["bol_link"] = bol_link
new_df["similarity_score"] = word_similarity

new_df.to_csv("data/word_similarity.csv", index=False)
