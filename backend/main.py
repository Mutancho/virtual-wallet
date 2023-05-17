from fastapi import FastAPI
from routers.users import users_router

from database.connection import init_db, get_connection

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_db()


@app.on_event("shutdown")
async def shutdown_event():
    pool = await get_connection()
    await pool.close()


app.include_router(users_router)