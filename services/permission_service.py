from sqlalchemy.orm import Session

from models.permission import Permission as PermissionModel
from schemas.permission import Permission as PermissionSchema, PermissionCreate, PermissionUpdate


def get_permission_service():
    try:
        yield PermissionService()
    finally:
        pass


class PermissionService:
    def get_all_permissions(self, db: Session) -> list[type[PermissionSchema]]:
        return db.query(PermissionModel).all()

    def create_permission(self, db: Session, permission: PermissionCreate) -> PermissionSchema:
        new_permission = PermissionModel(
            activity=permission.activity,
            description=permission.description,
        )
        db.add(new_permission)
        db.commit()
        db.refresh(new_permission)
        return new_permission

    def update_permission(self, db: Session, permission: PermissionUpdate, permission_id: int) -> PermissionSchema:
        permission_model = db.query(PermissionModel).filter(PermissionModel.id == permission_id).first()

        permission_model.activity = permission.activity
        permission_model.description = permission.description
        db.commit()
        db.refresh(permission_model)
        return permission_model

    def delete_permission(self, db: Session, permission_id: int) -> list[type[PermissionSchema]]:
        permission_model = db.query(PermissionModel).filter(PermissionModel.id == permission_id).first()
        db.delete(permission_model)
        db.commit()
        return db.query(PermissionModel).all()
