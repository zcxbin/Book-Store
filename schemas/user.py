from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    role: str
    address: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    username: str
    email: str
    role: str
    address: str

    class Config:
        from_attributes = True
