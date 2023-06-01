from database.database_queries import insert_query


async def update_transfers_db(type: str, amount: str, wallet_id: int):
    await insert_query("INSERT INTO transfers(type,amount, wallet_id) VALUES(%s,%s,%s)",
                       (type, float(amount), wallet_id))
