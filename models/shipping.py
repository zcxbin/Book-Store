from sqlalchemy import Column, Integer, String

from configs.database import Base


class Shipping(Base):
    __tablename__ = 'shipping'
    id = Column(Integer, primary_key=True, nullable=False)
    provider = Column(String(100), nullable=False)
    cost = Column(Integer, nullable=False)
    delivery_time = Column(String(100), nullable=False)
