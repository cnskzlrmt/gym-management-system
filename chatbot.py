import os
import json
import re
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from auth import get_current_user
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain  # Deprecated uyarısı veriyor; şimdilik kullanıyoruz

# 🌍 Ortam değişkenlerini yükle
load_dotenv()

# 🔑 Veritabanı bağlantı bilgileri
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "1521")
DB_USER = os.getenv("DB_USER", "GYM_ADMIN")
DB_PASS = os.getenv("DB_PASS", "gym123")
DB_SID  = os.getenv("DB_SID", "XE")

# 📌 SQLDatabase URI'sini oluştur ve veritabanına bağlan
database_uri = f"oracle+oracledb://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_SID}"
db = SQLDatabase.from_uri(database_uri)
print("Oluşturulan URI:", database_uri)

# Şema bilgilerini SQLDatabase üzerinden çekelim
try:
    tables = db.get_usable_table_names()  # Yeni metot kullanılıyor
    schema_info = {}
    for table in tables:
        # Her tablo için sütun listesini Oracle sistem görünümünden çekiyoruz
        query = f"SELECT column_name FROM all_tab_columns WHERE table_name = UPPER('{table}')"
        results = db.run(query)
        columns = [row[0] for row in results]
        schema_info[table] = columns
    schema_json = json.dumps(schema_info, ensure_ascii=False, indent=2)
    print("🔍 Öğretilen Şema:", schema_json)
except Exception as e:
    print("❌ Şema bilgileri çekilemedi:", e)
    schema_info = {}
    schema_json = json.dumps(schema_info, ensure_ascii=False, indent=2)

# ✅ FastAPI Router oluştur
router = APIRouter()

# 🧠 OpenAI API Anahtarını Al ve Modeli Başlat
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise Exception("❌ OPENAI_API_KEY bulunamadı! Lütfen .env dosyanıza ekleyin.")
llm = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)

# 📌 Custom Prompt Tanımı
custom_prompt = PromptTemplate(
    input_variables=["query", "schema_info"],
    template="""
Aşağıda Oracle veritabanının şeması ve sütun bilgileri verilmiştir (lütfen yalnızca bu şemada yer alan tablo ve sütun adlarını kullanın):
{schema_info}

Kullanıcının sorgusuna uygun bir SQL sorgusu üret:
Soru: {query}

Kurallar:
- Yalnızca yukarıdaki şema bilgisinde yer alan tablo adlarını kullanın. Örneğin, eğer sorguda "ürün" ifadesi geçiyorsa, doğru tablo adı (örneğin, "PRODUCTS") kullanılmalıdır.
- WHERE koşulunda, tablo adını değil, ilgili sütun adını kullanın (örneğin, "NAME" veya "PRODUCT_NAME").
- Sadece geçerli ve optimize edilmiş Oracle SQL sorguları üret.
- DDL (CREATE, DROP, ALTER) sorguları üretme.
- DELETE veya UPDATE sorguları oluşturma.
- Tüm tablo ve sütun isimlerini büyük harf ile yaz.
- Oracle sözdizimine uygun sorgu üret.
- NULL değerleri kontrol et, NULL olan kayıtları ihmal etme.
    """
)

# LLMChain oluştur (deprecated uyarısı alınsa da çalışacaktır)
llm_chain = LLMChain(llm=llm, prompt=custom_prompt)
print("Zincirin input_keys:", llm_chain.prompt.input_variables)

# Helper: LLMChain çıktısını temizleyen fonksiyon
def parse_sql_output(llm_output: str) -> str:
    # Önce, kod bloğu içindeki SQL sorgusunu ayıkla (örneğin, ```sql ... ```)
    match = re.search(r"```(?:sql)?\s*(.*?)\s*```", llm_output, re.DOTALL | re.IGNORECASE)
    if match:
        sql = match.group(1).strip()
    else:
        sql = re.sub(r"^(SQL Sorgusu:|Yanıt:)\s*", "", llm_output, flags=re.IGNORECASE).strip()
    
    # Gereksiz açıklama satırlarını temizle: SELECT, FROM, WHERE, AND, ORDER, GROUP, HAVING, UNION, INTERSECT, EXCEPT, 
    # ve JOIN ifadelerini de dahil ediyoruz.
    lines = sql.splitlines()
    cleaned_lines = []
    pattern = r"^(SELECT|FROM|WHERE|AND|ORDER|GROUP|HAVING|UNION|INTERSECT|EXCEPT|(?:(?:INNER|LEFT|RIGHT|FULL)\s+)?JOIN|ON)\b"
    for line in lines:
        line_strip = line.strip()
        if re.match(pattern, line_strip, re.IGNORECASE):
            cleaned_lines.append(line_strip)
        else:
            # Eğer satır önemli bir bilgi içeriyorsa, isteğe bağlı ekleyebilirsiniz.
            # Örneğin, satır boş değilse ekleyebilirsiniz:
            if line_strip != "":
                cleaned_lines.append(line_strip)
    if cleaned_lines:
        sql = "\n".join(cleaned_lines)
    else:
        sql = sql.strip()
    
    # "FETCH FIRST ... ROWS ONLY" ifadesini kaldır (varsa)
    sql = re.sub(r"FETCH FIRST\s+\d+\s+ROWS ONLY", "", sql, flags=re.IGNORECASE).strip()
    
    # Trailing noktalı virgülü kaldır
    if sql.endswith(";"):
        sql = sql[:-1].strip()
    return sql

# Helper: SQL sorgusundaki çift tırnakları kaldıran fonksiyon
def adjust_case(query: str) -> str:
    return query.replace('"', '')

# SQL sorgusunu çalıştıran fonksiyon (SQLDatabase üzerinden)
def execute_sql_query(query: str):
    try:
        print("Çalıştırılan SQL Sorgusu:", query)
        adjusted_query = adjust_case(query)
        results = db.run(adjusted_query)
        return results
    except Exception as e:
        raise Exception(f"SQL sorgusu çalıştırılırken hata: {str(e)}")

# 📌 Kullanıcıdan gelen istek modeli
class ChatRequest(BaseModel):
    question: str

@router.post("/")
def process_chat(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    try:
        user_input = request.question.strip()
        print("📩 Kullanıcı Sorusu:", user_input)
        
        # LLMChain'i çalıştırarak SQL sorgusunu üret
        llm_output = llm_chain.run(query=user_input, schema_info=schema_json)
        print("Ham LLMChain çıktısı:", llm_output)
        
        # Üretilen çıktıyı temizleyip geçerli SQL sorgusuna dönüştür
        sql_query = parse_sql_output(llm_output)
        sql_query = adjust_case(sql_query)
        print("Parse edilmiş SQL Sorgusu:", sql_query)
        
        # SQL sorgusunu çalıştır
        results = execute_sql_query(sql_query)
        print("SQL Sonuçları:", results)
        
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Bir hata oluştu: {str(e)}")
