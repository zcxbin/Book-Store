from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from configs.database import Base


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    publisher_id = Column(Integer, ForeignKey('publishers.id'), nullable=False)
    publication_date = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    img_url = Column(String, nullable=False)
    stock_count = Column(Integer, nullable=False)

    authors = relationship("Author", back_populates="books")
    categories = relationship("Category", back_populates="books")
    publishers = relationship("Publisher", back_populates="books")
    order_items = relationship("OrderItem", back_populates="books")
    reviews = relationship("Review", back_populates="books")
    wish_list = relationship("WishList", back_populates="books")
