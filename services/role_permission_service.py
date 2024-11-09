from typing import Type

from sqlalchemy.orm import Session

from models import RolePermission as RolePermissionModel
from schemas.role_permission import RolePermission as RolePermissionSchema, RolePermissionCreate, RolePermissionUpdate


def get_role_permission_service():
    try:
        yield RolePermissionService()
    finally:
        pass


class RolePermissionService:
    def get_role_permissions(self, db: Session) -> list[Type[RolePermissionSchema]]:
        return db.query(RolePermissionModel).all()

    def create_role_permission(self, db: Session, role_permission: RolePermissionCreate) -> \
            list[Type[RolePermissionSchema]]:
        new_role_permission = RolePermissionModel(
            role_id=role_permission.role_id,
            permission_id=role_permission.permission_id,
        )

        db.add(new_role_permission)
        db.commit()
        db.refresh(new_role_permission)
        return db.query(RolePermissionModel).all()

    def update_role_permission(self, db: Session, role_permission_update: RolePermissionUpdate,
                               role_permission_id: int) -> list[Type[RolePermissionSchema]]:
        role_permission_model = db.query(RolePermissionModel).filter(
            RolePermissionModel.id == role_permission_id
        ).first()
        role_permission_model.permission_id = role_permission_update.permission_id
        role_permission_model.role_id = role_permission_update.role_id
        db.commit()
        db.refresh(role_permission_model)
        return db.query(RolePermissionModel).all()

    def delete_role_permission(self, db: Session, role_permission_id: int) -> list[Type[RolePermissionSchema]]:
        role_permission_model = db.query(RolePermissionModel).filter(
            role_permission_id == RolePermissionModel.id
        ).first()
        db.delete(role_permission_model)
        db.commit()
        return db.query(RolePermissionModel).all()
