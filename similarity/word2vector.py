from gensim.models import Word2Vec

# Eğitilmiş modeli yükle
word2vec_model = Word2Vec.load("word2vec_model.bin")

# Bir kelimenin en benzer kelimelerini bul
similar_words = word2vec_model.wv.most_similar('example')
print("En benzer kelimeler:", similar_words)
