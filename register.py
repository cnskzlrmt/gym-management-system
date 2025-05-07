# auth.py ya da ayrı bir register.py içinde
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import bcrypt
from database import get_db_connection

router = APIRouter()

class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone: str
    role: str  # Örneğin, "member"

@router.post("/register")
def register_user(request: RegisterRequest):
    # Şifreyi hashleyelim
    password_hash = bcrypt.hashpw(request.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Veritabanı bağlantısı ve stored procedure çağrısı
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Oracle için PL/SQL bloğu çalıştırma örneği:
        cursor.execute(
            """
            BEGIN
                sp_add_user(
                    p_first_name    => :first_name,
                    p_last_name     => :last_name,
                    p_email         => :email,
                    p_password_hash => :password_hash,
                    p_phone         => :phone,
                    p_role          => :role,
                    p_is_active     => 1
                );
            END;
            """,
            {
                "first_name": request.first_name,
                "last_name": request.last_name,
                "email": request.email,
                "password_hash": password_hash,
                "phone": request.phone,
                "role": request.role
            }
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Kayıt sırasında hata oluştu: " + str(e))
    finally:
        cursor.close()
        conn.close()

    return {"message": "Kayıt başarılı."}
