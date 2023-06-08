from database.database_queries import insert_query, manage_db_transaction
from asyncmy.connection import Connection


@manage_db_transaction
async def update_transfers_db(conn: Connection, type: str, amount: str, wallet_id: int):
    await insert_query(conn, "INSERT INTO transfers(type,amount, wallet_id) VALUES(%s,%s,%s)",
                       (type, float(amount), wallet_id))
