from fastapi import APIRouter, Response, Header, Request
from schemas.user_models import RegisterUser,EmailLogin,UsernameLogin
from services import user_service
from utils import oauth2

users_router = APIRouter(prefix='/users', tags=['Users'])

@users_router.post("/register")
async def create_user(user:RegisterUser):
    if await user_service.exists_by_username_email_phone(user):
        return Response(status_code=400,
                        content=f'A User with this username: {user.username}, email: {user.email} or phone number: {user.phone_number} already exists!')

    return await user_service.create(user)

@users_router.get("/confirmation/{id}")
async def confirmation_email(id: int):

    return await user_service.confirm(id)

@users_router.post('/login')
async def login(credentials: EmailLogin | UsernameLogin):
    if not await user_service.verify_credentials(credentials):
        if isinstance(credentials, EmailLogin):
            return Response(status_code=401, content=f"User with this email: {credentials.email} doesn't exist!")
        if isinstance(credentials, UsernameLogin):
            return Response(status_code=401, content=f"User with this username: {credentials.username} doesn't exist!")
    if not await user_service.valid_password(credentials):
        return Response(status_code=401, content='Invalid password.')

    return await user_service.login(credentials)

@users_router.get('/')
async def get_all(username: str | None = None,
                  phone: str | None = None,
                  email: str | None = None,
                  limit: int | None = None,
                  offset: int | None = None,
                  token: str = Header(alias="Authorization")):
    if not await user_service.exists_by_id(token):
        return Response(status_code=404)
    if not await user_service.is_admin(token):
        return Response(status_code=403)

    return await user_service.all(username,phone,email,limit,offset)
