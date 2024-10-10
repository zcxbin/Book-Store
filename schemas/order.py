from datetime import datetime
from typing import List

from pydantic import BaseModel
from schemas.order_item import OrderItem


class Order(BaseModel):
    id: str
    user_id: int
    order_date: datetime
    status: str
    total_price: int
    user_address: str

    class Config:
        from_attributes: True


class OrderItemCreate(BaseModel):
    items: List[OrderItem]
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    order: list[OrderItem] = []
    length: int = 0

    class Config:
        from_attributes = True
