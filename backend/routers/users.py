from fastapi import APIRouter, Response, Header, Request
from schemas.user_models import RegisterUser
from services import user_service
from utils import oauth2

users_router = APIRouter(prefix='/users', tags=['Users'])

@users_router.post("/register")
async def create_user(user:RegisterUser):

    return await user_service.create(user)

@users_router.get("/confirmation/{id}")
async def confirmation_email(id: int):


    return await user_service.confirm(id)