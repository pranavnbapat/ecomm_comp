import gensim

model = gensim.models.KeyedVectors.load_word2vec_format('pretrained_models/GoogleNews-vectors-negative300.bin', binary=True)
string1 = "Samsung Galaxy Watch4 Classic Smartwatch, zwart, 42 mm, LTE"
string2 = "Samsung Galaxy Watch - Smartwatch - 42 mm - Zwart"

tokens1 = string1.split()
tokens2 = string2.split()

vec1 = [model.get_vector(token) for token in tokens1 if token in model.key_to_index]
vec2 = [model.get_vector(token) for token in tokens2 if token in model.key_to_index]

similarity = model.n_similarity(vec1, vec2)
print('Similarity:', similarity)