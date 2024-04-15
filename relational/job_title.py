import sqlite3

# Veritabanı bağlantısını oluştur
conn = sqlite3.connect('hr_chatbot.db')
cursor = conn.cursor()

# Tabloyu oluştur
cursor.execute('''CREATE TABLE job_titles(
                    id INTEGER PRIMARY KEY,
                    job_title_name TEXT
                )''')

# Verileri ekle
job_titles=[('Java Developer',),
            ('Software Engineer',),
('Software Developer',),
('Front End Developer',),
('Network Engineer',),
('Android Developer',),
('Salesforce Developer',),
('IOS Developer',),
('SQL Developer',),
('.NET Developer',),
('Python Developer',),
('Game Developer',),
('Data Engineer',),
('Full Stack Developer',),
('React Developer',),
('UI Developer',)]

cursor.executemany('INSERT INTO job_titles (job_title_name) VALUES (?)', job_titles)

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()
