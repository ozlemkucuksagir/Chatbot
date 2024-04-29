import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Bağlantı oluştur
conn = sqlite3.connect('new_interview_questions1.db')
c = conn.cursor()

# Kullanıcıdan metin girişi alın
user_input_text = input("Karşılaştırmak istediğiniz metni girin: ")

# Veritabanından ilk cevabı al
c.execute("SELECT answer FROM interview_questions LIMIT 1")
row = c.fetchone()

if row:
    # Veritabanındaki cevabı al ve TF-IDF vektörüne dönüştür
    answer = row[0]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([answer, user_input_text])
    tfidf_array = tfidf_matrix.toarray()

    # Benzerlik hesapla
    similarity = cosine_similarity(tfidf_array)
    print("Benzerlik:", similarity[0][1])

else:
    print("Veritabanında cevap bulunamadı.")

# Bağlantıyı kapat
conn.close()
