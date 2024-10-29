from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from schemas.user import User as UserSchema
from models.user import User as UserModel
from schemas.authentication import Token, Register, UpdateUser
from configs.authentication import verify_password, get_password_hash, create_access_token
from models.role import Role as RoleModel
from models.review import Review as ReviewModel

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
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        if not verify_password(login_data.password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect password')
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
            email=register_data.email,
            password=get_password_hash(register_data.password),
            first_name=register_data.first_name,
            last_name=register_data.last_name,
            phone_number=register_data.phone_number,
            address=register_data.address
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        role_model = db.query(RoleModel).filter(RoleModel.id == new_user.role_id).first()
        return UserSchema(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            address=new_user.address,
            role=role_model.role_name
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
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            role=role_model.role_name,
            address=user_model.address
        )

    def delete_user(self, db: Session, user_id: int) -> list[type[UserSchema]]:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        user_reviews = db.query(ReviewModel).filter(ReviewModel.user_id == user.id).all()
        for review in user_reviews:
            db.delete(review)
        db.delete(user)
        db.commit()
        return db.query(UserModel).all()
