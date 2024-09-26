from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum
from sqlalchemy.orm import relationship

from configs.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    phone_number = Column(String(50), unique=True, nullable=False)
    address = Column(String(50), unique=True, nullable=False)

    orders = relationship('Order', back_populates='users')
    user_roles = relationship('Role', back_populates='users')
    wish_list = relationship('WishList', back_populates='user')
