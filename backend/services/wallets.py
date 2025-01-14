from database.database_queries import read_query, update_query, insert_query, manage_db_transaction
from schemas.wallet_models import NewWallet, ViewWallet, ViewAllWallets, WalletSettings, Member
from utils.oauth2 import get_current_user
from services.currencies import select_currency
from services.constants import JOINT, IS_TRUE, FULL, TOP_UP_ONLY
from services.custom_errors.wallets import BalanceNotNull, NotWalletAdmin, \
    UserAlreadyInGroup, CannotRemoveWalletAdmin, WithdrawMoreThanBalance, NoWithdrawalAccess, NoTopUpAccess
from decimal import Decimal
from asyncmy.connection import Connection


@manage_db_transaction
async def create(conn: Connection, wallet: NewWallet, token: str):
    user_id = get_current_user(token)
    currency_id = await select_currency(conn, wallet.currency)

    has_wallets = await _user_has_wallet(conn, user_id)
    if has_wallets:
        new_wallet_id = await insert_query(
            conn,
            "INSERT INTO wallets(name, type, currency_id, creator_id, default_wallet) VALUES(%s,%s,%s,%s,%s)",
            (wallet.name.title(), wallet.type.capitalize(), currency_id, user_id, 0))
    else:
        new_wallet_id = await insert_query(
            conn,
            "INSERT INTO wallets(name, type, currency_id, creator_id) VALUES(%s,%s,%s,%s)",
            (wallet.name.title(), wallet.type.capitalize(), currency_id, user_id))

    if wallet.type.lower() == JOINT.lower():
        await _create_joint_wallet(conn, user_id, new_wallet_id)

    return new_wallet_id


@manage_db_transaction
async def all_wallets(conn: Connection, token: str) -> ViewAllWallets:
    user_id = get_current_user(token)
    get_wallets = await read_query(
        conn,
        'SELECT w.id, w.name, w.type, c.currency, w.balance, w.is_active, w.default_wallet, w.created_at '
        'FROM wallets w '
        'JOIN currencies c ON c.id = w.currency_id '
        'WHERE w.creator_id = %s '
        'UNION '
        'SELECT w.id, w.name, w.type, c.currency, w.balance, w.is_active, w.default_wallet, w.created_at '
        'FROM wallets w '
        'JOIN currencies c ON c.id = w.currency_id '
        'JOIN users_wallets uw ON uw.wallet_id = w.id '
        'WHERE uw.user_id = %s AND uw.is_creator = 0', (user_id, user_id))
    get_owner = await read_query(conn, "SELECT username FROM users WHERE id=%s", (user_id,))
    wallets = [ViewWallet.from_query_result(*wallet) for wallet in get_wallets]
    for wallet in wallets:
        if wallet.type == JOINT:
            wallet.members = await _view_group_members(conn, wallet.wallet_id)
    return ViewAllWallets(owner=get_owner[0][0], wallets=wallets)


@manage_db_transaction
async def wallet_by_id(conn: Connection, wallet_id: int, token: str) -> ViewWallet | None:
    user_id = get_current_user(token)

    get_wallet = await read_query(
        conn,
        "SELECT w.id,w.name, w.type, c.currency, w.balance, w.is_active, w.default_wallet, w.created_at FROM wallets w "
        "JOIN currencies c on c.id = w.currency_id "
        "WHERE w.id=%s and w.creator_id=%s", (wallet_id, user_id))
    if not get_wallet:
        return None

    wallet = ViewWallet.from_query_result(*get_wallet[0])
    if wallet.type.lower() == JOINT.lower():
        wallet.members = await _view_group_members(conn, wallet_id)
    return wallet


@manage_db_transaction
async def delete(conn: Connection, wallet_id: int, token: str):
    user_id = get_current_user(token)
    wallet_balance = await read_query(conn, "SELECT balance FROM wallets WHERE id=%s", (wallet_id,))
    if wallet_balance and wallet_balance[0][0] != 0:
        raise BalanceNotNull()
    delete_row = await update_query(conn, "DELETE FROM wallets WHERE id=%s and creator_id=%s", (wallet_id, user_id))
    return delete_row > 0


@manage_db_transaction
async def set_default_wallet(conn: Connection, wallet_id: int, token: str):
    user_id = get_current_user(token)
    await update_query(conn, "UPDATE wallets SET default_wallet = %s WHERE creator_id = %s", (0, user_id))
    updated_wallet = await update_query(conn, "UPDATE wallets SET default_wallet = %s WHERE id = %s", (1, wallet_id))
    return updated_wallet > 0


@manage_db_transaction
async def settings(conn: Connection, wallet: WalletSettings, wallet_id: int, token: str):
    user_id = get_current_user(token)
    is_user_wallet_admin = await _is_wallet_admin(conn, user_id)

    if not await _wallet_exists(conn, wallet_id):
        return None

    if not is_user_wallet_admin:
        raise NotWalletAdmin()

    if wallet.name is not None:
        await _change_wallet_name(conn, wallet.name, wallet_id)

    if wallet.status is not None:
        await _wallet_status(conn, wallet.status, wallet_id)

    if wallet.add_username is not None:
        other_user = await get_user_id_from_username(conn, wallet.add_username)
        added_user = await _add_user_to_joint_wallet(conn, other_user, wallet_id)
        if not added_user:
            return None

    if wallet.remove_username is not None:
        other_user = await get_user_id_from_username(conn, wallet.remove_username)
        removed_user = await _remove_user_from_joint_wallet(conn, other_user, wallet_id)
        if not removed_user:
            return None

    if wallet.change_user_access is not None:
        other_user = await get_user_id_from_username(conn, wallet.username)
        await _amend_user_access_joint_wallet(conn, wallet.change_user_access, other_user, wallet_id)
    return True


@manage_db_transaction
async def update_wallet_balance(conn: Connection, wallet_id: int, amount: str, token: str, is_withdrawal: bool):
    user_id = get_current_user(token)
    amount = Decimal(amount)
    if is_withdrawal:
        amount *= -1
    is_wallet_joint = await read_query(conn, "SELECT type FROM wallets WHERE id = %s", (wallet_id,))
    if is_wallet_joint and is_wallet_joint[0][0] == JOINT.lower():
        access_level = await read_query(conn, "SELECT access_level FROM users_wallets WHERE user_id = %s", (user_id,))
        if is_withdrawal:
            if not access_level[0][0] == FULL:
                raise NoWithdrawalAccess()
        else:
            if access_level[0][0] not in [TOP_UP_ONLY, FULL]:
                raise NoTopUpAccess()
    if amount < 0:
        get_current_balance = await read_query(conn, "SELECT balance FROM wallets WHERE id = %s", (wallet_id,))
        if get_current_balance[0][0] + amount < 0:
            raise WithdrawMoreThanBalance()
    balance_change = await update_query(conn, "UPDATE wallets SET balance = balance + %s WHERE id = %s",
                                        (amount, wallet_id))
    return True if balance_change else False


async def get_user_id_from_username(conn: Connection, username: str):
    other_user_id = await read_query(conn, "SELECT id FROM users WHERE username =%s", (username,))
    if not other_user_id:
        return None
    return other_user_id[0][0]


async def _create_joint_wallet(conn: Connection, user_id: int, wallet_id):
    await insert_query(conn, "INSERT INTO users_wallets(is_creator, user_id, wallet_id) VALUES(%s, %s, %s)",
                       (IS_TRUE, user_id, wallet_id))


async def _view_group_members(conn: Connection, wallet_id: int):
    get_members = await read_query(conn,
                                   "SELECT u.id, u.username, uw.access_level FROM users u "
                                   "JOIN users_wallets uw on u.id = uw.user_id "
                                   "WHERE uw.wallet_id =%s", (wallet_id,))
    members = [Member.from_query_results(*member) for member in get_members]
    return members


async def _user_has_wallet(conn, user_id: int) -> bool:
    wallet_exists = await read_query(conn, "SELECT id FROM wallets WHERE creator_id= %s", (user_id,))
    return True if wallet_exists else False


async def _add_user_to_joint_wallet(conn: Connection, other_user_id: str, wallet_id: int):
    if not other_user_id:
        return False
    is_added = await read_query(conn, "SELECT user_id FROM users_wallets WHERE user_id = %s and wallet_id = %s",
                                (other_user_id, wallet_id))
    if is_added and is_added[0][0] == other_user_id:
        raise UserAlreadyInGroup()
    add_user = await update_query(conn, "INSERT INTO users_wallets(user_id, wallet_id) VALUES(%s,%s)",
                                  (other_user_id, wallet_id))
    if not add_user:
        return False
    return add_user > 0


async def _remove_user_from_joint_wallet(conn: Connection, user_id: int, wallet_id: int):
    is_wallet_admin = await _is_wallet_admin(conn, user_id)
    if is_wallet_admin == user_id:
        raise CannotRemoveWalletAdmin()
    delete_user = await update_query(conn, "DELETE FROM users_wallets WHERE user_id = %s and wallet_id = %s",
                                     (user_id, wallet_id))
    return True if delete_user else False


async def _amend_user_access_joint_wallet(conn: Connection, access: str, user_id: int, wallet_id: int) -> bool:
    update_access = await update_query(
        conn,
        "UPDATE users_wallets SET access_level = %s WHERE user_id = %s and wallet_id = %s",
        (access, user_id, wallet_id))
    return True if update_access else False


async def _is_wallet_admin(conn: Connection, user_id: int) -> bool:
    is_wallet_admin = await read_query(conn, "SELECT is_creator FROM users_wallets WHERE user_id = %s", (user_id,))
    return True if is_wallet_admin else False


async def _wallet_status(conn: Connection, status: int, wallet_id: int) -> bool:
    set_status = await update_query(conn, "UPDATE wallets SET is_active = %s WHERE id = %s ", (status, wallet_id))
    return True if set_status else False


async def _wallet_exists(conn: Connection, wallet_id: int):
    wallet = await read_query(conn, "SELECT id FROM wallets WHERE id=%s", (wallet_id,))
    return True if wallet else None


async def _change_wallet_name(conn: Connection, wallet_name: str, wallet_id: int):
    updated_name = await update_query(conn, "UPDATE wallets SET name = %s WHERE id= %s", (wallet_name, wallet_id))
    return True if updated_name else False
