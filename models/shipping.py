from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum
from sqlalchemy.orm import relationship

from configs.database import Base


class Shipping(Base):
    __tablename__ = 'shipping'
    id = Column(Integer, primary_key=True)
    provider = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)
    delivery_time = Column(String, nullable=False)
