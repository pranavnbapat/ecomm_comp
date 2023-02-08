import math
import sys
from tqdm import tqdm
import pandas as pd
import numpy as np
from collections import Iterable

df = pd.read_csv("data/filtered.csv")

amazon_df = df[df["source"] == "amazon"]
bol_df = df[df["source"] == "bol"]


# term -frequenvy :word occurences in a document
def compute_tf(docs_list):
    for doc in docs_list:
        doc1_lst = doc.split(" ")
        wordDict_1 = dict.fromkeys(set(doc1_lst), 0)

        for token in doc1_lst:
            wordDict_1[token] += 1
        df = pd.DataFrame([wordDict_1])
        idx = 0
        new_col = ["Term Frequency"]
        df.insert(loc=idx, column='Document', value=new_col)


# Normalized Term Frequency
def termFrequency(term, document):
    normalizeDocument = document.lower().split()
    return normalizeDocument.count(term.lower()) / float(len(normalizeDocument))


def compute_normalizedtf(documents):
    tf_doc = []
    for txt in documents:
        sentence = txt.split()
        norm_tf= dict.fromkeys(set(sentence), 0)
        for word in sentence:
            norm_tf[word] = termFrequency(word, txt)
        tf_doc.append(norm_tf)
        df = pd.DataFrame([norm_tf])
        idx = 0
        new_col = ["Normalized TF"]
        df.insert(loc=idx, column='Document', value=new_col)
    return tf_doc


def inverseDocumentFrequency(term, allDocuments):
    numDocumentsWithThisTerm = 0
    for doc in range(0, len(allDocuments)):
        if term.lower() in allDocuments[doc].lower().split():
            numDocumentsWithThisTerm = numDocumentsWithThisTerm + 1

    if numDocumentsWithThisTerm > 0:
        return 1.0 + math.log(float(len(allDocuments)) / numDocumentsWithThisTerm)
    else:
        return 1.0


def compute_idf(documents):
    idf_dict = {}
    for doc in documents:
        sentence = doc.split()
        for word in sentence:
            idf_dict[word] = inverseDocumentFrequency(word, documents)
    return idf_dict


# tf-idf score across all docs for the query string("life learning")
def compute_tfidf_with_alldocs(documents, query):
    tf_idf = []
    index = 0
    query_tokens = query.split()
    df = pd.DataFrame(columns=['doc'] + query_tokens)
    for doc in documents:
        df['doc'] = np.arange(0, len(documents))
        doc_num = tf_doc[index]
        sentence = doc.split()
        for word in sentence:
            for text in query_tokens:
                if (text == word):
                    idx = sentence.index(word)
                    tf_idf_score = doc_num[word] * idf_dict[word]
                    tf_idf.append(tf_idf_score)
                    df.iloc[index, df.columns.get_loc(word)] = tf_idf_score
        index += 1
    df.fillna(0, axis=1, inplace=True)
    return tf_idf, df


# Normalized TF for the query string("life learning")
def compute_query_tf(query, list_of_docs=None):
    query_norm_tf = {}
    tokens = query.split()
    for word in tokens:
        query_norm_tf[word] = termFrequency(word , query)
    return query_norm_tf


# idf score for the query string("life learning")
def compute_query_idf(query, list_of_docs):
    idf_dict_qry = {}
    sentence = query.split()
    documents = list_of_docs
    for word in sentence:
        idf_dict_qry[word] = inverseDocumentFrequency(word ,documents)
    return idf_dict_qry


# tf-idf score for the query string("life learning")
def compute_query_tfidf(query):
    tfidf_dict_qry = {}
    sentence = query.split()
    for word in sentence:
        tfidf_dict_qry[word] = query_norm_tf[word] * idf_dict_qry[word]
    return tfidf_dict_qry


def cosine_similarity(tfidf_dict_qry, df, query, doc_num):
    dot_product = 0
    qry_mod = 0
    doc_mod = 0
    tokens = query.split()

    for keyword in tokens:
        dot_product += tfidf_dict_qry[keyword] * df[keyword][df['doc'] == doc_num]
        # ||Query||
        qry_mod += tfidf_dict_qry[keyword] * tfidf_dict_qry[keyword]
        # ||Document||
        doc_mod += df[keyword][df['doc'] == doc_num] * df[keyword][df['doc'] == doc_num]
    qry_mod = np.sqrt(qry_mod)
    doc_mod = np.sqrt(doc_mod)
    # implement formula
    denominator = qry_mod * doc_mod
    cos_sim = dot_product / denominator

    return cos_sim


def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item


def rank_similarity_docs(data):
    cos_sim =[]
    for doc_num in range(0 , len(data)):
        cos_sim.append(cosine_similarity(tfidf_dict_qry, df , query , doc_num).tolist())
    return cos_sim


new_df = pd.DataFrame(columns=["amazon_product", "bol_product", "amazon_price", "bol_price", "amazon_link", "bol_link", "similarity_score"])
amazon_products = []
bol_products = []
amazon_prices = []
bol_prices = []
amazon_links = []
bol_links = []
similarity_score = []

for index1, value1 in tqdm(amazon_df.iterrows()):
    temp_max_score = 0
    temp_amazon_product = ""
    temp_bol_product = ""
    temp_amazon_price = ""
    temp_bol_price = ""
    temp_amazon_link = ""
    temp_bol_link = ""
    flattened_list = ""
    for index2, value2 in bol_df.iterrows():
        query = value2["products"]
        # list_of_docs = amazon_df["products"].to_list()
        list_of_docs = [value1["products"]]

        compute_tf(list_of_docs)

        tf_doc = compute_normalizedtf(list_of_docs)

        idf_dict = compute_idf(list_of_docs)
        compute_idf(list_of_docs)

        documents = list_of_docs
        tf_idf, df = compute_tfidf_with_alldocs(documents, query)

        query_norm_tf = compute_query_tf(query, list_of_docs)

        idf_dict_qry = compute_query_idf(query, list_of_docs)

        tfidf_dict_qry = compute_query_tfidf(query)

        similarity_docs = rank_similarity_docs(documents)
        # print(value1["products"], value1["prices"])
        # print(value2["products"], value2["prices"])
        # print(max(list(flatten(similarity_docs))))
        flattened_list = list(flatten(similarity_docs))
        print(value1["products"])
        print(value2["products"])

    if temp_max_score < float(flattened_list[0]):
        temp_max_score = float(flattened_list[0])
        amazon_products.append(value1["products"])
        bol_products.append(value2["products"])
        amazon_prices.append(value1["prices"])
        bol_prices.append(value2["prices"])
        amazon_links.append(value1["links"])
        # bol_links.append(value2["links"])
        similarity_score.append(temp_max_score)
    sys.exit()

new_df["amazon_product"] = amazon_products
new_df["bol_product"] = bol_products
new_df["amazon_price"] = amazon_prices
new_df["bol_price"] = bol_prices
new_df["amazon_link"] = amazon_links
new_df["bol_link"] = bol_links
new_df["similarity_score"] = similarity_score
new_df.to_csv("data/tfidf_score.csv", index=False)
