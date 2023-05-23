from pydantic import BaseModel, EmailStr
from datetime import datetime, date


class Referral(BaseModel):
    email: EmailStr


class ViewReferrals(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    expiry_date: date
    link: str
    is_used: bool

    @classmethod
    def read_from_query(cls, id, email, created_at, expiry_date, link, is_used):
        return cls(id=id, email=email, created_at=created_at, expiry_date=expiry_date, link=link, is_used=is_used)
