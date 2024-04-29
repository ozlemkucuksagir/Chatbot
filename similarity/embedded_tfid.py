import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# Bağlantı oluştur
conn = sqlite3.connect('new_interview_questions1.db')
c = conn.cursor()

# 500 belgeyi al<
c.execute("SELECT id, answer FROM interview_questions")
rows = c.fetchall()

if rows:
    # TF-IDF vektörizasyonu için yeni bir vectorizer oluştur
    vectorizer = TfidfVectorizer()

    for row in rows:
        # Her bir belgeyi ayrı ayrı TF-IDF vektörüne dönüştür
        tfidf_matrix = vectorizer.fit_transform([row[1]])
        tfidf_array = tfidf_matrix.toarray()

        # TF-IDF vektörlerini pickle formatında kaydet
        tfidf_vectors = pickle.dumps(tfidf_array)
        # Yeni bir sütun ekleyerek TF-IDF vektörlerini kaydet

        # Veritabanına TF-IDF vektörlerini kaydet
        c.execute("UPDATE interview_questions SET tfidf_vector=? WHERE id=?", (tfidf_vectors, row[0]))

    # Değişiklikleri kaydet
    conn.commit()
    print("TF-IDF vektörleri başarıyla kaydedildi.")

else:
    print("Veritabanında vektör bulunamadı.")

# Bağlantıyı kapat
conn.close()
