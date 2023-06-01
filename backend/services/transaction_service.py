from database.database_queries import read_query,update_query,insert_query
from utils import oauth2,send_emails
from schemas.transaction_models import Transaction, DisplayTransaction, DisplayTransactionInfo,PendingTransaction
from datetime import date,datetime,timedelta
from currency_converter import CurrencyConverter
from services.wallets import get_user_id_from_username
async def create_transaction(transaction,token):
    user_id = oauth2.get_current_user(token)

    recipient = await get_user_id_from_username(transaction.recipient)
    confirmed = 1
    if transaction.amount > 10000:
        confirmed = 0
    if not transaction.category:
        transaction.category = 'Other'
    if not transaction.is_recurring:
        transaction.is_recurring = False

    transaction_id = await insert_query('''INSERT INTO transactions(amount, is_recurring, recipient_id, category, wallet_id,confirmed) VALUES(%s,%s,%s,%s,%s,%s)''',
                       (transaction.amount,transaction.is_recurring,recipient,transaction.category,transaction.wallet,confirmed))
    if transaction.amount <= 10000:
        recepient_email = await read_query('''SELECT email FROM users WHERE id = %s''',(recipient,))

        await acceptence_email(transaction_id,recepient_email[0][0])
        info = "Transaction created successfully. Awaiting recipient response."
    else:
        user_email = await read_query('''SELECT email FROM users WHERE id = %s''',(user_id,))
        subject = "Outgoing transaction"
        confirmation_link = f'http://127.0.0.1:8000/transactions/confirmation/{transaction_id}'
        msg = f"Please click the link below to confirm this transaction:\n\n{confirmation_link}\n\n"
        await send_emails.send_email(user_email[0][0],confirmation_link, subject,msg)
        info = "Transaction created successfully. Awaiting your confirmation."

    return DisplayTransaction.from_query_result(info,transaction.amount,transaction.category,transaction.recipient,transaction.wallet,transaction.is_recurring)

async def accept(id,wallet):

    await update_query('''UPDATE transactions set accepted_by_recipient = 1,received_at = %s where id = %s''',(datetime.now(),id))
    transaction_info = await read_query('''SELECT amount,category,recipient_id,wallet_id,is_recurring FROM transactions WHERE id = %s''',(id,))
    transaction = Transaction.from_query_result(*transaction_info[0])
    await update_query('''UPDATE wallets SET balance = balance - %s Where id = %s''', (transaction.amount,transaction.wallet))
    sender_currency = await read_query('''SELECT c.currency FROM wallets as w JOIN currencies c on c.id = w.currency_id WHERE w.id = %s''',(transaction.wallet,))
    reciver_currency = await read_query('''SELECT c.currency FROM wallets as w JOIN currencies c on c.id = w.currency_id WHERE w.id = %s''',(wallet.wallet,))

    if sender_currency[0][0] != reciver_currency[0][0]:
        c = CurrencyConverter()
        amount = c.convert(transaction.amount, sender_currency[0][0], reciver_currency[0][0])
        fx_rate = round(amount,2)/transaction.amount
        transaction.amount = round(amount,2)
        await insert_query('''INSERT INTO currency_conversions(base_currency_id,quote_currency_id,fx_rate,transaction_id)
            VALUES((SELECT currency_id FROM wallets WHERE id = %s),(SELECT id FROM currencies WHERE currency = %s),%s,%s)''',
                           (transaction.wallet,reciver_currency[0][0],fx_rate,id))


    await update_query('''UPDATE wallets SET balance = balance + %s Where id = %s''',(transaction.amount,wallet.wallet))

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Transaction Accepted</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 100px;
            }

            h1 {
                color: #336699;
            }

            p {
                color: #666666;
            }
        </style>
    </head>
    <body>
        <h1>Transaction Accepted</h1>
        <p>This transaction has been successfully accepted.</p>
    </body>
    </html>
    '''

async def confirm(id):

    await update_query('''UPDATE transactions set confirmed = 1 where id = %s''',(id,))
    recepient_id = await read_query('''select recipient_id from transactions where id = %s''',(id,))
    recepient_email = await read_query('''SELECT email FROM users WHERE id = %s''', (recepient_id,))

    await acceptence_email(id,recepient_email[0][0])

    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Transaction Confirmed</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin-top: 100px;
            }

            h1 {
                color: #336699;
            }

            p {
                color: #666666;
            }
        </style>
    </head>
    <body>
        <h1>Transaction Confirmed</h1>
        <p>Your transaction has been successfully confirmed.</p>
    </body>
    </html>
    '''

async def acceptence_email(transaction_id,recepient_email):
    subject = "Incoming transaction"
    confirmation_link = f'http://127.0.0.1:8000/transactions/accept_confirmation/{transaction_id}'
    msg = f"Please go to the Pending Transactions section on the site to view and accept this transaction. \n\n If you don't want to accept you can ignore this email.\n\n    The Team at Virtual Wallet."
    await send_emails.send_email(recepient_email,confirmation_link, subject,msg)


async def all(from_date,to_date,sender,recipient,limit,offset):


    sql = '''SELECT t.amount,t.category,t.recipient_id,t.wallet_id,t.is_recurring,t.sent_at,t.accepted_by_recipient,t.received_at FROM transactions as t '''

    where_clauses = []
    if from_date:
        where_clauses.append(f"t.sent_at >= '{from_date}'")
    if to_date:
        where_clauses.append(f"t.received_at <= '{to_date}'")
    if sender:
        where_clauses.append(f"t.wallet_id in (SELECT id FROM wallets WHERE creator_id = (SELECT id From users where username = '{sender}'))")
    if recipient:
        where_clauses.append(f"t.recipient_id = (SELECT id From users where username = '{recipient}')")
    if where_clauses:
        sql += ' WHERE ' + ' AND '.join(where_clauses)
    if limit:
        if offset:
            sql += f" limit {offset},{limit}"
        else:
            sql += f" limit {limit}"
    data = await read_query(sql)

    return (DisplayTransactionInfo.from_query_result(*row) for row in data)

async def get_transactions(from_date:date,to_date,user,direction,limit,offset,token):
    user_id = oauth2.get_current_user(token)

    sql = f'''SELECT t.amount,t.category,t.recipient_id,t.wallet_id,t.is_recurring,t.sent_at,t.accepted_by_recipient,t.received_at FROM transactions as t '''

    where_clauses = []
    if user:
        if direction and direction.lower() == 'incoming':
            where_clauses.append(
                f"t.wallet_id in (SELECT id FROM wallets WHERE creator_id = (SELECT id From users where username = '{user}')) AND t.recipient_id = {user_id}")
        elif direction and direction.lower() == 'outgoing':
            where_clauses.append(f"t.recipient_id = (SELECT id From users where username = '{user}')")
    elif user is None or direction is None:
        where_clauses.append(f"(wallet_id in (SELECT w.id FROM wallets as w left join users_wallets as uw on w.id = uw.wallet_id WHERE w.creator_id = {user_id} or uw.user_id = {user_id}) or t. recipient_id = {user_id})")
    if user is None and direction and direction.lower() == 'incoming':
        where_clauses.append(f"t.recipient_id = {user_id}")
    if user is None and direction and direction.lower() == 'outgoing':
        where_clauses.append(
            f"t.wallet_id in (SELECT w.id FROM wallets as w left join users_wallets as uw on w.id = uw.wallet_id WHERE w.creator_id = {user_id} or uw.user_id = {user_id})")
    if from_date:
        where_clauses.append(f"t.sent_at >= '{from_date}'")
    if to_date:
        where_clauses.append(f"t.received_at <= '{to_date}'")
    if where_clauses:
        sql += ' WHERE ' + ' AND '.join(where_clauses)
    if limit:
        if offset:
            sql += f" limit {offset},{limit}"
        else:
            sql += f" limit {limit}"

    data = await read_query(sql)




    return (DisplayTransactionInfo.from_query_result(*row) for row in data)

async def get_pending_transactions(token):
    user_id = oauth2.get_current_user(token)
    transaction_data = await read_query(f'''SELECT t.id, t.amount, t.category, t.is_recurring, t.sent_at, t.accepted_by_recipient,c.currency FROM transactions as t, currencies as c 
                                            WHERE confirmed = 1 AND accepted_by_recipient = 0 AND recipient_id = {user_id} AND c.id = (SELECT currency_id FROM wallets WHERE id = t.wallet_id)''')


    return (PendingTransaction.from_query_result(*t) for t in transaction_data)

async def get_transaction_sent_at(transaction_id: int):
    sent_at = await read_query('''SELECT sent_at FROM transactions WHERE id = %s''',(transaction_id,))

    return sent_at[0][0]

def sort(transactions: list[DisplayTransactionInfo], *, attribute='sent_at', reverse=False):

    if attribute == 'amount':
        def sort_fn(t: DisplayTransactionInfo): return t.amount
    elif attribute == 'received_at':
        def sort_fn(t: DisplayTransactionInfo): return t.received_at
    else:
        def sort_fn(t: DisplayTransactionInfo): return t.sent_at

    return sorted(transactions, key=sort_fn, reverse=reverse)
