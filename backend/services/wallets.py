from database.database_queries import read_query, update_query, insert_query
from schemas.wallet_models import NewWallet, ViewWallet, ViewAllWallets
from utils.oauth2 import get_current_user
from services.currencies import select_currency
from services.constants import JOINT, IS_TRUE
from services.custom_errors import BalanceNotNull


async def create(wallet: NewWallet, token: str):
    user_id = get_current_user(token)
    currency_id = await select_currency(wallet.currency)

    has_wallets = await _user_has_wallet(user_id)
    if has_wallets:
        new_wallet_id = await insert_query(
            "INSERT INTO wallets(type, currency_id, creator_id, default_wallet) VALUES(%s,%s,%s,%s)",
            (wallet.type, currency_id, user_id, 0))
    else:
        new_wallet_id = await insert_query(
            "INSERT INTO wallets(type, currency_id, creator_id) VALUES(%s,%s,%s)",
            (wallet.type, currency_id, user_id))

    if wallet.type == JOINT:
        await _create_joint_wallet(user_id, new_wallet_id)

    return new_wallet_id


async def all_wallets(token: str) -> ViewAllWallets:
    user_id = get_current_user(token)
    get_wallets = await read_query(
        "SELECT w.id, w.type, c.currency, w.balance, w.is_active, w.default_wallet, w.created_at FROM wallets w "
        "JOIN currencies c on c.id = w.currency_id "
        "WHERE w.creator_id=%s", (user_id,))
    get_owner = await read_query("SELECT username FROM users WHERE id=%s", (user_id,))
    wallets = [ViewWallet.from_query_result(*wallet) for wallet in get_wallets]
    for wallet in wallets:
        if wallet.type == JOINT:
            wallet.members = await _add_group_members(wallet.wallet_id)
    return ViewAllWallets(owner=get_owner[0][0], wallets=wallets)


async def wallet_by_id(wallet_id: int, token: str) -> ViewWallet | None:
    user_id = get_current_user(token)

    get_wallet = await read_query(
        "SELECT w.id, w.type, c.currency, w.balance, w.is_active, w.default_wallet, w.created_at FROM wallets w "
        "JOIN currencies c on c.id = w.currency_id "
        "WHERE w.id=%s and w.creator_id=%s", (wallet_id, user_id))
    if not get_wallet:
        return None
    wallet = ViewWallet.from_query_result(*get_wallet[0])
    if wallet.type == JOINT:
        wallet.members = _add_group_members(wallet_id)
    return wallet


async def delete(wallet_id: int, token: str):
    user_id = get_current_user(token)
    wallet_balance = await read_query("SELECT balance FROM wallets WHERE id=%s", (wallet_id,))
    if wallet_balance:
        raise BalanceNotNull("Wallet still holds cash, needs to be empty before removed!")
    delete_row = await update_query("DELETE FROM wallets WHERE id=%s and creator_id=%s", (wallet_id, user_id))
    return delete_row > 0


async def set_default_wallet(wallet_id: int, token: str):
    user_id = get_current_user(token)
    await update_query("UPDATE wallets SET default_wallet = %s WHERE creator_id = %s", (0, user_id))
    updated_wallet = await update_query("UPDATE wallets SET default_wallet = %s WHERE id = %s", (1, wallet_id))
    return updated_wallet > 0


# async def manage_joint_wallet_users(wallet_id: int, token: str):
#     user_id = get_current_user(token)
#     if user_id is None:
#         raise InvalidTokenError("Invalid token or user does not exist")
#     is_wallet_owner = read_query("SELECT ")


async def _create_joint_wallet(user_id: int, wallet_id):
    await insert_query("INSERT INTO users_wallets(is_creator, user_id, wallet_id) VALUES(%s, %s, %s)",
                       (IS_TRUE, user_id, wallet_id))


async def _add_group_members(wallet_id: int):
    get_members = await read_query("SELECT u.username FROM users u "
                                   "JOIN users_wallets uw on u.id = uw.user_id "
                                   "WHERE uw.wallet_id =%s", (wallet_id,))
    return get_members


async def _user_has_wallet(user_id: int) -> bool:
    wallet_exists = await read_query("SELECT id FROM wallets WHERE creator_id= %s", (user_id,))
    return True if wallet_exists else False
