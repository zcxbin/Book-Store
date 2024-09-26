from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum
from sqlalchemy.orm import relationship

from configs.database import Base


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    order_id = Column(DateTime, ForeignKey('orders.id'), nullable=False)
    status = Column(Enum('Pending', 'Shipped', 'Delivered', 'Canceled'), nullable=False)
    total_price = Column(Integer, nullable=False)
    user_address = Column(String, nullable=False)
    payment_method = Column(Enum('PayPal', 'PayPal', 'PayPalPayments'))

    order_items = relationship('OrderItem', back_populates='order')
    users = relationship('User', back_populates='orders')
