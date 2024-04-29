import sqlite3
from gensim.models import Word2Vec
import nltk

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

# Word2Vec modelini oluştur
word2vec_model = Word2Vec(sentences=tokenized_answers, vector_size=100, window=5, min_count=1, sg=1)

# Modeli eğit
word2vec_model.train(tokenized_answers, total_examples=len(tokenized_answers), epochs=10)

# Eğitilmiş modeli kaydet
word2vec_model.save("word2vec_model.bin")
print("oluştu")

# Veritabanı bağlantısını kapat
conn.close()


test_sentence = "Abstract classes can have both abstract and concrete methods, but interfaces can only contain abstract methods."
tokenized_test_sentence = word_tokenize(test_sentence.lower())

# Test cümlesi için kelime vektörünü elde et
test_vector = word2vec_model.wv[tokenized_test_sentence]

# Tüm cevapların benzerlik skorlarını ölç
similarities = []
for tokenized_answer in tokenized_answers:
    similarities.append(word2vec_model.wv.n_similarity(tokenized_test_sentence, tokenized_answer))

# En yüksek benzerlik skoruna sahip cevabı bul
max_similarity_index = similarities.index(max(similarities))
most_similar_answer = answers[max_similarity_index]

print("Test cümlesi:", test_sentence)
print("En benzer cevap:", most_similar_answer)
print("Benzerlik skoru:", max(similarities))