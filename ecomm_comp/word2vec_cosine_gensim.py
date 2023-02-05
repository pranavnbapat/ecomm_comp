from gensim.models import Word2Vec
from nltk.tokenize import word_tokenize
import gensim.downloader as api

string1 = "Samsung Galaxy Watch4 Classic Smartwatch, zwart, 42 mm, LTE  "
string2 = "Samsung Galaxy Watch - Smartwatch  - 42 mm - Zwart"

# Tokenizing the strings
tokens1 = word_tokenize(string1)
tokens2 = word_tokenize(string2)

# Loading the pre-trained Word2Vec model
# model = Word2Vec.load("word2vec.model")
model = api.load("word2vec-google-news-300")

# Vectorizing the tokens
vec1 = [model.get_vector(token) for token in tokens1 if token in model.key_to_index]
vec2 = [model.get_vector(token) for token in tokens2 if token in model.key_to_index]

# Calculating the similarity
similarity = model.n_similarity(vec1, vec2)

print("Similarity between the strings:", similarity)