import numpy as np
import gensim

def similarity(string1, string2):
    # GoogleNews - vectors - negative300.bin
    model = gensim.models.KeyedVectors.load_word2vec_format('pretrained_models/GoogleNews-vectors-negative300.bin',
                                                            binary=True)

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

for string1, string2 in strings:
    print("Similarity between '{}' and '{}': {:.3f}".format(string1, string2, similarity(string1, string2)))

