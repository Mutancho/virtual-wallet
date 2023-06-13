from fastapi import APIRouter, HTTPException, status, Header, Body
from services.external_apis.stripe_api import attach_payment_method, detach_payment_method, list_payment_methods
from schemas.cards_models import PaymentCard

cards_router = APIRouter(prefix="/users/cards/payment-methods", tags=['Payment-Cards'])


@cards_router.post("/attachments")
async def attach_payment(payment_method: PaymentCard, auth: str = Header(alias="Authorization")):
    try:
        return await attach_payment_method(payment_method.id, auth)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@cards_router.post("/detachments")
async def detach_payment(payment_method: PaymentCard = Body(...)):
    try:
        return await detach_payment_method(payment_method.id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@cards_router.get("/")
async def list_payments(auth: str = Header(alias="Authorization")):
    try:
        return await list_payment_methods(auth)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
