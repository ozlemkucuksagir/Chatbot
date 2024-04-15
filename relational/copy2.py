import sqlite3

# Kaynak veritabanı bağlantısı
source_conn = sqlite3.connect('hr_chatbot.db')
source_cursor = source_conn.cursor()

# Hedef veritabanı bağlantısı
target_conn = sqlite3.connect('hr_chatbot.db')
target_cursor = target_conn.cursor()

# Kaynak tablo adı
source_table_name = 'interview_questions_new'

# Hedef tablo adı
target_table_name = 'interview_questions'

try:
    # Kaynak tablodaki verileri al
    source_cursor.execute(f"SELECT * FROM {source_table_name}")
    rows = source_cursor.fetchall()

    # Tablo yapısını al
    source_cursor.execute(f"PRAGMA table_info({source_table_name})")
    columns = source_cursor.fetchall()

    # Hedef tabloyu oluştur
    columns_str = ', '.join([f'{col[1]} {col[2]}' for col in columns])
    target_cursor.execute(f"CREATE TABLE IF NOT EXISTS {target_table_name} ({columns_str})")

    # Veriyi hedef tabloya kopyala
    for row in rows:
        placeholders = ', '.join(['?'] * len(row))
        target_cursor.execute(f"INSERT INTO {target_table_name} VALUES ({placeholders})", row)

    # Değişiklikleri kaydet
    target_conn.commit()

    print("Tablo başarıyla kopyalandı.")
except sqlite3.Error as e:
    print("Hata oluştu:", e)
finally:
    source_conn.close()
    target_conn.close()
