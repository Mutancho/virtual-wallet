from pydantic import BaseModel,constr,EmailStr,validator

class Contact(BaseModel):
    username: str
    email:EmailStr | None
    phone_number: str | None
