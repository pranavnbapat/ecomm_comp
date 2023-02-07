import sys

import pandas as pd
import fuzzywuzzy
from fuzzywuzzy import fuzz

df = pd.read_csv("data/filtered.csv")
df_amazon = df[df["source"] == "amazon"]
df_bol = df[df["source"] == "bol"]

new_df = pd.DataFrame(columns=["product_amazon", "product_bol", "similarity_score"])

amazon_list = []
bol_list = []
amazon_price_list = []
bol_price_list = []
similarity_score_list = []


for index1, value1 in df_bol.iterrows():
    for index2, value2 in df_amazon.iterrows():
        score = fuzz.token_set_ratio(value1["products"], value2["products"])
        if score >= 70:
            amazon_list.append(value2["products"])
            bol_list.append(value1["products"])
            # amazon_price_list.append(value2.prices)
            # bol_price_list.append(value1.prices)
            similarity_score_list.append(score)

new_df["product_amazon"] = amazon_list
new_df["product_bol"] = bol_list
# new_df["price_amazon"] = amazon_price_list
# new_df["price_bol"] = bol_price_list
new_df["similarity_score"] = similarity_score_list
new_df.to_csv("data/fuzzy_comparison.csv", index=False)

# similar_strings = [item2 for item1 in df_amazon['products'] for item2 in df_bol['products'] if fuzz.token_set_ratio(item1, item2) >= 70]
# result = list(set(similar_strings))
# print(result)
