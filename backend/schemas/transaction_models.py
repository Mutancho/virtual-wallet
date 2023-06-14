from pydantic import BaseModel, PositiveFloat, constr
from datetime import date


class Transaction(BaseModel):
    amount: PositiveFloat
    category: constr(regex=r'^(Rent|Utilities|Food & Groceries|Transportation|Health & Fitness|Shopping &'
                           r' Entertainment|Travel|Education|Personal Care|Investments & Savings|Other)$') | None
    recipient: str
    wallet: int
    is_recurring: bool | None
    start_date: date | None
    interval: int | None

    @classmethod
    def from_query_result(cls, amount, category, recipient, wallet, is_recurring):
        return cls(amount=amount, category=category, recipient=recipient, wallet=wallet,
                   is_recurring=is_recurring)


class DisplayTransaction(BaseModel):
    information: str
    amount: PositiveFloat
    category: str
    recipient: str
    wallet: int
    is_recurring: bool | None
    interval: int | None

    @classmethod
    def from_query_result(cls, information, amount, category, recipient, wallet, is_recurring):
        return cls(information=information, amount=amount, category=category, recipient=recipient, wallet=wallet,
                   is_recurring=is_recurring)


class DisplayTransactionInfo(BaseModel):
    amount: PositiveFloat
    category: str
    recipient: str
    wallet: str
    is_recurring: bool
    sent_at: date
    accepted: bool
    received_at: date | None
    currency: str

    @classmethod
    def from_query_result(cls, amount, category, recipient, wallet, is_recurring, sent_at, accepted, received_at,
                          currency):
        return cls(amount=amount, category=category, recipient=recipient, wallet=wallet,
                   is_recurring=bool(is_recurring), sent_at=sent_at, accepted=bool(accepted), received_at=received_at,
                   currency=currency)


class PendingTransaction(BaseModel):
    id: int
    amount: PositiveFloat
    category: str
    is_recurring: bool
    sent_at: date
    accepted: bool
    currency: str

    @classmethod
    def from_query_result(cls, id, amount, category, is_recurring, sent_at, accepted, currency):
        return cls(id=id, amount=amount, category=category, is_recurring=bool(is_recurring), sent_at=sent_at,
                   accepted=bool(accepted), currency=currency)
