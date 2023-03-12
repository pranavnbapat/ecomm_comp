import time

from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import gensim.downloader as api
import pandas as pd
from tqdm import tqdm

string1 = "Samsung Galaxy Watch4 Classic Smartwatch, zwart, 42 mm, LTE  "
string2 = "Samsung Galaxy Watch - Smartwatch  - 42 mm - Zwart"

df = pd.read_csv("data/filtered.csv")

df_amazon = df[df['source'] == "amazon"]
df_bol = df[df['source'] == "bol"]

# Loading the pre-trained Word2Vec model
# model = Word2Vec.load("word2vec.model")
model = api.load("word2vec-google-news-300")

new_df = pd.DataFrame(columns=["amazon_product", "bol_product", "amazon_price", "bol_price", "amazon_link", "bol_link",
                               "similarity_score"])

amazon_product = []
bol_product = []
amazon_price = []
bol_price = []
amazon_link = []
bol_link = []
similarity_score = []
for index, value in tqdm(df_amazon.iterrows()):
    for index2, value2 in df_bol.iterrows():
        # Tokenizing the strings
        tokens1 = word_tokenize(value["products"])
        tokens2 = word_tokenize(value2["products"])

        # Vectorizing the tokens
        vec1 = [model.get_vector(token) for token in tokens1 if token in model.key_to_index]
        vec2 = [model.get_vector(token) for token in tokens2 if token in model.key_to_index]

        # Calculating the similarity
        similarity = model.n_similarity(vec1, vec2)

        amazon_product.append(value["products"])
        bol_product.append(value2["products"])
        amazon_price.append(value["prices"])
        bol_price.append(value2["prices"])
        amazon_link.append(value["links"])
        bol_link.append(value2["links"])
        similarity_score.append(similarity)

        # print(f"Similarity between {value['products'][:50]} and {value2['products'][:50]} is {similarity}")
    time.sleep(0.1)

new_df["amazon_product"] = amazon_product
new_df["bol_product"] = bol_product
new_df["amazon_price"] = amazon_price
new_df["bol_price"] = bol_price
new_df["amazon_link"] = amazon_link
new_df["bol_link"] = bol_link
new_df["similarity_score"] = similarity_score

new_df.to_csv("data/similarity_score_word2vec_cosine_gensim.csv", index=False)
