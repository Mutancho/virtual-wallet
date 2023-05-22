from fastapi import APIRouter, Response, Header, Request
from schemas.transaction_models import Transaction
from schemas.wallet_models import ChooseWallet
from services import transaction_service,user_service,wallets


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