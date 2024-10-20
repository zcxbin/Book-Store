from pydantic import BaseModel


class RolePermission(BaseModel):
    id: int
    role_id: int
    permission_id: int

    class Config:
        from_attributes = True


class RolePermissionCreate(BaseModel):
    role_id: int
    permission_id: int

    class Config:
        from_attributes = True


class RolePermissionUpdate(BaseModel):
    role_id: int
    permission_id: int

    class Config:
        from_attributes = True

