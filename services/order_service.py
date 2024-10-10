from datetime import datetime

from sqlalchemy.orm import Session

from exceptions import raise_error
from models.order import Order as OrderModel
from models.user import User as UserModel
from models.order_item import OrderItem
from models.book import Book as BookModel
from schemas.order import OrderItemCreate, OrderResponse


def get_order_service():
    try:
        yield OrderService()
    finally:
        pass

class OrderService:
    def create_order(self, db: Session, order: OrderItemCreate, user_id: int) -> OrderResponse:
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

        return OrderResponse(
            id=new_order.id,
            user_id=new_order.user_id,
            order_date=new_order.order_date,
            status=new_order.status,
            total_price=new_order.total_price,
            user_address=user_model.address,
        )
