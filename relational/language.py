import sqlite3

# Veritabanı bağlantısını oluştur
conn = sqlite3.connect('hr_chatbot.db')
cursor = conn.cursor()

# Tabloyu oluştur
cursor.execute('''CREATE TABLE language(
                    id INTEGER PRIMARY KEY,
                    language TEXT
                )''')

# Verileri ekle
languages = [
    ('ENG (US)',)
]
cursor.executemany('INSERT INTO language (language) VALUES (?)', languages)

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()
