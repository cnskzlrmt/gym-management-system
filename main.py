from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Modüllerin import edilmesi
from auth import router as auth_router
from routes import products, workout_programs, member, payments, users # payments modülü ekleniyor
from database import get_db_connection
from register import router as register_router
from chatbot import router as chatbot_router




app = FastAPI(
    title="Gym Membership Management API",
    description="API for managing gym memberships, products, and workout programs with JWT authentication and role-based access control.",
    version="1.0.0"
)

# CORS Middleware (frontend erişimi için)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Gerekirse frontend domain'lerini ekleyin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Kök endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Gym Membership Management API"}

# Veritabanı bağlantısını test eden endpoint
@app.get("/db-test")
def db_test():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM DUAL")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return {"result": result}

# API Endpointlerinin dahil edilmesi
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(workout_programs.router, prefix="/workout-programs", tags=["Workout Programs"])
app.include_router(member.router, prefix="/member", tags=["Member"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])  # Payments router eklendi
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(register_router, prefix="/auth", tags=["Authentication"])
app.include_router(chatbot_router, prefix="/chatbot", tags=["Chatbot"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
