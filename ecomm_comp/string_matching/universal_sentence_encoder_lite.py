try:
    import elasticsearch
    from elasticsearch import Elasticsearch

    import pandas as pd
    import json
    from ast import literal_eval
    from tqdm import tqdm
    import datetime
    import os
    import sys
    import os
    import tensorflow as tf
    import tensorflow_hub as hub

    import numpy as np

    from math import sqrt

    print("Loaded  .. . . . . . . .")
except Exception as e:
    print("Some Modules are Missing {} ".format(e))

# embed = hub.KerasLayer(os.getcwd())
url = "https://tfhub.dev/google/universal-sentence-encoder-lite/2"
embed = hub.KerasLayer(url)

tem = "Software engineer"
x = tf.constant([tem])
embeddings = embed(x)
x = np.asarray(embeddings)
x1 = x[0].tolist()

tem = "senior Software developer"
x = tf.constant([tem])
embeddings = embed(x)
x = np.asarray(embeddings)
x2 = x[0].tolist()


from math import sqrt

def cosineSim(a1,a2):
    sum = 0
    suma1 = 0
    sumb1 = 0
    for i,j in zip(a1, a2):
        suma1 += i * i
        sumb1 += j*j
        sum += i*j
    cosine_sim = sum / ((sqrt(suma1))*(sqrt(sumb1)))
    return cosine_sim

print(cosineSim(x1,x2))
