from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from configs.database import Base


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    type_name = Column(String(100), unique=True, nullable=False)

    books = relationship('Book', back_populates='categories')
