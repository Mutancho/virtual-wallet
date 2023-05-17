from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.external_apis.stripe_api import create_payment_intent

router = APIRouter()
templates = Jinja2Templates(directory="../frontend/templates")


@router.post("/create-payment-intent", response_class=HTMLResponse)
async def create_payment_intent_route(request: Request, amount: int = Form(...), payment_method_id: str = Form(...)):
    payment_intent = await create_payment_intent(amount, payment_method_id)
    if payment_intent.status == 'succeeded':
        return templates.TemplateResponse("success.html", {"request": request})
    else:
        return templates.TemplateResponse("cancel.html", {"request": request})


@router.get("/success", response_class=HTMLResponse)
async def success(request: Request):
    return templates.TemplateResponse("success.html", {"request": request})


@router.get("/cancel", response_class=HTMLResponse)
async def cancel(request: Request):
    return templates.TemplateResponse("cancel.html", {"request": request})
