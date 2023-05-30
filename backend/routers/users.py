from fastapi import APIRouter, Response, Header, Query, Request
from fastapi.responses import HTMLResponse
from schemas.user_models import RegisterUser, EmailLogin, UsernameLogin, DisplayUser, UpdateUser, BlockUnblock
from services import user_service
from services.referrals import referral_used
from fastapi.templating import Jinja2Templates

users_router = APIRouter(prefix='/users', tags=['Users'])
templates = Jinja2Templates(directory="../frontend/templates")


@users_router.post("/register")
async def create_user(user: RegisterUser, referral_id: int = Query(None)):
    if await user_service.exists_by_username_email_phone(user):
        return Response(status_code=400,
                        content=f'A User with this username, email or phone number already exists!')
    if referral_id:
        await referral_used(referral_id)
    return await user_service.create(user)


@users_router.get("/confirmation/{id}")
async def confirmation_email(id: int):

    return HTMLResponse(content=await user_service.confirm(id), status_code=200, media_type='text/html')


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

@users_router.post('/logout')
async def logout(token: str = Header(alias="Authorization")):
    if not await user_service.is_logged_in(token):
        return Response(status_code=401)
    return await user_service.logout(token)


@users_router.get('/')
async def get_all(username: str | None = None,
                  phone: str | None = None,
                  email: str | None = None,
                  limit: int | None = None,
                  offset: int | None = None,
                  token: str = Header(alias="Authorization")):
    if not await user_service.is_logged_in(token):
        return Response(status_code=401)
    if not await user_service.is_admin(token):
        return Response(status_code=403)

    return await user_service.all(username, phone, email, limit, offset)


@users_router.delete('/{id}', response_model=DisplayUser)
async def delete(id: int|None, token: str = Header(alias="Authorization")):
    if not await user_service.is_logged_in(token):
        return Response(status_code=401)
    if not await user_service.is_user_authorized_to_delete(token, id):
        return Response(status_code=403, content="You are not allowed to delete this user!")
    if not await user_service.exists_by_id(id):
        return Response(status_code=404)

    return await user_service.delete(id)


@users_router.put('/{id}')
async def update(id: int, user: UpdateUser, token: str = Header(alias="Authorization")):
    if not await user_service.is_logged_in(token):
        return Response(status_code=401)
    if not await user_service.can_update(id, token, user.old_password, user.new_password, user.repeat_password):
        return Response(status_code=400, content="You can't perform this action!")
    if await user_service.check_exists_by_email_phone_for_updating(id, user):
        return Response(status_code=400,
                        content=f'A User with this email: {user.email}'
                                f' or phone number: {user.phone_number} already exists!')

    return await user_service.update(id, user)


@users_router.post('/{id}/blocks')  # maybe change method to patch/put
async def block_unblock(id: int, command: BlockUnblock, token: str = Header(alias="Authorization")):
    if not await user_service.is_logged_in(token):
        return Response(status_code=401)
    if not await user_service.is_admin(token):
        return Response(status_code=403)
    if not await user_service.exists_by_id(id):
        return Response(status_code=404)

    return await user_service.block_unblock(id, command)


@users_router.get('/search')
async def get_user(username: str | None = None,
                   phone: str | None = None,
                   email: str | None = None,
                   token: str = Header(alias="Authorization")):
    if not await user_service.is_logged_in(token):
        return Response(status_code=401)
    if username is None and phone is None and email is None:
        return Response(status_code=400,
                        content="You must provide either a username,"
                                " an email or a phone number as a query parameter in order to search!")

    user = await user_service.get_user(username, email, phone)
    if isinstance(user, str):
        return Response(status_code=404, content=user)
    return user
