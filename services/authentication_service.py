from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import Update
from sqlalchemy.orm import Session

from models import Role as RoleModel
from models.user import User as UserModel
from schemas.authentication import Token, Register, UpdateUser
from schemas.user import User as UserSchema
from configs.authentication import verify_password, get_password_hash, create_access_token


def get_authentication_service():
    try:
        yield AuthenticationService()
    finally:
        pass


class AuthenticationService:
    def authenticate_user(self, login_data: OAuth2PasswordRequestForm, db: Session) -> Token:
        user = db.query(UserModel).filter(UserModel.username == login_data.username).first()
        role = db.query(RoleModel).filter(user.role_id == RoleModel.id).first()
        if not user:
            return None
        if not verify_password(login_data.password, user.password):
            return None
        # print(user.username, user.role, user.id)

        access_token = create_access_token(data={
            'username': user.username,
            'role': role.role_name,
            'id': user.id
        })
        return Token(access_token=access_token)

    def register_user(self, register_data: Register, db: Session) -> UserSchema:
        try:
            new_user = UserModel(
                username=register_data.username,
                email=register_data.email,
                password=get_password_hash(register_data.password),
                first_name=register_data.first_name,
                last_name=register_data.last_name,
                phone_number=register_data.phone_number,
                address=register_data.address,
                role_id=2
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            user_role = db.query(RoleModel).filter(new_user.role_id == RoleModel.id).first()
            return UserSchema(
                id=new_user.id,
                username=new_user.username,
                email=new_user.email,
                phone_number=new_user.phone_number,
                address=new_user.address,
                role=user_role.role_name
            )
        except Exception as e:
            print(e)
