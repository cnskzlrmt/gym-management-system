# database.py
import os
import oracledb
from fastapi import HTTPException

# Ortam değişkenlerini al
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1521")
DB_USER = os.getenv("DB_USER", "GYM_ADMIN")
DB_PASS = os.getenv("DB_PASS", "gym123")
DB_SID  = os.getenv("DB_SID", "XE")
dsn = f"{DB_HOST}:{DB_PORT}/{DB_SID}"

# Oracle veritabanı bağlantısı oluşturma
def get_db_connection():
    try:
        connection = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=dsn)
        return connection
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection error: " + str(e))
