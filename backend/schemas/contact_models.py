from pydantic import BaseModel, EmailStr


class Contact(BaseModel):
    username: str
    email: EmailStr | None
    phone_number: str | None
