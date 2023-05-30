from pydantic import BaseModel, PositiveFloat, constr
from datetime import datetime,date


class Transaction(BaseModel):
    amount: PositiveFloat
    category: constr(regex=r'^(Rent|Utilities|Food & Groceries|Transportation|Health & Fitness|Shopping & Entertainment|Travel|Education|Personal Care|Investments & Savings|Other)$') | None
    recipient: str
    wallet: int
    is_recurring: bool | None
    start_date: date | None
    interval: int | None

    @classmethod
    def from_query_result(cls, amount, category, recipient, wallet, is_recuring):
        return cls(amount=amount, category=category, recipient=recipient, wallet=wallet,
                   is_recuring=is_recuring)

class DisplayTransaction(BaseModel):
    information: str
    amount: PositiveFloat
    category: str
    recipient: str
    wallet: int
    is_recurring: bool | None
    interval: int | None


    @classmethod
    def from_query_result(cls,information,amount,category,recipient,wallet,is_recuring):
        return cls(information=information,amount=amount,category=category,recipient=recipient,wallet=wallet,is_recuring=is_recuring)

class DisplayTransactionInfo(BaseModel):
    amount: PositiveFloat
    category: str
    recipient: str
    wallet: int
    is_recurring: bool
    sent_at: date
    accepted:bool
    received_at: date

    @classmethod
    def from_query_result(cls,amount,category,recipient,wallet,is_recurring,sent_at,accepted,received_at):
        return cls(amount=amount,category=category,recipient=recipient,wallet=wallet,is_recurring=bool(is_recurring),sent_at=sent_at,accepted=bool(accepted),received_at=received_at)

