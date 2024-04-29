import sqlite3
from gensim.models import Word2Vec
import nltk
import numpy as np
from nltk.tokenize import word_tokenize

nltk.download('punkt')

# Veritabanı bağlantısını oluştur
conn = sqlite3.connect('new_interview_questions1.db')
c = conn.cursor()

# Tüm cevapları al
c.execute("SELECT answer FROM interview_questions")
answers = [row[0] for row in c.fetchall()]

# Cümleleri tokenlara ayır
tokenized_answers = [word_tokenize(answer.lower()) for answer in answers]

# Word2Vec modelini oluştur ve OOV kelimeleri yok sayarak eğitin
word2vec_model = Word2Vec(sentences=tokenized_answers, vector_size=100, window=5, min_count=1, sg=1, ns_exponent=0)

# Modeli eğit
word2vec_model.train(tokenized_answers, total_examples=len(tokenized_answers), epochs=10)

# Eğitilmiş modeli kaydet
word2vec_model.save("word2vec_model.bin")
print("Model oluşturuldu ve eğitildi.")

# Veritabanı bağlantısını kapat
conn.close()

# Modeli yükle
word2vec_model = Word2Vec.load("word2vec_model.bin")

# Test cümlesi
test_sentence = "Interfaces cannot exclusively contain abstract methods."
tokenized_test_sentence = word_tokenize(test_sentence.lower())

# Test cümlesi için kelime vektörünü elde et
test_vector = [word2vec_model.wv[word] for word in tokenized_test_sentence if word in word2vec_model.wv]

# Tüm cevapların benzerlik skorlarını ölç
similarities = []
for tokenized_answer in tokenized_answers:
    similarity = word2vec_model.wv.n_similarity(tokenized_test_sentence, tokenized_answer)
    similarities.append(similarity if not np.isnan(similarity) else 0)  # NaN değerleri sıfır ile değiştir

# En yüksek benzerlik skoruna sahip cevabı bul
max_similarity_index = similarities.index(max(similarities))
most_similar_answer = answers[max_similarity_index]

print("Test cümlesi:", test_sentence)
print("En benzer cevap:", most_similar_answer)
print("Benzerlik skoru:", max(similarities))
