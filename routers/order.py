from fastapi import APIRouter, Depends

from configs.authentication import get_current_user
from configs.database import get_db
from exceptions import raise_error
from schemas.order import OrderItemCreate
from services.order_sevice import get_order_service

router = APIRouter()


@router.get('/get_all_orders')
def get_all_orders(
        db=Depends(get_db),
        user=Depends(get_current_user),
        order_service=Depends(get_order_service)
):
    try:
        if user.role != 'admin':
            return raise_error(401)

        orders = order_service.get_all_orders(db)
        if not orders:
            return raise_error(501)
        return orders
    except Exception as e:
        print(e)


@router.get('/get_order_by_user_id')
async def get_order_by_user_id(
        user=Depends(get_current_user),
        db=Depends(get_db),
        order_service=Depends(get_order_service)
):
    try:
        orders = order_service.get_order_by_user_id(db, user.id)
        if not orders:
            return raise_error(501)
        return orders
    except Exception as e:
        print(e)


@router.post('/create_orders')
async def create_order(
        order: OrderItemCreate,
        user=Depends(get_current_user),
        db=Depends(get_db),
        order_service=Depends(get_order_service)
):
    try:
        return order_service.create_order(db, order, user.id)
    except Exception as e:
        print(e)


@router.put('/update_order_status')
async def update_order_status(
        status: str,
        order_id: int,
        user=Depends(get_current_user),
        db=Depends(get_db),
        order_service=Depends(get_order_service)
):
    try:
        if user.role != 'admin':
            return raise_error(401)
        return order_service.update_order_status(db, order_id, status)
    except Exception as e:
        print(e)


@router.delete('/delete_orders')
async def delete_order(
        order_id: int,
        user=Depends(get_current_user),
        db=Depends(get_db),
        order_service=Depends(get_order_service)
):
    try:
        return order_service.delete_order_by_user_id(db, user.id, order_id)
    except Exception as e:
        print(e)
