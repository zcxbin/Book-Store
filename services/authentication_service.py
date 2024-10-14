from typing import Union

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from exceptions import raise_error
from models import Role as RoleModel
from models.user import User as UserModel
from schemas.authentication import Token, Register, UpdateUser
from schemas.base_response import BaseResponse
from schemas.user import User as UserSchema, UserResponse
from configs.authentication import verify_password, get_password_hash, create_access_token


def get_authentication_service():
    try:
        yield AuthenticationService()
    finally:
        pass


class AuthenticationService:
    def authenticate_user(self, login_data: OAuth2PasswordRequestForm, db: Session) -> Union[raise_error, Token]:
        user = db.query(UserModel).filter(UserModel.username == login_data.username).first()
        role = db.query(RoleModel).filter(user.role_id == RoleModel.id).first()
        if not user:
            return raise_error(402)
        if not verify_password(login_data.password, user.password):
            return raise_error(401)
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

    def update_user(self, update_data: UpdateUser, db: Session, user_id: int) -> UserResponse:
        user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
        user_model.username = update_data.username
        user_model.password = get_password_hash(update_data.password)
        user_model.address = update_data.address
        user_model.phone_number = update_data.phone_number
        role_model = db.query(RoleModel).filter(RoleModel.id == user_model.role_id).first()
        db.commit()
        return UserResponse(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            address=user_model.address,
            role=role_model.role_name
        )

    def delete_user(self, db: Session, user_id: int):
        user_model = db.query(UserModel).filter(UserModel.id == user_id).first()
        db.delete(user_model)
        db.commit()

