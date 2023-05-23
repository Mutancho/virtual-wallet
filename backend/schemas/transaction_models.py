from pydantic import BaseModel, PositiveFloat, constr


class Transaction(BaseModel):
    amount: PositiveFloat
    category: constr(regex='''(?i)^(Rent|Utilities|Food & Groceries|Transportation|Health & Fitness|Shopping & Entertainment|Travel|Education|Personal Care|Invesments & Savings|Other)$''') | None
    recipient: int
    wallet: int
    is_recurring: bool | None

    @classmethod
    def from_query_result(cls, amount, category, recipient, wallet, is_recuring):
        return cls(amount=amount, category=category, recipient=recipient, wallet=wallet,
                   is_recuring=is_recuring)

class DisplayTransaction(BaseModel):
    information: str
    amount: PositiveFloat
    category: str
    recipient: int
    wallet: int
    is_recurring: bool | None

    @classmethod
    def from_query_result(cls,information,amount,category,recipient,wallet,is_recuring):
        return cls(information=information,amount=amount,category=category,recipient=recipient,wallet=wallet,is_recuring=is_recuring)

