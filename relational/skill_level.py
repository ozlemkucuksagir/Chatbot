import sqlite3

# Veritabanı bağlantısını oluştur
conn = sqlite3.connect('hr_chatbot.db')
cursor = conn.cursor()

# Tabloyu oluştur
cursor.execute('''CREATE TABLE skill_level(
                    id INTEGER PRIMARY KEY,
                    skill_level_name TEXT
                )''')

# Verileri ekle
levels = [
    ('Junior',),
    ('Mid-level',),
    ('Senior',)
]
cursor.executemany('INSERT INTO skill_level (skill_level_name) VALUES (?)', levels)

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()
