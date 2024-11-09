from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from configs.database import Base


class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    publisher_name = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)

    books = relationship('Book', back_populates='publishers')
