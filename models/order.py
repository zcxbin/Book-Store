from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from configs.database import Base


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    order_date = Column(String(100), nullable=False)
    status = Column(String(100), nullable=False, default='Pending')
    total_price = Column(Integer, nullable=False)
    user_address = Column(String(100), nullable=False)

    order_items = relationship('OrderItem', back_populates='orders')
    users = relationship('User', back_populates='orders')
