from datetime import datetime, timedelta
from database.database_queries import insert_query, read_query, update_query
from services.custom_errors.referrals import UserHasBeenReferredAlready
from utils.oauth2 import get_current_user
from utils.send_emails import send_email
from schemas.referrals import Referral, ViewReferrals
from services.user_service import is_admin
from services.custom_errors.users import AdminAccessRequired

base_url = "http://127.0.0.1:8000"


async def create_referral_link(referral: Referral, token: str):
    user_id = get_current_user(token)
    global_check_referral = await read_query("SELECT is_used FROM referrals WHERE email = %s", (referral.email,))

    if any(num[0] == 1 for num in global_check_referral):
        raise UserHasBeenReferredAlready()

    local_check_referral = await read_query("SELECT link FROM referrals WHERE user_id =%s  and email = %s",
                                            (user_id, referral.email,))

    if local_check_referral:
        return local_check_referral[0][0]

    get_last_referral_id = await read_query("SELECT id FROM referrals ORDER BY id DESC LIMIT 1")
    if not get_last_referral_id:
        get_last_referral_id = 0
    else:
        get_last_referral_id = get_last_referral_id[0][0]
    new_link = f"{base_url}/users/{user_id}/referrals/{get_last_referral_id + 1}"
    # todo update above link to deployed host link
    expiry_date = datetime.now() + timedelta(days=30)

    await insert_query(
        "INSERT INTO referrals(email, expiry_date, user_id, link) VALUES (%s, %s, %s, %s)",
        (referral.email, expiry_date, user_id, new_link))
    await send_email(referral.email, subject="Virtual Wallet Referral Link",
                     message=f"Please use the referral link to register for a Virtual Wallet:\n\n{new_link} ")
    return new_link


async def view(token: str):
    user_id = get_current_user(token)
    get_referrals = await read_query(
        "SELECT id, email, created_at, expiry_date, link, is_used FROM referrals WHERE user_id = %s",
        (user_id,))
    found_referrals = [ViewReferrals.read_from_query(*referral) for referral in get_referrals]
    return found_referrals


async def delete(token: str):
    admin = await is_admin(token)
    if not admin:
        raise AdminAccessRequired()
    delete_referrals = await update_query("DELETE FROM referrals WHERE expiry_date < CURDATE()")
    return delete_referrals


async def validate(referral_id: int):
    is_referral_valid = await read_query("SELECT id FROM referrals WHERE id = %s", (referral_id,))
    return is_referral_valid


async def referral_used(referral_id: int):
    await update_query("UPDATE referrals SET is_used = 1 WHERE id = %s", (referral_id,))
# todo add transaction for bonuses for the 2 users
