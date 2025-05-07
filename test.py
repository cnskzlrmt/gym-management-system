import oracledb
import os

# Ortam değişkenlerini oku
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1521")
DB_USER = os.getenv("DB_USER", "GYM_ADMIN")
DB_PASS = os.getenv("DB_PASS", "gym123")
DB_SID  = os.getenv("DB_SID", "XE")

# DSN oluştur
dsn = f"{DB_HOST}:{DB_PORT}/{DB_SID}"

try:
    # Bağlantıyı dene
    print("🔄 Veritabanına bağlanılıyor...")
    connection = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=dsn)
    cursor = connection.cursor()
    print("✅ BAĞLANTI BAŞARILI!")

    # Tüm tabloları listele
    print("\n📌 Tablolar Listesi:")
    cursor.execute("SELECT table_name FROM all_tables WHERE owner = UPPER(:owner)", {"owner": DB_USER})
    tables = cursor.fetchall()

    if tables:
        table_names = [table[0] for table in tables]
        print("🗂️ Bulunan Tablolar:", table_names)
    else:
        print("⚠️ HİÇ TABLO BULUNAMADI!")

except oracledb.DatabaseError as e:
    print(f"❌ BAĞLANTI HATASI: {e}")

finally:
    if 'connection' in locals():
        connection.close()
