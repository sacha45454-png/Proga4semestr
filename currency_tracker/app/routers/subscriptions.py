from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User, Currency, subscription
from app.schemas import SubscriptionRequest

router = APIRouter()

@router.post("/", status_code=201)
async def subscribe(sub_data: SubscriptionRequest, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, sub_data.user_id)
    if not user:
        raise HTTPException(404, "User not found")
    currency = await db.execute(select(Currency).where(Currency.code == sub_data.currency_code))
    currency = currency.scalar_one_or_none()
    if not currency:
        raise HTTPException(404, "Currency not found")
    existing = await db.execute(select(subscription).where(
        subscription.c.user_id == user.id,
        subscription.c.currency_id == currency.id
    ))
    if existing.first():
        raise HTTPException(409, "Already subscribed")
    await db.execute(subscription.insert().values(user_id=user.id, currency_id=currency.id))
    await db.commit()
    return {"message": "Subscribed"}

@router.delete("/", status_code=204)
async def unsubscribe(sub_data: SubscriptionRequest, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, sub_data.user_id)
    if not user:
        raise HTTPException(404, "User not found")
    currency = await db.execute(select(Currency).where(Currency.code == sub_data.currency_code))
    currency = currency.scalar_one_or_none()
    if not currency:
        raise HTTPException(404, "Currency not found")
    await db.execute(subscription.delete().where(
        subscription.c.user_id == user.id,
        subscription.c.currency_id == currency.id
    ))
    await db.commit()