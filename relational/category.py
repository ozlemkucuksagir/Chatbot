import sqlite3

# Veritabanı bağlantısını oluştur
conn = sqlite3.connect('hr_chatbot.db')
cursor = conn.cursor()

# Tabloyu oluştur
cursor.execute('''CREATE TABLE categories(
                    id INTEGER PRIMARY KEY,
                    category TEXT
                )''')

# Verileri ekle
category = [
    ('Technical',),
    
]
cursor.executemany('INSERT INTO categories (category) VALUES (?)', category)

# Değişiklikleri kaydet ve bağlantıyı kapat
conn.commit()
conn.close()
