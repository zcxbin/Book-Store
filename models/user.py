from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum
from sqlalchemy.orm import relationship

from configs.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), default=2)

    orders = relationship('Order', back_populates='users')
    roles = relationship('Role', back_populates='users')
    reviews = relationship('Review', back_populates='users')
    wish_list = relationship('WishList', back_populates='users')
