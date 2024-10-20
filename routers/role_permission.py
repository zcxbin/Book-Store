from fastapi import APIRouter, Depends

from configs.authentication import get_current_user
from configs.database import get_db
from exceptions import raise_error
from schemas.role_permission import RolePermission as RolePermissionSchema, RolePermissionUpdate, RolePermissionCreate
from services.role_permission_service import get_role_permission_service

router = APIRouter()


@router.get("/get_all_permission")
async def get_all_permission(
        db=Depends(get_db),
        user=Depends(get_current_user),
        role_permission_service=Depends(get_role_permission_service)
):
    try:
        if user.role != 'admin':
            return raise_error(401)
        return role_permission_service.get_role_permissions(db)
    except Exception as e:
        print(e)


@router.post("/create_role_permission")
async def create_role_permission(
        role_permission_create: RolePermissionCreate,
        db=Depends(get_db),
        user=Depends(get_current_user),
        role_permission_service=Depends(get_role_permission_service)
):
    try:
        if user.role != 'admin':
            return raise_error(401)
        return role_permission_service.create_role_permission(db, role_permission_create)
    except Exception as e:
        print(e)


@router.put("/update_role_permission")
async def update_role_permission(
        role_permission_id: int,
        role_permission_update: RolePermissionUpdate,
        db=Depends(get_db),
        user=Depends(get_current_user),
        role_permission_service=Depends(get_role_permission_service)
):
    try:
        if user.role != 'admin':
            return raise_error(401)
        return role_permission_service.update_role_permission(db, role_permission_update, role_permission_id)
    except Exception as e:
        print(e)


@router.delete("/delete_role_permission")
async def delete_role_permission(
        role_permission_id: int,
        db=Depends(get_db),
        user=Depends(get_current_user),
        role_permission_service=Depends(get_role_permission_service)
):
    try:
        if user.role != 'admin':
            return raise_error(401)
        return role_permission_service.delete_role_permission(db, role_permission_id)
    except Exception as e:
        print(e)
