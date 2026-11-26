from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import Currency
from app.schemas import Currency as CurrencySchema
from app.services.cbr_service import fetch_currencies_from_cbr

router = APIRouter()

@router.get("/", response_model=list[CurrencySchema])
async def get_currencies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Currency))
    return result.scalars().all()

@router.post("/update", status_code=200)
async def update_currencies(db: AsyncSession = Depends(get_db)):
    currencies_data = await fetch_currencies_from_cbr()
    for code, name, _ in currencies_data:
        existing = await db.execute(select(Currency).where(Currency.code == code))
        currency = existing.scalar_one_or_none()
        if currency:
            if currency.name != name:
                currency.name = name
        else:
            db.add(Currency(code=code, name=name))
    await db.commit()
    return {"message": "Currencies updated successfully"}

@router.get("/{currency_code}/rate")
async def get_rate(currency_code: str, db: AsyncSession = Depends(get_db)):
    currencies_data = await fetch_currencies_from_cbr()
    for code, _, value in currencies_data:
        if code == currency_code.upper():
            return {"currency_code": code, "rate": value}
    raise HTTPException(404, "Currency not found")