from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum
from sqlalchemy.orm import relationship

from configs.database import Base


class WishList(Base):
    __tablename__ = 'wish_list'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)

    users = relationship('User', back_populates='wish_list')
    books = relationship('Book', back_populates='wish_list')
