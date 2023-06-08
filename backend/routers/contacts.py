from fastapi import APIRouter, Response, Header, status
from services import contact_service, user_service
from schemas.contact_models import Contact

contacts_router = APIRouter(prefix='/contacts', tags=['Contacts'])


@contacts_router.post('/{username}')
async def add_contact(username: str, token: str = Header(alias="Authorization")):
    contact = Contact(username=username)
    if not await user_service.is_logged_in(token):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    if not await user_service.exists_by_username_email_phone(contact):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    if await contact_service.is_contact(username, token):
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content='This user is already in your contacts list')

    return await contact_service.add_contact(username, token)


@contacts_router.delete('/{username}')
async def remove_contact(username: str, token: str = Header(alias="Authorization")):
    contact = Contact(username=username)
    if not await user_service.is_logged_in(token):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)
    if not await user_service.exists_by_username_email_phone(contact):
        return Response(status_code=status.HTTP_404_NOT_FOUND)
    if not await contact_service.is_contact(username, token):
        return Response(status_code=status.HTTP_400_BAD_REQUEST, content='This user is not in your contacts list')

    return await contact_service.remove_contact(username, token)


@contacts_router.get('')
async def view_contact_list(token: str = Header(alias="Authorization")):
    if not await user_service.is_logged_in(token):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    return await contact_service.get_contacts(token)
