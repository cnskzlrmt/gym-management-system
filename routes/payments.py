from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from auth import get_admin_user
from database import get_db_connection
from rate_limit import rate_limiter

router = APIRouter(
    dependencies=[Depends(rate_limiter)]
)

# Tüm ödemeleri listeleme endpoint'i (Admin)
@router.get("/")
def list_payments(admin_user: dict = Depends(get_admin_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, user_id, product_id, amount, payment_date, status
            FROM payments
        """)
        rows = cursor.fetchall()
        payments = [{
            "id": row[0],
            "user_id": row[1],
            "product_id": row[2],
            "amount": float(row[3]),
            "payment_date": row[4].isoformat() if row[4] else None,
            "status": row[5]
        } for row in rows]
        return {"payments": payments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Yeni ödeme ekleme endpoint'i (Admin)
@router.post("/")
def create_payment(payment: dict, admin_user: dict = Depends(get_admin_user)):
    # Eğer payment_date alanı gönderilmemişse veya boş ise, kaldırıyoruz.
    if "payment_date" in payment:
        payment.pop("payment_date")
    query = """
        INSERT INTO payments (user_id, product_id, amount, status)
        VALUES (:user_id, :product_id, :amount, :status)
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query, payment)
        conn.commit()
        return {"msg": "Ödeme başarıyla eklendi!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Ödeme güncelleme endpoint'i (Admin)
@router.put("/{payment_id}")
def update_payment(payment_id: int, updated_payment: dict, admin_user: dict = Depends(get_admin_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Dinamik olarak güncellenecek alanları belirleyelim
        fields = []
        params = {"id": payment_id}

        if "user_id" in updated_payment:
            fields.append("user_id = :user_id")
            params["user_id"] = updated_payment["user_id"]

        if "product_id" in updated_payment:
            fields.append("product_id = :product_id")
            params["product_id"] = updated_payment["product_id"]

        if "amount" in updated_payment:
            fields.append("amount = :amount")
            params["amount"] = updated_payment["amount"]

        if "status" in updated_payment:
            fields.append("status = :status")
            params["status"] = updated_payment["status"]

        if "payment_date" in updated_payment:
            pd = updated_payment["payment_date"]
            if pd and pd.strip() != "":
                try:
                    dt = datetime.strptime(pd.strip(), "%Y-%m-%d")
                    fields.append("payment_date = :payment_date")
                    params["payment_date"] = dt
                except Exception as e:
                    # Eğer tarih formatı uygun değilse, alanı eklemiyoruz.
                    pass

        if not fields:
            raise HTTPException(status_code=400, detail="Güncellenecek geçerli alan bulunamadı.")

        query = "UPDATE payments SET " + ", ".join(fields) + " WHERE id = :id"
        cursor.execute(query, params)
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Ödeme bulunamadı.")
        return {"msg": "Ödeme başarıyla güncellendi!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

# Ödeme silme endpoint'i (Admin)
@router.delete("/{payment_id}")
def delete_payment(payment_id: int, admin_user: dict = Depends(get_admin_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM payments WHERE id = :id", {"id": payment_id})
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Ödeme bulunamadı.")
        return {"msg": "Ödeme başarıyla silindi!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
