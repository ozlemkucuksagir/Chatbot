import sqlite3
from FlagEmbedding import FlagModel
import random
import numpy as np
# Veritabanı bağlantısını oluştur
conn = sqlite3.connect('new_interview_questions1.db')
c = conn.cursor()

# Kullanıcıya sorulacak soruları ve HR'nin beklenen cevaplarını veritabanından al
c.execute("SELECT question, answer FROM interview_questions LIMIT 20")
sorular_cevaplar = c.fetchall()

# Sorular ve cevaplar listelerini ayır
sorular = [soru for soru, _ in sorular_cevaplar]
beklenen_cevaplar = [cevap for _, cevap in sorular_cevaplar]

# FlagModel'i yükle
model = FlagModel('BAAI/bge-large-en-v1.5', 
                  query_instruction_for_retrieval="Generate representation for this sentence to retrieve relevant articles:",
                  use_fp16=True)

# Soruların gömme vektörlerini oluştur
soru_gomme = model.encode(sorular)

# Cevapların gömme vektörlerini oluştur
cevap_gomme = model.encode(beklenen_cevaplar)

# Rastgele bir soru seç
secilen_soru_index = random.randint(0, len(sorular) - 1)
secilen_soru = sorular[secilen_soru_index]

# Kullanıcıya soruyu göster
print("Soru:", secilen_soru)

# Kullanıcının cevabını al
kullanici_cevabi = input("Cevabınızı girin: ")

# Kullanıcının cevabının gömme vektörünü oluştur
kullanici_cevabi_vektor = model.encode([kullanici_cevabi])[0]

# Beklenen cevapların gömme vektörleri ile kullanıcının cevabının benzerlik skorlarını hesapla
benzerlikler = [np.dot(kullanici_cevabi_vektor, cevap_vektor) for cevap_vektor in cevap_gomme]

# En yüksek benzerlik skoruna sahip beklenen cevabı bul
en_yuksek_benzerlik_index = np.argmax(benzerlikler)
en_yuksek_benzerlik = benzerlikler[en_yuksek_benzerlik_index]
en_yakin_cevap = beklenen_cevaplar[en_yuksek_benzerlik_index]

# Benzerlik skorunu ve en yakın beklenen cevabı ekrana yazdır
print("Beklenen Cevap:", en_yakin_cevap)
print("Benzerlik Skoru:", en_yuksek_benzerlik)

# Veritabanı bağlantısını kapat
conn.close()
