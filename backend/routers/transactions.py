from fastapi import APIRouter, Response, Header, Query
from fastapi.responses import HTMLResponse
from schemas.transaction_models import Transaction
from schemas.wallet_models import ChooseWallet
from services import transaction_service, user_service, wallets
from datetime import date, datetime, timedelta

transactions_router = APIRouter(prefix='/transactions', tags=['Transactions'])


@transactions_router.post('/')
async def make_transaction(transaction: Transaction, token: str = Header(alias="Authorization")):
    if not await user_service.is_logged_in(token):
        return Response(status_code=401)
    if await user_service.is_blocked(token):
        return Response(status_code=403)
    wallet = await wallets.wallet_by_id(transaction.wallet, token)
    if wallet.balance < transaction.amount:
        return Response(status_code=400, content='Insufficient funds')

    return await transaction_service.create_transaction(transaction, token)


@transactions_router.post("/accept_confirmation/{id}")
async def accept(id: int, wallet: ChooseWallet):
    if not await transaction_service.get_transaction_sent_at(id) + timedelta(1) >= datetime.now():
        return Response(status_code=400, content='You are past the time to accept this transaction')

    return HTMLResponse(content=await transaction_service.accept(id, wallet), status_code=200, media_type='text/html')


@transactions_router.get("/confirmation/{id}")
async def confirmation_email(id: int):
    if not await transaction_service.get_transaction_sent_at(id) + timedelta(1) >= datetime.now():
        html = '''<!DOCTYPE html><html><head><title>Transaction Confirmation Time Expired</title><style>body {font-family: Arial, sans-serif;text-align: center;margin-top: 100px;}h1 {color: #336699;}p {color: #666666;}</style></head><body><h1>Transaction Confirmation Time Expired</h1><p>We're sorry, but the confirmation time for this transaction has expired. Please contact our support team for further assistance.</p></body></html>'''
        return HTMLResponse(content=html, status_code=400, media_type='text/html')

    return HTMLResponse(content=await transaction_service.confirm(id), status_code=200, media_type='text/html')


@transactions_router.get('/')
async def get_all(from_date: date | None = None,
                  to_date: date | None = None,
                  sender: str | None = None,
                  recipient: str | None = None,
                  limit: int | None = 20,
                  offset: int | None = None,
                  sort: str | None = Query(default=None, regex='(?i)^DESC|ASC'),
                  sort_by: str | None = Query(default=None, regex='^amount|sent_at|received_at'),
                  token: str = Header(alias="Authorization")):
    if not await user_service.is_logged_in(token):
        return Response(status_code=401)
    if not await user_service.is_admin(token):
        return Response(status_code=403)
    result = await transaction_service.all(from_date, to_date, sender, recipient, limit, offset)
    if sort and (sort.lower() == 'asc' or sort.lower() == 'desc'):
        return transaction_service.sort(result, reverse=sort.lower() == 'desc', attribute=sort_by)

    return result


@transactions_router.get('/search')
async def get_transactions(from_date: date | None = None,
                           to_date: date | None = None,
                           user: str | None = None,
                           direction: str | None = Query(default=None, regex='(?i)^incoming|outgoing$'),
                           limit: int | None = None,
                           offset: int | None = None,
                           sort: str | None = Query(default=None, regex='(?i)^DESC|ASC'),
                           sort_by: str | None = Query(default=None, regex='^amount|sent_at|received_at'),
                           token: str = Header(alias="Authorization")):
    if not await user_service.is_logged_in(token):
        return Response(status_code=401)
    result = await transaction_service.get_transactions(from_date, to_date, user, direction, limit, offset, token)
    if sort and (sort.lower() == 'asc' or sort.lower() == 'desc'):
        return transaction_service.sort(result, reverse=sort.lower() == 'desc', attribute=sort_by)

    return result


@transactions_router.get('/pending')
async def pending_transactions(token: str = Header(alias="Authorization")):
    if not await user_service.is_logged_in(token):
        return Response(status_code=401)

    return await transaction_service.get_pending_transactions(token)


@transactions_router.post('/recurring')
async def recurring_transactions():
    return await transaction_service.execute_recurring_transactions()
