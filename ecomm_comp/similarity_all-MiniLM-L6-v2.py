import sys
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv("smartwatch_apple.csv")

df1 = df[df['source'] == "amazon"]
df2 = df[df['source'] == "bol"]

new_df = pd.DataFrame(columns=["product_amazon", "product_bol", "price_amazon", "price_bol", "similarity_score"])

# Converting dataframe to list for processing
source_amazon = df1['product'].to_list()
source_bol = df2['product'].to_list()

# Using huggingface sentence transformer model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
embeddings_amazon = model.encode(source_amazon)
embeddings_bol = model.encode(source_bol)

amazon_list = []
bol_list = []
amazon_price_list = []
bol_price_list = []
similarity_score_list = []

for i, v1 in enumerate(source_amazon):
    for j, v2 in enumerate(source_bol):
        if cosine_similarity(embeddings_amazon[i].reshape(1, -1), embeddings_bol[j].reshape(1, -1))[0][0] > 0.91:
            amazon_list.append(v1)
            bol_list.append(v2)
            amazon_price_list.append(df1["price"].iloc[i])
            bol_price_list.append(df2["price"].iloc[j])
            similarity_score_list.append(cosine_similarity(
                embeddings_amazon[i].reshape(1, -1), embeddings_bol[j].reshape(1, -1))[0][0])


new_df["product_amazon"] = amazon_list
new_df["product_bol"] = bol_list
new_df["price_amazon"] = amazon_price_list
new_df["price_bol"] = bol_price_list
new_df["similarity_score"] = similarity_score_list
new_df.to_csv("smartwatch_comparison.csv", index=False)


# Using glove model

