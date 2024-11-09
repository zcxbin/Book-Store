from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from configs.database import Base


class Permission(Base):
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    activity = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)

    role_permissions = relationship("RolePermission", back_populates="permissions")
