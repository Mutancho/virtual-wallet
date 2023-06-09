from datetime import datetime, timedelta
from database.database_queries import insert_query, read_query, update_query, manage_db_transaction
from services.custom_errors.referrals import UserHasBeenReferredAlready
from utils.oauth2 import get_current_user
from utils.send_emails import send_email
from schemas.referrals import Referral, ViewReferrals
from services.user_service import is_admin
from services.custom_errors.users import AdminAccessRequired
from config.config import settings
from asyncmy.connection import Connection

base_url = settings.base_url


@manage_db_transaction
async def create_referral_link(conn: Connection, referral: Referral, token: str):
    user_id = get_current_user(token)
    global_check_referral = await read_query(conn, "SELECT is_used FROM referrals WHERE email = %s", (referral.email,))

    if any(num[0] == 1 for num in global_check_referral):
        raise UserHasBeenReferredAlready()

    local_check_referral = await read_query(conn, "SELECT link FROM referals WHERE user_id =%s  and email = %s",
                                            (user_id, referral.email,))

    if local_check_referral:
        return local_check_referral[0][0]

    get_last_referral_id = await read_query(conn, "SELECT id FROM referals ORDER BY id DESC LIMIT 1")
    if not get_last_referral_id:
        get_last_referral_id = 0
    else:
        get_last_referral_id = get_last_referral_id[0][0]
    new_link = f"{base_url}/register/{get_last_referral_id + 1}"
    expiry_date = datetime.now() + timedelta(days=30)

    await insert_query(
        conn,
        "INSERT INTO referrals(email, expiry_date, user_id, link) VALUES (%s, %s, %s, %s)",
        (referral.email, expiry_date, user_id, new_link))
    await send_email(referral.email, subject="Virtual Wallet Referral Link",
                     message=f"Please use the referral link to register for a Virtual Wallet:\n\n{new_link} ")
    return new_link


@manage_db_transaction
async def view(conn: Connection, token: str):
    user_id = get_current_user(token)
    get_referrals = await read_query(
        conn,
        "SELECT id, email, created_at, expiry_date, link, is_used FROM referals WHERE user_id = %s",
        (user_id,))
    found_referrals = [ViewReferrals.read_from_query(*referral) for referral in get_referrals]
    return found_referrals


@manage_db_transaction
async def delete(conn: Connection, token: str):
    admin = await is_admin(token)
    if not admin:
        raise AdminAccessRequired()
    delete_referrals = await update_query(conn, "DELETE FROM referals WHERE expiry_date < CURDATE()")
    return delete_referrals


@manage_db_transaction
async def validate(conn: Connection, referral_id: int):
    return await read_query(conn, "SELECT id FROM referals WHERE id = %s", (referral_id,))


@manage_db_transaction
async def referral_used(conn: Connection, referral_id: int):
    await update_query(conn, "UPDATE referals SET is_used = 1 WHERE id = %s", (referral_id,))
