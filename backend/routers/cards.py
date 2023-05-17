from fastapi import APIRouter, Request, Form, HTTPException, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from utils.oauth2 import get_current_user

from services.external_apis.stripe_api import attach_payment_method, detach_payment_method, list_payment_methods, \
    get_stripe_id

router = APIRouter()
templates = Jinja2Templates(directory="../frontend/templates")


@router.get("/", response_class=HTMLResponse)
async def payment(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/payment-methods/attach")
async def attach_payment(payment_method_id: str, current_user: str = Depends(get_current_user)):
    try:
        stripe_id = await get_stripe_id(current_user)
        return attach_payment_method(payment_method_id, stripe_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/payment-methods/attach")
async def attach_payment(payment_method_id: str, current_user: str = Depends(get_current_user)):
    try:
        stripe_id = await get_stripe_id(current_user)
        return attach_payment_method(payment_method_id, stripe_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/payment-methods/detach")
async def detach_payment(payment_method_id: str, current_user: str = Depends(get_current_user)):
    try:
        return detach_payment_method(payment_method_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/payment-methods/list")
async def list_payments(current_user: str = Depends(get_current_user)):
    try:
        stripe_id = await get_stripe_id(current_user)
        return list_payment_methods(stripe_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
