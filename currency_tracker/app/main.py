from fastapi import FastAPI
from app.routers import users, currencies, subscriptions
from app.database import engine, Base

app = FastAPI(title="Currency Tracker API")

@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(currencies.router, prefix="/currencies", tags=["currencies"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])