from fastapi import Depends, APIRouter

from configs.authentication import get_current_user
from configs.database import get_db
from exceptions import raise_error
from schemas.permission import PermissionCreate, PermissionUpdate
from services.permission_service import get_permission_service

router = APIRouter()


@router.get('/get_all_permission')
async def get_all_permission(
        user=Depends(get_current_user),
        db=Depends(get_db),
        permission_service=Depends(get_permission_service),
):
    try:
        if user.role != 'admin':
            return raise_error(401)
        return permission_service.get_all_permissions(db)
    except Exception as e:
        print(e)


@router.post('/create_permission')
async def create_permission(
        permission_data: PermissionCreate,
        permission_service=Depends(get_permission_service),
        db=Depends(get_db),
        user=Depends(get_current_user)
):
    try:
        if user.role != 'admin':
            return raise_error(401)
        return permission_service.create_permission(db, permission_data)
    except Exception as e:
        print(e)


@router.put('/update_permission')
async def update_permission(
        permission_id: int,
        permission_data: PermissionUpdate,
        permission_service=Depends(get_permission_service),
        db=Depends(get_db),
        user=Depends(get_current_user)
):
    try:
        if user.role != 'admin':
            return raise_error(401)
        return permission_service.update_permission(db, permission_data, permission_id)
    except Exception as e:
        print(e)


@router.delete('/delete_permission')
async def delete_permission(
        permission_id: int,
        permission_service=Depends(get_permission_service),
        db=Depends(get_db),
        user=Depends(get_current_user)
):
    try:
        if user.role != 'admin':
            return raise_error(401)
        return permission_service.delete_permission(db, permission_id)
    except Exception as e:
        print(e)
