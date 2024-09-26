from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum
from sqlalchemy.orm import relationship

from configs.database import Base


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    role_name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    role_permissions = relationship('RolePermission', back_populates='roles')
    user_roles = relationship('UserRole', back_populates='role')
