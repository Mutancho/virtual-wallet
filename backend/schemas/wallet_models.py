from datetime import datetime
from pydantic import BaseModel, constr
import re


class NewWallet(BaseModel):
    type: str
    currency: constr(regex=r"^(USD|EUR|GBP|JPY|CAD|AUD|TRY|BGN)$")


class ViewWallet(NewWallet):
    wallet_id: int
    balance: float
    is_active: bool
    created_at: datetime
    default_wallet: bool
    members: list[str] | None = None

    @classmethod
    def from_query_result(cls, wallet_id, type, currency, balance, is_active, default_wallet, created_at,
                          members=None):
        default_wallet = True if default_wallet == 1 else False
        return cls(wallet_id=wallet_id, type=type, currency=currency, balance=balance, is_active=is_active,
                   default_wallet=default_wallet, created_at=created_at, members=members)


class ViewAllWallets(BaseModel):
    owner: str
    wallets: list[ViewWallet]
