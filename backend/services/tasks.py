import datetime
import asyncio
from database.database_queries import read_query,update_query,insert_query
from schemas.transaction_models import Transaction, DisplayTransaction, DisplayTransactionInfo,PendingTransaction


async def execute_recurring_transactions():
    data = await read_query('''SELECT amount,category,recipient_id,wallet_id,is_recurring FROM transactions WHERE is_recurring = 1 and id in 
    (SELECT transaction_id FROM recurring_transactions  WHERE next_occurrence = DATE(NOW()))''')
    for t in data:
        transaction = Transaction.from_query_result(*t)
        await insert_query('''INSERT INTO transactions(amount, is_recurring, recipient_id, category, wallet_id) VALUES (%s,%s,%s,%s,%s)''',
                           (transaction.amount,transaction.is_recurring,int(transaction.recipient),transaction.category,int(transaction.wallet)))

        print(transaction)



async def is_within_time_period(start_time, end_time):
    now = datetime.datetime.now().time()
    return start_time <= now <= end_time


async def schedule_task():
    while True:
        # Calculate the time for the next execution
        current_time = datetime.datetime.now().time()
        next_execution_time = datetime.datetime.combine(
            datetime.datetime.now().date() + datetime.timedelta(days=1),
            current_time
        )

        # Calculate the duration until the next execution
        duration = (next_execution_time - datetime.datetime.now()).total_seconds()

        # Sleep until the next execution
        await asyncio.sleep(duration)

        # Execute the task
        await execute_recurring_transactions()


def run_task_scheduler():
    asyncio.run(schedule_task())
