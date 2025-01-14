from fastapi.middleware.cors import CORSMiddleware
from database.connection import init_db
from fastapi import FastAPI
from routers.referrals import referrals_router
from routers.users import users_router
from routers.cards import cards_router
from routers.transfers import transfers_router
from routers.wallets import wallets_router
from routers.contacts import contacts_router
from routers.transactions import transactions_router
import threading
from services.tasks import run_task_scheduler
from database.connection import Database

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_db()
    thread = threading.Thread(target=run_task_scheduler)
    thread.start()


@app.on_event("shutdown")
async def shutdown_event():
    if Database.pool is not None:
        Database.pool.close()
        await Database.pool.wait_closed()


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://frontend:3000",
    "http://frontend:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(cards_router)
app.include_router(transfers_router)
app.include_router(wallets_router)
app.include_router(contacts_router)
app.include_router(referrals_router)
app.include_router(transactions_router)
