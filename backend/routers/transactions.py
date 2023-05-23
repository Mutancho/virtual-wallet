from fastapi import APIRouter, Response, Header, Request, Query
from schemas.transaction_models import Transaction
from schemas.wallet_models import ChooseWallet
from services import transaction_service,user_service,wallets
from datetime import date,datetime

transactions_router = APIRouter(prefix='/transactions', tags=['Transactions'])


@transactions_router.post('/')
async def make_transaction(transaction: Transaction,token: str = Header(alias="Authorization")):
    if not await user_service.is_logged_in(token):
        return Response(status_code=401)
    wallet = await wallets.wallet_by_id(transaction.wallet,token)
    if wallet.balance < transaction.amount:
        return Response(status_code=400,content='Insufficient funds')

    return await transaction_service.create_transaction(transaction,token)

@transactions_router.get("/accept_confirmation/{id}")
async def confirmation_email(id: int,wallet: ChooseWallet):

    return await transaction_service.accept(id,wallet)

@transactions_router.get("/confirmation/{id}")
async def confirmation_email(id: int):

    return await transaction_service.confirm(id)

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
    result = await transaction_service.all(from_date,to_date,sender,recipient,limit,offset)
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
    result = await transaction_service.get_transactions(from_date,to_date,user,direction,limit,offset,token)
    if sort and (sort.lower() == 'asc' or sort.lower() == 'desc'):
        return transaction_service.sort(result, reverse=sort.lower() == 'desc', attribute=sort_by)

    return result