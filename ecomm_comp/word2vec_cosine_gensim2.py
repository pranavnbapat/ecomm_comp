import time

import numpy as np
import gensim
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
similarity_score = []


model = gensim.models.KeyedVectors.load_word2vec_format('pretrained_models/GoogleNews-vectors-negative300.bin',
                                                            binary=True)


def similarity(string1, string2):
    tokens1 = string1.split()
    tokens2 = string2.split()
    vectors1 = np.zeros((len(tokens1), 300))
    for i in range(len(tokens1)):
        if tokens1[i] in model:
            vectors1[i] = model[tokens1[i]]
    vectors2 = np.zeros((len(tokens2), 300))
    for i in range(len(tokens2)):
        if tokens2[i] in model:
            vectors2[i] = model[tokens2[i]]

    if vectors1.shape[0] > vectors2.shape[0]:
        vectors2 = np.pad(vectors2, ((0, vectors1.shape[0] - vectors2.shape[0]), (0, 0)), mode='constant')
    else:
        vectors1 = np.pad(vectors1, ((0, vectors2.shape[0] - vectors1.shape[0]), (0, 0)), mode='constant')

    return np.mean(vectors1 * vectors2, axis=1).sum() / np.sqrt((vectors1 ** 2).sum() * (vectors2 ** 2).sum())


strings = [("Samsung Galaxy Watch4 - Smartwatch Dames - 40mm - Pink gold", "Samsung Galaxy Watch4 Rose Gold - 40MM  ")]


for index, value in tqdm(df_amazon.iterrows()):
    for index2, value2 in df_bol.iterrows():
        amazon_product.append(value["products"])
        bol_product.append(value2["products"])
        amazon_price.append(value["prices"])
        bol_price.append(value2["prices"])
        amazon_link.append(value["links"])
        bol_link.append(value2["links"])
        similarity_score.append(similarity(value["products"], value2["products"]))
    time.sleep(0.1)

new_df["amazon_product"] = amazon_product
new_df["bol_product"] = bol_product
new_df["amazon_price"] = amazon_price
new_df["bol_price"] = bol_price
new_df["amazon_link"] = amazon_link
new_df["bol_link"] = bol_link
new_df["similarity_score"] = similarity_score

new_df.to_csv("data/similarity_score_word2vec_cosine_gensim2.csv", index=False)
