from fastapi import APIRouter, Depends, HTTPException
from auth import get_admin_or_trainer_user
from database import get_db_connection
from rate_limit import rate_limiter
from datetime import datetime

router = APIRouter(
    dependencies=[Depends(rate_limiter)]
)

@router.get("/")
def list_workout_programs(user: dict = Depends(get_admin_or_trainer_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if user["role"] == "admin":
            cursor.execute("SELECT id, user_id, trainer_id, name, description, created_at FROM workout_programs")
        else:
            cursor.execute("""
                SELECT id, user_id, trainer_id, name, description, created_at 
                FROM workout_programs 
                WHERE trainer_id = :trainer_id
            """, {"trainer_id": user["id"]})

        programs = cursor.fetchall()
        result = []
        for prog in programs:
            result.append({
                "id": prog[0],
                "user_id": prog[1],
                "trainer_id": prog[2],
                "name": prog[3],
                "description": prog[4].read() if prog[4] else None,
                "created_at": prog[5].isoformat() if prog[5] else None
            })
        return {"workout_programs": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.post("/")
def create_workout_program(program: dict, user: dict = Depends(get_admin_or_trainer_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # ID alanını kaldırdık; Oracle trigger id'yi otomatik atayacak.
        cursor.execute("""
            INSERT INTO workout_programs (user_id, trainer_id, name, description, created_at)
            VALUES (:user_id, :trainer_id, :name, :description, :created_at)
        """, {
            "user_id": program["user_id"],
            "trainer_id": user["id"] if user["role"] == "trainer" else program["trainer_id"],
            "name": program["name"],
            "description": program.get("description", ""),
            "created_at": datetime.now()
        })
        conn.commit()
        return {"message": "Workout programı başarıyla eklendi!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.put("/{program_id}")
def update_workout_program(program_id: int, updated_program: dict, user: dict = Depends(get_admin_or_trainer_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if user["role"] == "trainer":
            cursor.execute("""
                UPDATE workout_programs SET
                    user_id = :user_id,
                    name = :name,
                    description = :description
                WHERE id = :id AND trainer_id = :trainer_id
            """, {
                "user_id": updated_program["user_id"],
                "name": updated_program["name"],
                "description": updated_program.get("description", ""),
                "id": program_id,
                "trainer_id": user["id"]
            })
        else:  # admin ise
            cursor.execute("""
                UPDATE workout_programs SET
                    user_id = :user_id,
                    trainer_id = :trainer_id,
                    name = :name,
                    description = :description
                WHERE id = :id
            """, {
                "user_id": updated_program["user_id"],
                "trainer_id": updated_program["trainer_id"],
                "name": updated_program["name"],
                "description": updated_program.get("description", ""),
                "id": program_id
            })
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Workout programı bulunamadı veya yetkiniz yok.")
        return {"message": "Workout programı başarıyla güncellendi!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()


@router.delete("/{program_id}")
def delete_workout_program(program_id: int, user: dict = Depends(get_admin_or_trainer_user)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if user["role"] == "admin":
            cursor.execute("DELETE FROM workout_programs WHERE id = :id", {"id": program_id})
        else:
            cursor.execute("DELETE FROM workout_programs WHERE id = :id AND trainer_id = :trainer_id", {"id": program_id, "trainer_id": user["id"]})
        conn.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Workout programı bulunamadı veya yetkiniz yok.")
        return {"message": "Workout programı başarıyla silindi!"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()
