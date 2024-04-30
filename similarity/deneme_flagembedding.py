import sqlite3
from FlagEmbedding import FlagModel
import numpy as np
import nltk
from nltk.tokenize import word_tokenize



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
# Gömme vektörlerini kaydet
np.save("soru_gomme.npy", soru_gomme)
np.save("cevap_gomme.npy", cevap_gomme)


# Her bir soru için benzerlik puanlarını hesapla
for i, soru in enumerate(sorular):
    # Sorunun gömme vektörü
    soru_vektor = soru_gomme[i]
    
    # Tüm cevapların benzerlik skorlarını ölç
    benzerlikler = [np.dot(soru_vektor, cevap_vektor) for cevap_vektor in cevap_gomme]
    
    # En yüksek benzerlik skoruna sahip cevabı bul
    en_yuksek_benzerlik_index = np.argmax(benzerlikler)
    en_yuksek_benzerlik = benzerlikler[en_yuksek_benzerlik_index]
    en_yakin_cevap = beklenen_cevaplar[en_yuksek_benzerlik_index]
    
    # Benzerlik skorunu ve en yakın cevabı ekrana yazdır
    print("Soru:", soru)
    print("Beklenen Cevap:", en_yakin_cevap)
    print("Benzerlik Skoru:", en_yuksek_benzerlik)
    print("\n")

# Veritabanı bağlantısını kapat
conn.close()
