from pydantic import BaseModel


class PaymentCard(BaseModel):
    id: str
