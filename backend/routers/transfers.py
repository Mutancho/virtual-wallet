from fastapi import APIRouter, Request, Form, Header, Body, status
from fastapi.responses import JSONResponse

from services.external_apis.stripe_api import create_payment_intent
from services.external_apis.stripe_api import create_payout
from services.wallets import update_wallet_balance

transfers_router = APIRouter(prefix="/users/transfers", tags=["Transfers"])

@transfers_router.post("/payment-intent")
async def create_payment_intent_route(amount: int = Body(...), wallet_id: int = Body(...),
                                      currency: str = Body(...), payment_method_id: str = Body(...),
                                      token: str = Header(alias="Authorization")):
    payment_intent = await create_payment_intent(amount, payment_method_id, currency, token)
    if payment_intent.status == 'succeeded':
        await update_wallet_balance(wallet_id, amount)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Payment succeeded"})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Payment failed"})


@transfers_router.post("/create-payout")
async def create_payout_route(wallet_id: int = Form(...),
                              amount: int = Form(...), currency: str = Form(...),
                              destination: str = Form(...), token: str = Header(alias="Authorization")):
    payout = await create_payout(amount, currency, destination)
    if payout.status == 'succeeded':
        await update_wallet_balance(wallet_id, -amount)
        return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Payout succeeded"})
    else:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": "Payout failed"})
