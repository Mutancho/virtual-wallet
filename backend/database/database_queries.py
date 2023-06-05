from database.connection import Database, init_db


async def read_query(sql: str, sql_params=()) -> list:
    if Database.pool is None:
        await init_db()
    async with Database.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(sql, sql_params)
            result = await cur.fetchall()
    return result


async def insert_query(sql: str, sql_params=()) -> int:
    if Database.pool is None:
        await init_db()
    async with Database.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql, sql_params)
            await conn.commit()
            return cursor.lastrowid


async def update_query(sql: str, sql_params=()) -> bool:
    if Database.pool is None:
        await init_db()
    async with Database.pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(sql, sql_params)
            await conn.commit()
            return cursor.rowcount


