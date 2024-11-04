from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from configs.database import Base


class RolePermission(Base):
    __tablename__ = 'role_permission'
    id = Column(Integer, primary_key = True, index = True, nullable = False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable = False)
    permission_id = Column(Integer, ForeignKey('permission.id'), nullable = False)

    roles = relationship("Role", back_populates = "role_permissions")
    permissions = relationship("Permission", back_populates = "role_permissions")
