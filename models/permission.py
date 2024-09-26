from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, Enum
from sqlalchemy.orm import relationship

from configs.database import Base


class Permission(Base):
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    activity = Column(String, nullable=False)
    description = Column(String, nullable=False)

    role_permission = relationship("RolePermission", back_populates="permissions")
