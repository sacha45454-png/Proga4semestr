from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class UserCreate(BaseModel):
    username: str
    email: EmailStr

class UserUpdate(BaseModel):
    email: EmailStr

class CurrencyBase(BaseModel):
    code: str
    name: str

class Currency(CurrencyBase):
    id: int
    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    currencies: List[Currency] = []

    class Config:
        from_attributes = True

class SubscriptionRequest(BaseModel):
    user_id: int
    currency_code: str