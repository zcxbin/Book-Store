from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum
from sqlalchemy.orm import relationship

from configs.database import Base


class Publisher(Base):
    __tablename__ = 'publishers'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)

    books = relationship('Book', back_populates='publishers')
