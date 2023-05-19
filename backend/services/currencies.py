from database.database_queries import read_query


async def select_currency(currency: str):
    get_currency_id = await read_query("SELECT id FROM currencies WHERE currency=%s", (currency.upper(),))
    return get_currency_id
