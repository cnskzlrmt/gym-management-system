from fastapi import APIRouter, Depends, HTTPException
from auth import get_member_user
from database import get_db_connection
from rate_limit import rate_limiter

router = APIRouter(
    dependencies=[Depends(rate_limiter)]
)

# Kendi ödeme bilgilerini görme
@router.get("/payments")
def my_payments(member_user: dict = Depends(get_member_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, amount, payment_date, status
            FROM payments
            WHERE user_id = :user_id
        """, {"user_id": member_user["id"]})
        payments = cursor.fetchall()
        result = [{
            "id": p[0],
            "amount": float(p[1]),
            "payment_date": p[2].isoformat() if p[2] else None,
            "status": p[3]
        } for p in payments]
        return {"payments": result}
    finally:
        cursor.close()
        conn.close()

# Kendi workout programını görme
@router.get("/workout-program")
def my_workout_program(member_user: dict = Depends(get_member_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, trainer_id, name, description, created_at
            FROM workout_programs
            WHERE user_id = :user_id
        """, {"user_id": member_user["id"]})
        
        programs = cursor.fetchall()
        result = []
        for prog in programs:
            result.append({
                "id": prog[0],
                "trainer_id": prog[1],
                "name": prog[2],
                "description": prog[3].read() if prog[3] else None,
                "created_at": prog[4].isoformat() if prog[4] else None
            })
        return {"workout_programs": result}
    finally:
        cursor.close()
        conn.close()

# ➜ Yeni: Kendi profil bilgilerini getirme endpoint'i
@router.get("/profile")
def get_member_profile(member_user: dict = Depends(get_member_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, first_name, last_name, email, phone, is_active
            FROM users
            WHERE id = :id
        """, {"id": member_user["id"]})
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı.")
        return {
            "id": user[0],
            "first_name": user[1],
            "last_name": user[2],
            "email": user[3],
            "phone": user[4],
            "is_active": bool(user[5])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()
