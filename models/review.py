from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from configs.database import Base


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(String(100), nullable=False)
    created_at = Column(String(100), nullable=False)

    users = relationship('User', back_populates='reviews')
    books = relationship('Book', back_populates='reviews')
