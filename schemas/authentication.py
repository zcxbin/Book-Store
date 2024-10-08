from pydantic import BaseModel


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


class TokenData(BaseModel):
    username: str = None
    role: str = None
    id: int = None
