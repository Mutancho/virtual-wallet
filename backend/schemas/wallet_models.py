from datetime import datetime
from pydantic import BaseModel, constr


class NewWallet(BaseModel):
    name: str
    type: str
    currency: constr(regex=r"(?i)^(USD|EUR|GBP|JPY|CAD|AUD|TRY|BGN)$")


class Member(BaseModel):
    user_id: int
    name: str
    access_level: constr(regex=r"(?i)^(null|top_up_only|full)$")

    @classmethod
    def from_query_results(cls, user_id, name, access_level):
        return cls(user_id=user_id, name=name, access_level=access_level)


class ViewWallet(NewWallet):
    wallet_id: int
    balance: float
    is_active: bool
    created_at: datetime
    default_wallet: bool
    members: list[Member] | None = None

    @classmethod
    def from_query_result(cls, wallet_id, name, type, currency, balance, is_active, default_wallet, created_at,
                          members=None):
        default_wallet = True if default_wallet == 1 else False
        return cls(wallet_id=wallet_id, name=name, type=type, currency=currency, balance=balance, is_active=is_active,
                   default_wallet=default_wallet, created_at=created_at, members=members)


class ViewAllWallets(BaseModel):
    owner: str
    wallets: list[ViewWallet]


class WalletSettings(BaseModel):
    name: str | None
    status: bool | None
    add_username: str | None
    remove_username: str | None
    username: str | None
    change_user_access: constr(regex="^(null|top_up_only|full)$") | None
