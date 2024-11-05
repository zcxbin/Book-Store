from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from configs.database import Base


class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)

    orders = relationship("Order", back_populates="order_items")
    books = relationship("Book", back_populates="order_items")
