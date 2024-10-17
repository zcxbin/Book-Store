from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import Update
from sqlalchemy.orm import Session
from schemas.user import User as UserSchema
from models.user import User as UserModel
from schemas.authentication import Token, Register, UpdateUser
from configs.authentication import verify_password, get_password_hash, create_access_token
from models.role import Role as RoleModel
def get_authentication_service():
    try:
        yield AuthenticationService()
    finally:
        pass


class AuthenticationService:
    def authenticate_user(self, login_data: OAuth2PasswordRequestForm, db: Session) -> Token:
        user = db.query(UserModel).filter(UserModel.username == login_data.username).first()
        role = db.query(RoleModel).filter(RoleModel.id == user.role_id).first()
        if not user:
            return None
        if not verify_password(login_data.password, user.password):
            return None
        print(user.username, role.role_name, user.id)

        access_token = create_access_token(data={
            'username': user.username,
            'role': role.role_name,
            'id': user.id
        })
        return Token(access_token=access_token)

    def register_user(self, register_data: Register, db: Session) -> UserSchema:
        new_user = UserModel(
            username=register_data.username,
            password=get_password_hash(register_data.password),
            role=register_data.role
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserSchema(
            id=new_user.id,
            username=new_user.username,
            role=new_user.role
        )

    def update_user(self, update_data: UpdateUser, db: Session, user_id: int) -> UserSchema:
        user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
        user_model.username = update_data.username
        user_model.username = update_data.username
        user_model.password = get_password_hash(update_data.password)
        user_model.phone_number = update_data.phone_number
        role_model = db.query(RoleModel).filter(RoleModel.id == user_model.role_id).first()
        db.commit()
        return UserSchema(
            username=user_model.username,
            email=user_model.email,
            role=role_model.role_name,
            address=user_model.address
        )

    def delete_user(self, db: Session, user_id: int) -> UserSchema:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        db.delete(user)
        db.commit()
