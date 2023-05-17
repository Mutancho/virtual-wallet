from pydantic import BaseModel,constr,EmailStr,validator
import re
from datetime import datetime,date
def validate_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[~!@#$%^&*_\-+=|(){}[\]:;<>.,/?]).{8,}$"
    return re.match(pattern, password) is not None

def validate_bg_phone_number(phone_number):
    pattern = r'^\+?(359)?0[7-9][0-9]{8}$'
    return re.match(pattern, phone_number) is not None
class RegisterUser(BaseModel):
    id: int|None
    username: constr(min_length=2,max_length=20)
    password: str
    email: EmailStr
    first_name: constr(min_length=1,max_length=20)
    last_name: constr(min_length=1,max_length=20)
    phone_number: str
    two_factor_auth: constr(regex='(?i)\b(?:email|sms)\b')|None
    title: constr(regex='^(Mr|Mrs|Miss|Ms|Dr|Prof)$')|None
    gender: constr(regex='^(male|female|other)$')|None
    date_of_birth: str
    address: str
    photo_selfie: bytes|None
    identity_document: bytes|None


    @validator('password')
    def password_validation(cls, password):
        if not validate_password(password):
            raise ValueError(
                "Password must contain at least one uppercase letter, one digit, one special symbol, and have a minimum length of 8 characters")
        return password

    @validator('phone_number')
    def phone_number_validation(cls, phone_number):
        if not validate_bg_phone_number(phone_number):
            raise ValueError("Invalid Bulgarian phone number")
        return phone_number

    @validator('date_of_birth')
    def validate_birth_date(cls, value):
        try:
            date_obj = datetime.strptime(value, '%d.%m.%Y').date()
        except ValueError:
            raise ValueError('Invalid date format. Expected format: day.month.year')
        return date_obj

class UsernameLogin(BaseModel):
    username: constr(min_length=2,max_length=20)
    password: str


class EmailLogin(BaseModel):
    email: EmailStr
    password: str



