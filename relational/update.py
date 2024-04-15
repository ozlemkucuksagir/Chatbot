import sqlite3

# Veritabanı bağlantıları
conn = sqlite3.connect('hr_chatbot.db')
cursor = conn.cursor()

try:
    # questions2 tablosundaki evaluator sütununu evaluator tablosundaki evaluator_type_name ile eşleşen id değerleriyle güncelle
    cursor.execute("""
        UPDATE questions3new
        SET evaluator = (
            SELECT id FROM evaluator
            WHERE evaluator.evaluator_type_name = questions3new.evaluator
        )
    """)

    # Değişiklikleri kaydet
    conn.commit()

    print("Veriler başarıyla güncellendi.")
except sqlite3.Error as e:
    print("Hata oluştu:", e)
finally:
    conn.close()
