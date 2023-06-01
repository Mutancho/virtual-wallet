from fastapi import APIRouter, Header, Body, status
from fastapi.responses import JSONResponse
from services.external_apis.stripe_api import create_payment_intent
from services.wallets import update_wallet_balance
from services.custom_errors.wallets import NoTopUpAccess, NoWithdrawalAccess, WithdrawMoreThanBalance
from services.transfers import update_transfers_db

transfers_router = APIRouter(prefix="/users/transfers", tags=["Transfers"])


@transfers_router.post("/payment-intent")
async def create_payment_intent_route(amount: str = Body(...), wallet_id: int = Body(...),
                                      currency: str = Body(...), payment_method_id: str = Body(...),
                                      token: str = Header(alias="Authorization")):
    try:
        await update_wallet_balance(wallet_id, amount, token, is_withdrawal=False)
        payment_intent = await create_payment_intent(amount, payment_method_id, currency, token)
        if payment_intent.status == 'succeeded':
            await update_transfers_db("deposit", amount, wallet_id)
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Payment succeeded"})
    except NoTopUpAccess:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Payment unsuccessful"})


@transfers_router.post("/create-payout")
async def create_payout_route(amount: str = Body(...), wallet_id: int = Body(...),
                              token: str = Header(alias="Authorization")):
    try:

        withdrawal_success = await update_wallet_balance(wallet_id, amount, token, is_withdrawal=True)
        if withdrawal_success:
            await update_transfers_db("withdrawal", amount, wallet_id)
            return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Payment succeeded"})
    except WithdrawMoreThanBalance:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Payment unsuccessful"})
    except NoWithdrawalAccess:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Payment unsuccessful"})
