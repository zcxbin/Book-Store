from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from configs.database import Base


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String(100), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    publisher_id = Column(Integer, ForeignKey('publishers.id'), nullable=False)
    publication_date = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    discount = Column(Integer, nullable=False)
    description = Column(String(100), nullable=False)
    image_url = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)

    authors = relationship("Author", back_populates="books")
    categories = relationship("Category", back_populates="books")
    publishers = relationship("Publisher", back_populates="books")
    order_items = relationship("OrderItem", back_populates="books")
    reviews = relationship("Review", back_populates="books")
    wish_list = relationship("WishList", back_populates="books")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.authors.to_dict(),
            'category_id': self.category_id,
            'publication_date': self.publication_date,
            'price': self.price,
            'discount': self.discount,
            'description': self.description,
            'quantity': self.quantity,

        }
