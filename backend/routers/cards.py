from fastapi import APIRouter, HTTPException, status, Header, Body
from services.external_apis.stripe_api import attach_payment_method, detach_payment_method, list_payment_methods, \
    get_stripe_id
from schemas.cards_models import PaymentCard

cards_router = APIRouter(prefix="/users/cards", tags=['Payment-Cards'])


@cards_router.post("/payment-methods/attach")
async def attach_payment(payment_method: PaymentCard, auth: str = Header(alias="Authorization")):
    try:
        stripe_id = await get_stripe_id(auth)
        return await attach_payment_method(payment_method.id, stripe_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@cards_router.post("/payment-methods/detach")
async def detach_payment(payment_method: PaymentCard = Body(...)):
    try:
        return await detach_payment_method(payment_method.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@cards_router.get("/payment-methods/list")
async def list_payments(auth: str = Header(alias="Authorization")):
    try:
        stripe_id = await get_stripe_id(auth)
        return await list_payment_methods(stripe_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
