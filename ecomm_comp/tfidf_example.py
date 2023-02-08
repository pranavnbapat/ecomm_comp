import math
import sys

import pandas as pd
import numpy as np
from collections import Iterable


# documents
doc1 = "Samsung Galaxy Watch4 Classic  Smartwatch heren  46mm  Silver"
doc2 = "Samsung Galaxy Watch4 Classic Smartwatch Zwart Staal 46mm"
doc3 = "Samsung Galaxy Watch5  Smartwatch  44 mm  Blue"

# query string
query = "Samsung Galaxy Watch 5 44mm Bluetooth  Smartwatch Blue"


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


compute_tf([doc1, doc2, doc3])


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


tf_doc = compute_normalizedtf([doc1, doc2, doc3])


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


idf_dict = compute_idf([doc1, doc2, doc3])

compute_idf([doc1, doc2, doc3])


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


documents = [doc1, doc2, doc3]
tf_idf, df = compute_tfidf_with_alldocs(documents, query)


# Normalized TF for the query string("life learning")
def compute_query_tf(query):
    query_norm_tf = {}
    tokens = query.split()
    for word in tokens:
        query_norm_tf[word] = termFrequency(word , query)
    return query_norm_tf


query_norm_tf = compute_query_tf(query)


# idf score for the query string("life learning")
def compute_query_idf(query):
    idf_dict_qry = {}
    sentence = query.split()
    documents = [doc1, doc2, doc3]
    for word in sentence:
        idf_dict_qry[word] = inverseDocumentFrequency(word ,documents)
    return idf_dict_qry


idf_dict_qry = compute_query_idf(query)


# tf-idf score for the query string("life learning")
def compute_query_tfidf(query):
    tfidf_dict_qry = {}
    sentence = query.split()
    for word in sentence:
        tfidf_dict_qry[word] = query_norm_tf[word] * idf_dict_qry[word]
    return tfidf_dict_qry


tfidf_dict_qry = compute_query_tfidf(query)


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


similarity_docs = rank_similarity_docs(documents)
doc_names = ["Document1", "Document2", "Document3"]
print(doc_names)
print(list(flatten(similarity_docs)))

