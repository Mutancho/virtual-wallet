import asyncio
import asyncmy
from config.config import settings


class Database:
    pool = None


async def init_db():
    attempts = 0
    while attempts < 5:
        try:
            Database.pool = await asyncmy.create_pool(
                host=settings.database_hostname,
                port=settings.database_port,
                user=settings.database_username,
                password=settings.database_password,
                db=settings.database_name,
                minsize=1,  # Minimum number of connections in the pool
                maxsize=10,  # Maximum number of connections in the pool
            )
            return Database.pool
        except Exception as e:
            print(f"Failed to connect to database. Exception: {e}")
            attempts += 1
            await asyncio.sleep(5)
    raise Exception("Could not connect to the database after max retries")


async def get_connection():
    if Database.pool is None:
        await init_db()
    # acquire a single connection from the pool
    async with Database.pool.acquire() as conn:
        return conn
