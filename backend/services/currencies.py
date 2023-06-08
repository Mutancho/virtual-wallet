from database.database_queries import read_query
from asyncmy.connection import Connection


async def select_currency(conn: Connection, currency: str):
    get_currency_id = await read_query(conn, "SELECT id FROM currencies WHERE currency=%s", (currency.upper(),))
    return get_currency_id


async def get_all_currencies(conn: Connection):
    get_currencies = read_query(conn, "SELECT * FROM currencies")
    return get_currencies
