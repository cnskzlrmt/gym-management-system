from pydantic import BaseModel
from typing import Optional

class Product(BaseModel):
    id: int
    name: str
    price: float
    description: Optional[str] = None

class Membership(Product):
    duration_days: int  # üyelik süresi gün bazında

class Class(Product):
    session_count: int  # ders sayısı
