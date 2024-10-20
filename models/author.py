from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship

from configs.database import Base


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    author_name = Column(String(100), nullable=False)
    bio = Column(String(100), nullable=False)

    books = relationship("Book", back_populates="authors")
