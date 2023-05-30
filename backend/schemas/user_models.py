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
    two_factor_method: constr(regex='(?i)\b(?:email|sms)\b')|None
    title: constr(regex='^(Mr|Mrs|Miss|Ms|Dr|Prof)$')|None
    gender: constr(regex='^(male|female|other)$')|None
    date_of_birth: str
    address: str
    photo_selfie: str|None
    identity_document: str|None


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

class DisplayUser(BaseModel):
    username: str
    email:str
    phone_number: str
    first_name: str
    last_name:str
    address:str

    @classmethod
    def from_query_result(cls,username:str,email:str,phone_number: str,first_name: str,last_name:str,address:str):
        return cls(username=username,email=email,phone_number=phone_number,first_name=first_name,last_name=last_name,address=address)


class UpdateUser(BaseModel):
    old_password: str | None
    new_password: str | None
    repeat_password: str | None
    email: EmailStr | None
    first_name: constr(min_length=1, max_length=20) | None
    last_name: constr(min_length=1, max_length=20) | None
    phone_number: str | None
    two_factor_method: constr(regex='(?i)(email|sms)') | None
    title: constr(regex='^(Mr|Mrs|Miss|Ms|Dr|Prof)$') | None
    gender: constr(regex='^(male|female|other)$') | None
    address: str | None
    photo_selfie: str | None
    identity_document: str | None

    @validator('new_password')
    def password_validation(cls, new_password,allow_reuse=True):
        if not validate_password(new_password):
            raise ValueError(
                "Password must contain at least one uppercase letter, one digit, one special symbol, and have a minimum length of 8 characters")
        return new_password

    @validator('repeat_password',allow_reuse=True)
    def password_validation(cls, repeat_password):
        if not validate_password(repeat_password):
            raise ValueError(
                "Password must contain at least one uppercase letter, one digit, one special symbol, and have a minimum length of 8 characters")

        return repeat_password

    @validator('phone_number')
    def phone_number_validation(cls, phone_number):
        if not validate_bg_phone_number(phone_number):
            raise ValueError("Invalid Bulgarian phone number")
        return phone_number

    @classmethod
    def from_query_result(cls, password: str, email: str,first_name: str, last_name: str, phone_number: str, two_factor_method:str,title:str,
                          gender:str,photo_selfie:bytes,identity_document:bytes,address: str):
        return cls(old_password=password, email=email, phone_number=phone_number, first_name=first_name,
                   last_name=last_name, address=address,two_factor_method=two_factor_method,title=title,gender=gender,photo_selfie=photo_selfie,identity_document=identity_document)


class AfterUpdateUser(BaseModel):
    username:str
    password: str | None
    email: EmailStr | None
    first_name: constr(min_length=1, max_length=20) | None
    last_name: constr(min_length=1, max_length=20) | None
    phone_number: str | None
    two_factor_method: constr(regex='(?i)\b(?:email|sms)\b') | None
    title: constr(regex='^(Mr|Mrs|Miss|Ms|Dr|Prof)$') | None
    gender: constr(regex='^(male|female|other)$') | None
    address: str | None
    photo_selfie: str | None
    identity_document: str | None


    @classmethod
    def from_query_result(cls,username, password: str, email: str,first_name: str, last_name: str, phone_number: str, two_factor_method:str,title:str,
                          gender:str,photo_selfie:bytes,identity_document:bytes,address: str):
        return cls(username=username,password=password, email=email, phone_number=phone_number, first_name=first_name,
                   last_name=last_name, address=address,two_factor_method=two_factor_method,title=title,gender=gender,photo_selfie=photo_selfie,identity_document=identity_document)


class BlockUnblock(BaseModel):
    action:constr(regex='(?i)^(block|unblock)$')

class Username(BaseModel):
    username:str

