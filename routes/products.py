from fastapi import APIRouter, Depends, HTTPException
from auth import get_admin_user
from database import get_db_connection
from rate_limit import rate_limiter
from models.products import Membership, Class

router = APIRouter(
    dependencies=[Depends(rate_limiter)]
)

# Ürünleri listeleme endpoint'i
@router.get("/")
def list_products(admin_user: dict = Depends(get_admin_user)):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id, product_type, name, price, duration, description FROM products")
        products = cursor.fetchall()

        result = []
        for prod in products:
            product_dict = {
                "id": prod[0],
                "product_type": prod[1],
                "name": prod[2],
                "price": float(prod[3]),
                "duration": prod[4],
                "description": prod[5]
            }

            if prod[1] == "membership":
                result.append(Membership(**product_dict, duration_days=prod[4]))
            elif prod[1] == "class":
                result.append(Class(**product_dict, session_count=prod[4]))
            else:
                result.append(product_dict)  # Eğer bilinmeyen bir tip varsa direkt JSON olarak ekle

        return {"products": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# Yeni ürün ekleme endpoint'i (ID otomatik atanır, o yüzden "id" alanını kaldırdık)
@router.post("/")
def create_product(product: dict, admin_user: dict = Depends(get_admin_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO products (product_type, name, price, duration, description)
            VALUES (:product_type, :name, :price, :duration, :description)
        """, product)
        conn.commit()
        return {"msg": "Ürün başarıyla eklendi!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# Ürün güncelleme endpoint'i
@router.put("/{product_id}")
def update_product(product_id: int, updated_product: dict, admin_user: dict = Depends(get_admin_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE products SET
                product_type = :product_type,
                name = :name,
                price = :price,
                duration = :duration,
                description = :description
            WHERE id = :id
        """, {
            "id": product_id,
            **updated_product
        })
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı.")
        return {"msg": "Ürün başarıyla güncellendi!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# Ürün silme endpoint'i
@router.delete("/{product_id}")
def delete_product(product_id: int, admin_user: dict = Depends(get_admin_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE id = :id", {"id": product_id})
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı!")
        return {"msg": "Ürün başarıyla silindi!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
