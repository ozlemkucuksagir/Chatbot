import sqlite3
from mediapipe.tasks import python
from mediapipe.tasks.python import text
import numpy as np

# Bağlantı oluştur
conn = sqlite3.connect('interview_questions.db')
c = conn.cursor()

# Yeni tabloyu oluştur (Eğer daha önce oluşturmadıysanız)
c.execute('''CREATE TABLE IF NOT EXISTS new_interview_questions2
             (id INTEGER PRIMARY KEY, job_title TEXT, skill_level TEXT, category TEXT, evaluator TEXT, question_type TEXT, language TEXT, question TEXT, answer TEXT, vectorized_answer BLOB)''')

# TextEmbedder nesnesini oluşturun
base_options = python.BaseOptions(model_asset_path='C:/Users/okucuksagir/Desktop/chatbot/embedded/bert_embedder.tflite')
options = text.TextEmbedderOptions(base_options=base_options)
embedder = text.TextEmbedder.create_from_options(options)

# Veritabanındaki her bir cevabı döngüye alın
c.execute("SELECT * FROM interview_questions")
for row in c.fetchall():
    # Tüm sütun değerlerini alın
    answer_id, job_title, skill_level, category, evaluator, question_type, language, question, answer = row
    
    # Veritabanındaki verileri yeni tabloya ekleyin
    c.execute("INSERT INTO new_interview_questions2 (id, job_title, skill_level, category, evaluator, question_type, language, question, answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
              (answer_id, job_title, skill_level, category, evaluator, question_type, language, question, answer))
    
    # Cevabı vektörize edin
    answer_embedding = embedder.embed(answer)
    vectorized_answer = np.array(answer_embedding.embeddings[0])  # Embedding'i bir diziye dönüştürün
    
    # Vectorized answer'ı yeni tabloya ekleyin
    c.execute("UPDATE new_interview_questions2 SET vectorized_answer = ? WHERE id = ?", (vectorized_answer, answer_id))
    
    conn.commit()

# Bağlantıyı kaydet ve kapat
conn.close()

print("Veritabanındaki veriler başarıyla kopyalandı ve cevaplar vektörize edilerek yeni tabloya eklendi.")