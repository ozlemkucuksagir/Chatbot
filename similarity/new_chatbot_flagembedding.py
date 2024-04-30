import sqlite3
from FlagEmbedding import FlagModel
import numpy as np

# Veritabanı bağlantısını oluştur
conn = sqlite3.connect('new_interview_questions1.db')
c = conn.cursor()

# Tek bir soru ve beklenen cevabı seç
soru = "What is the difference between abstract class and interface in Java?"
beklenen_cevap = "Abstract classes can have both abstract and concrete methods, while interfaces can only have abstract methods."

# FlagModel'i yükle
model = FlagModel('BAAI/bge-large-en-v1.5', 
                  query_instruction_for_retrieval="Generate representation for this sentence to retrieve relevant articles:",
                  use_fp16=True)

# Sorunun ve beklenen cevabın gömme vektörlerini oluştur
soru_gomme = model.encode([soru])
beklenen_cevap_gomme = model.encode([beklenen_cevap])

# Kullanıcıya soruyu göster
print("Soru:", soru)

# Kullanıcının cevabını al
kullanici_cevabi = input("Cevabınızı girin: ")

# Kullanıcının cevabının gömme vektörünü oluştur
kullanici_cevabi_vektor = model.encode([kullanici_cevabi])[0]

# Beklenen cevabın gömme vektörü ile kullanıcının cevabının benzerlik skorunu hesapla
benzerlik_skoru = np.dot(kullanici_cevabi_vektor, beklenen_cevap_gomme[0])

# Benzerlik skorunu ekrana yazdır
print("Benzerlik Skoru:", benzerlik_skoru)

# Veritabanı bağlantısını kapat
conn.close()
