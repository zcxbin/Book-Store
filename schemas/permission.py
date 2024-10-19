from typing import List

from pydantic import BaseModel


class Permission(BaseModel):
    id: int
    activity: str
    description: str

    class Config:
        from_attributes = True


class PermissionCreate(BaseModel):
    activity: str
    description: str

    class Config:
        from_attributes = True


class PermissionUpdate(BaseModel):
    activity: str
    description: str

    class Config:
        from_attributes = True


class PermissionResponse(BaseModel):
    permissions: List[Permission] = []
    length: int = 0

    class Config:
        from_attributes = True
