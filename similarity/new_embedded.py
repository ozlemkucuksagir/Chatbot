import sqlite3
from mediapipe.tasks import python
from mediapipe.tasks.python import text
import numpy as np

conn = sqlite3.connect('interview_questions.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS new_interview_questions9
             (id INTEGER PRIMARY KEY, job_title TEXT, skill_level TEXT, category TEXT, evaluator TEXT, question_type TEXT, language TEXT, question TEXT, answer TEXT, vectorized_answer BLOB)''')

base_options = python.BaseOptions(model_asset_path='C:/Users/okucuksagir/Desktop/chatbot/embedded/bert_embedder.tflite')
options = text.TextEmbedderOptions(base_options=base_options)
embedder = text.TextEmbedder.create_from_options(options)

c.execute("SELECT * FROM interview_questions")
for row in c.fetchall():
    answer_id, job_title, skill_level, category, evaluator, question_type, language, question, answer = row
    
    c.execute("INSERT INTO new_interview_questions9 (id, job_title, skill_level, category, evaluator, question_type, language, question, answer) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
              (answer_id, job_title, skill_level, category, evaluator, question_type, language, question, answer))
    
    # Cevabı vektörize edin
    answer_embedding = embedder.embed(answer)
    print(answer_embedding)
    print(answer_embedding.embeddings[0])
    vectorized_answer_np = answer_embedding.embeddings[0].embedding.astype('>f8') # Embedding'i bir diziye dönüştürün   
    vectorized_answer_bytes = vectorized_answer_np.tobytes()
    
    vectorized_answer_np = np.frombuffer(vectorized_answer_np, dtype=np.float32)   
    print(vectorized_answer_np.shape)

    c.execute("UPDATE new_interview_questions9 SET vectorized_answer = ? WHERE id = ?", (vectorized_answer_bytes, answer_id))
    
    conn.commit()

conn.close()

print("Veritabanındaki veriler başarıyla kopyalandı ve cevaplar vektörize edilerek yeni tabloya eklendi.")