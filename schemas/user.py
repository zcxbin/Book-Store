from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    address: str
    role: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    username: str
    email: str
    role: str
    address: str

    class Config:
        from_attributes = True
