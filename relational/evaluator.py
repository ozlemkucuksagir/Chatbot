import sqlite3

# Veritabanı bağlantısını oluştur
conn = sqlite3.connect('hr_chatbot.db')
cursor = conn.cursor()

# Tabloyu oluştur
cursor.execute('''CREATE TABLE evaluator(
                    id INTEGER PRIMARY KEY,
                    evaluator_name TEXT
                )''')

# Verileri ekle
evaluator_type = [
    ('App',),
    ('Expert',)
]
cursor.executemany('INSERT INTO evaluator (evaluator_name) VALUES (?)', evaluator_type)

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()
