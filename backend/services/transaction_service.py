from database.database_queries import read_query,update_query,insert_query
from utils import oauth2,send_emails
from schemas.transaction_models import Transaction,DisplayTransaction
from datetime import date,datetime

async def create_transaction(transaction,token):
    user_id = oauth2.get_current_user(token)
    if not transaction.category:
        transaction.category = 'Other'
    if not transaction.is_recurring:
        transaction.is_recurring = False

    transaction_id = await insert_query('''INSERT INTO transactions(amount, is_recurring, recipient_id, category, wallet_id) VALUES(%s,%s,%s,%s,%s)''',
                       (transaction.amount,transaction.is_recurring,transaction.recipient,transaction.category,transaction.wallet))
    if transaction.amount <= 10000:
        recepient_email = await read_query('''SELECT email FROM users WHERE id = %s''',(transaction.recipient,))
        await acceptence_email(transaction_id,recepient_email[0][0])
    else:
        user_email = await read_query('''SELECT email FROM users WHERE id = %s''',(user_id,))
        subject = "Outgoing transaction"
        confirmation_link = f'http://127.0.0.1:8000/transactions/confirmation/{transaction_id}'
        msg = f"Please click the link below to confirm this transaction:\n\n{confirmation_link}\n\n"
        await send_emails.send_email(user_email[0][0],confirmation_link, subject,msg)
    info = "Transaction created successfully. Awaiting recipient response."

    return DisplayTransaction.from_query_result(info,transaction.amount,transaction.category,transaction.recipient,transaction.wallet,transaction.is_recurring)

async def accept(id,wallet):

    await update_query('''UPDATE transactions set accepted_by_recipient = 1,received_at = %s where id = %s''',(datetime.now(),id))
    transaction_info = await read_query('''SELECT amount,category,recipient_id,wallet_id,is_recurring FROM transactions WHERE id = %s''',(id,))
    transaction = Transaction.from_query_result(*transaction_info[0])
    await update_query('''UPDATE wallets SET balance = balance - %s Where id = %s''', (transaction.amount,transaction.wallet))
    await update_query('''UPDATE wallets SET balance = balance + %s Where id = %s''',(transaction.amount,wallet.wallet))

    return 'Transaction Accepted'

async def confirm(id):

    await update_query('''UPDATE transactions set confirmed = 1 where id = %s''',(id,))
    recepient_id = await read_query('''select recipient_id from transactions where id = %s''',(id,))
    recepient_email = await read_query('''SELECT email FROM users WHERE id = %s''', (recepient_id,))

    await acceptence_email(id,recepient_email[0][0])

    return 'Transaction Confirmed'

async def acceptence_email(transaction_id,recepient_email):
    subject = "Incoming transaction"
    confirmation_link = f'http://127.0.0.1:8000/transactions/accept_confirmation/{transaction_id}'
    msg = f"Please click the link below to accept this transaction:\n\n{confirmation_link}\n\n If you don't want to accept ignore this email."  # could add more info from who and amount later
    await send_emails.send_email(recepient_email,confirmation_link, subject,msg)