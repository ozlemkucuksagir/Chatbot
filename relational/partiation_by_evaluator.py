import sqlite3

# Veritabanı bağlantıları
conn = sqlite3.connect('hr_chatbot.db')
c = conn.cursor()

# Veritabanı tablosunu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS interview_questions
             (id INTEGER PRIMARY KEY, job_title_id TEXT, skill_level_id TEXT, category_id TEXT, evaluator_id TEXT , question_type TEXT, language_id TEXT, question TEXT, answer TEXT)''')

# evaluator_id alanına göre bölme (partition)
c.execute('''CREATE TABLE IF NOT EXISTS interview_questions_by_evaluator
             (evaluator_id TEXT, id INTEGER, job_title_id TEXT, skill_level_id TEXT, category_id TEXT, question_type TEXT, language_id TEXT, question TEXT, answer TEXT,
             PRIMARY KEY (evaluator_id, id))''')

# Veriyi orijinal tablodan kopyalama ve partition tablosuna ekleme
c.execute('''INSERT INTO interview_questions_by_evaluator
             SELECT evaluator_id, id, job_title_id, skill_level_id, category_id, question_type, language_id, question, answer 
             FROM interview_questions''')

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()
