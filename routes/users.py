from fastapi import APIRouter, Depends, HTTPException
from auth import get_current_user  # Hem admin hem de trainer için geçerli token'ı döndüren fonksiyon
from database import get_db_connection
from rate_limit import rate_limiter

router = APIRouter(
    dependencies=[Depends(rate_limiter)]
)

@router.get("/")
def list_users(current_user: dict = Depends(get_current_user)):
    """
    Bu endpoint, hem admin hem de trainer erişimine izin verir.
    Ancak, dönen kullanıcı listesi yalnızca role "member" olan kullanıcıları içerir.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, first_name, last_name, email 
            FROM users
            WHERE role = 'member'
        """)
        rows = cursor.fetchall()
        users = [{
            "id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "email": row[3]
        } for row in rows]
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
