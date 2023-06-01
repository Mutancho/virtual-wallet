from fastapi import APIRouter, HTTPException, status, Header, Response
from fastapi.responses import RedirectResponse
from services.custom_errors.referrals import UserHasBeenReferredAlready
from services.custom_errors.users import AdminAccessRequired
from services.referrals import create_referral_link, view, delete, validate, base_url
from schemas.referrals import Referral

referrals_router = APIRouter(prefix="/users/referrals", tags=["Referrals"])


@referrals_router.post("")
async def create_link(referral: Referral, token: str = Header(alias="Authorization")):
    try:
        new_link = await create_referral_link(referral, token)
        if not new_link:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return new_link
    except UserHasBeenReferredAlready:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=UserHasBeenReferredAlready.error_message)


@referrals_router.get("")
async def view_referrals(token: str = Header(alias="Authorization")):
    get_referrals = await view(token)
    if not get_referrals:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return get_referrals


@referrals_router.get("{referral_id}")
async def referral_check(referral_id: int):
    is_valid = await validate(referral_id)
    if not is_valid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expired referral link!")
    url = f"{base_url}/users/register?referral_id={referral_id}"
    response = RedirectResponse(url=url)
    return response


@referrals_router.delete("/")
async def delete_expired_referrals(token: str = Header(alias="Authorization")):
    try:
        deleted_referrals = await delete(token)
        if not deleted_referrals:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Nothing deleted, database is up to date!")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except AdminAccessRequired:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=AdminAccessRequired.error_message)
