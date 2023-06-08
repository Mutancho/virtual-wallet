from database.connection import Database, init_db
from functools import wraps
from asyncmy.connection import Connection


async def read_query(conn: Connection, sql: str, sql_params=()) -> list:
    async with conn.cursor() as cursor:
        await cursor.execute(sql, sql_params)
        result = await cursor.fetchall()
    return result


async def insert_query(conn: Connection, sql: str, sql_params=()) -> int:
    async with conn.cursor() as cursor:
        await cursor.execute(sql, sql_params)
        return cursor.lastrowid


async def update_query(conn: Connection, sql: str, sql_params=()) -> bool:
    async with conn.cursor() as cursor:
        await cursor.execute(sql, sql_params)
        return cursor.rowcount


def manage_db_transaction(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if Database.pool is None:
            await init_db()
        async with Database.pool.acquire() as conn:
            try:
                result = await func(conn, *args, **kwargs)
                await conn.commit()
                return result
            except Exception as e:
                await conn.rollback()
                raise e

    return wrapper
