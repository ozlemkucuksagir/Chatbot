import sqlite3
from mediapipe.tasks import python
from mediapipe.tasks.python import text
import numpy as np
import tensorflow_hub as hub
import tensorflow as tf

# Bağlantı oluştur
conn = sqlite3.connect('interview_questions.db')
c = conn.cursor()

# TextEmbedder nesnesini oluşturun
base_options = python.BaseOptions(model_asset_path='C:/Users/okucuksagir/Desktop/chatbot/embedded/bert_embedder.tflite')
options = text.TextEmbedderOptions(base_options=base_options)
embedder = text.TextEmbedder.create_from_options(options)

# Kullanıcıdan metin girişi alın
user_input_text = input("Karşılaştırmak istediğiniz metni girin: ")

# Kullanıcının girdisini vektörize edin
user_input_embedding = embedder.embed(user_input_text)
user_input_embedding = user_input_embedding.embeddings[0]

# Veritabanındaki ilk satırın vektörünü alın
c.execute("SELECT vectorized_answer FROM new_interview_questions9 LIMIT 1")
row = c.fetchone()
if row:
    vectorized_answer_bytes = row[0]
    vectorized_answer_np = np.frombuffer(vectorized_answer_bytes, dtype='>f8')  # BLOB veriyi numpy dizisine dönüştür
    vectorized_answer_embedding  = python.components.containers.Embedding(vectorized_answer_np.astype(np.float64))     # Dönüşümü gerçekleştirme
     #vectorized_answer_embedding_float = quantized_to_float(vectorized_answer_embedding)
else:
    print("Veritabanında vektör bulunamadı.")
    conn.close()
    exit()

# Cosine similarity hesapla
similarity = text.TextEmbedder.cosine_similarity(user_input_embedding, vectorized_answer_embedding) 
print("Benzerlik:", similarity)

# Bağlantıyı kapat
conn.close()