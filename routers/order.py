from fastapi import APIRouter, Depends

from configs.authentication import get_current_user
from configs.database import get_db
from schemas.order import OrderItemCreate, OrderResponse
from services.order_service import get_order_service

router = APIRouter()


@router.post('/create_orders', response_model=OrderResponse)
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
