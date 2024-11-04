from sqlalchemy import Column, Integer, String, Date

from configs.database import Base


class Coupon(Base):
    __tablename__ = 'coupons'
    id = Column(Integer, primary_key = True, index = True, nullable = False)
    code = Column(String, index = True, nullable = False)
    discount = Column(Integer, index = True, nullable = False)
    expiry_date = Column(Date, index = True, nullable = False)
