from datetime import datetime
from typing import List, Type

from sqlalchemy import and_
from sqlalchemy.orm import Session

from exceptions import raise_error
from models.order import Order as OrderModel
from models.order_item import OrderItem
from schemas.order import OrderResponse, OrderItemCreate, Order
from models.user import User as UserModel
from models.book import Book as BookModel


def get_order_service():
    try:
        yield OrderService()
    finally:
        pass


class OrderService:
    def get_all_orders(self, db: Session) -> list[Type[Order]]:
        return db.query(OrderModel).all()

    def get_order_by_user_id(self, db: Session, user_id: int) -> list[Type[Order]]:
        return db.query(OrderModel).filter(OrderModel.user_id == user_id).all()

    def update_order_status(self, db: Session, order_id: int, status: str) -> list[Type[Order]]:
        order = db.query(OrderModel).filter(OrderModel.id == order_id).first()
        order.status = status
        db.commit()
        return db.query(OrderModel).all()

    def create_order(self, db: Session, order: OrderItemCreate, user_id: int) -> list[Type[Order]]:
        total_amount = 0

        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        is_valid = True
        user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
        new_order = OrderModel(user_id=user_id, order_date=current_date)

        for item in order.items:
            if item.quantity < 0:
                is_valid = False

            book_model = db.query(BookModel).filter(BookModel.id == item.book_id).first()
            if book_model.quantity < item.quantity:
                raise_error(301)
            elif book_model.quantity < 0:
                raise_error(302)
            else:
                total_amount += book_model.price * item.quantity
                order_item_model = OrderItem(
                    book_id=book_model.id,
                    order_id=new_order.id,
                    quantity=item.quantity,
                    price=book_model.price,
                )
                book_model.quantity -= item.quantity
                new_order.order_items.append(order_item_model)

        if is_valid:
            new_order.total_price = total_amount
            new_order.user_address = user_model.address
            db.add(new_order)
            db.commit()

        return db.query(OrderModel).filter(OrderModel.user_id == user_id).all()

    def delete_order_by_user_id(self, db: Session, user_id: int, order_id: int) -> list[Type[Order]]:
        order_model = db.query(OrderModel).filter(and_(
            OrderModel.user_id == user_id,
            OrderModel.id == order_id,
        )).first()
        if order_model is None:
            raise_error(404)

        order_item_models = db.query(OrderItem).filter(OrderItem.order_id == order_id).all()
        for item in order_item_models:
            book_model = db.query(BookModel).filter(BookModel.id == item.book_id).first()
            book_model.quantity += item.quantity
            db.delete(item)
        db.delete(order_model)
        db.commit()

        return db.query(OrderModel).filter(OrderModel.user_id == user_id).all()
