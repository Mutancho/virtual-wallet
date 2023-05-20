from fastapi import APIRouter, Response, Header, Request
from services import contact_service,user_service
from schemas.contact_models import Contact

contacts_router = APIRouter(prefix='/contacts', tags=['Contacts'])

@contacts_router.post('/{username}')
async def add_contact(username: str,token: str = Header(alias="Authorization")):
    contact = Contact(username=username)
    if not await user_service.is_logged_in(token):
        return Response(status_code=401)
    if not await user_service.exists_by_username_email_phone(contact):
        return Response(status_code=404)
    if await contact_service.is_contact(username,token):
        return Response(status_code=400,content='This user is already in your contacts list')

    return await contact_service.add_contact(username,token)