import fasttext as ft

model = ft.train_unsupervised("corpus/custom_corpus.txt", model='cbow')

# Define two lists of words
list1 = "apple orange banana pear"
list2 = "banana cherry apple pear"

# Get the FastText embeddings for each word in the lists
vectors1 = [model.get_word_vector(word) for word in list1.split()]
vectors2 = [model.get_word_vector(word) for word in list2.split()]

# Compare the FastText embeddings for each pair of words
match_count = 0
for v1 in vectors1:
    for v2 in vectors2:
        cosine_similarity = model.cosine_similarity(v1, v2)
        if cosine_similarity > 0.9:
            match_count += 1
            break

# Calculate the percentage of words matched
total_count = len(list1.split()) + len(list2.split())
percent_matched = 100 * match_count / total_count

print("Percentage of words matched: {:.2f}%".format(percent_matched))
