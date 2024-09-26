from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum
from sqlalchemy.orm import relationship

from configs.database import Base


class UserRole(Base):
    __tablename__ = 'user_role'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    role_id = Column(Integer, ForeignKey('role.id'))

    users = relationship('User', back_populates='user_roles')
    roles = relationship('Role', back_populates='user_roles')
