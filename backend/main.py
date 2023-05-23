from database.connection import init_db, get_connection
from fastapi import FastAPI
from routers.referrals import referrals_router
from routers.users import users_router
from routers.cards import cards_router
from routers.transfers import transfers_router
from routers.wallets import wallets_router
from routers.contacts import contacts_router
from routers.transactions import transactions_router

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.on_event("shutdown")
async def shutdown_event():
    pool = await get_connection()
    await pool.close()


app.include_router(users_router)
app.include_router(cards_router)
app.include_router(transfers_router)
app.include_router(wallets_router)
app.include_router(contacts_router)
app.include_router(referrals_router)
app.include_router(transactions_router)
