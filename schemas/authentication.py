from pydantic import BaseModel
from models import User


class Register(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str
    address: str

    class Config:
        from_attributes = True

class LoginReq(BaseModel):
    username: str
    password: str
class UserOut(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    phone_number: str
    address: str
    role_id: int
    role_name: str


class UpdateUser(BaseModel):
    username: str
    password: str
    address: str
    phone_number: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
    user: UserOut
    
    class Config:
        arbitrary_types_allowed=True


class TokenData(BaseModel):
    username: str = None
    role: str = None
    id: int = None
