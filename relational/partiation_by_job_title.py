import sqlite3

# Veritabanı bağlantıları
conn = sqlite3.connect('hr_chatbot.db')
c = conn.cursor()

# Veritabanı tablosunu oluşturma
c.execute('''CREATE TABLE IF NOT EXISTS interview_questions
             (id INTEGER PRIMARY KEY, job_title_id TEXT, skill_level_id TEXT, category_id TEXT, evaluator_id TEXT , question_type TEXT, language_id TEXT, question TEXT, answer TEXT)''')

# job_title_id alanına göre bölme (partition)
c.execute('''CREATE TABLE IF NOT EXISTS interview_questions_by_job_title
             (job_title_id TEXT, id INTEGER, skill_level_id TEXT, category_id TEXT, evaluator_id TEXT , question_type TEXT, language_id TEXT, question TEXT, answer TEXT,
             PRIMARY KEY (job_title_id, id))''')

# Veriyi orijinal tablodan kopyalama ve partition tablosuna ekleme
c.execute('''INSERT INTO interview_questions_by_job_title 
             SELECT job_title_id, id, skill_level_id, category_id, evaluator_id, question_type, language_id, question, answer 
             FROM interview_questions''')

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()
