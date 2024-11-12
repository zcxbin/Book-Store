from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from configs.authentication import verify_password, get_password_hash, create_access_token
from models.review import Review as ReviewModel
from models.role import Role as RoleModel
from models.user import User as UserModel
from schemas.authentication import Token, Register, UpdateUser, LoginReq, UserOut
from configs.authentication import verify_password, get_password_hash, create_access_token
from models.role import Role as RoleModel
from models.review import Review as ReviewModel
from schemas.authentication import Token, Register, UpdateUser
from schemas.user import User as UserSchema

def get_authentication_service():
    try:
        yield AuthenticationService()
    finally:
        pass


class AuthenticationService:
    def authenticate_user(self, login_data: LoginReq, db: Session) -> Token:
        user = db.query(UserModel).filter(UserModel.username == login_data.username).first()
        role = db.query(RoleModel).filter(RoleModel.id == user.role_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        if not verify_password(login_data.password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect password')
        print(user.username, role.role_name, user.id)
        
        user_out = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "address": user.address,
            "role_id": user.role_id
        }
        access_token = create_access_token(data={
            'username': user.username,
            'role': role.role_name,
            'id': user.id
        })
        return Token(
            access_token=access_token,
            user=user_out
        )
    def login(self, login_data: LoginReq, db: Session) -> Token:
        user = db.query(UserModel).filter(UserModel.username == login_data.username).first()
        role = db.query(RoleModel).filter(RoleModel.id == user.role_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        if not verify_password(login_data.password, user.password):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect password')
        print(user.username, role.role_name, user.id)

        user_out = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "address": user.address,
            "role_id": user.role_id,
            "role_name": role.role_name
        }
        access_token = create_access_token(data={
            'username': user.username,
            'role': role.role_name,
            'id': user.id
        })
        return Token(
            access_token=access_token,
            user=user_out
        )
    
    def get_user_by_id(self, id: int, db: Session):
        try:
            return db.query(UserModel).filter(UserModel.id == id).first()
        except Exception as e:
            return e

    def register_user(self, register_data: Register, db: Session) -> UserSchema:
        try:
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
            role_model = db.query(RoleModel).filter(RoleModel.id == new_user.role_id).first()
            return UserSchema(
                id=new_user.id,
                username=new_user.username,
                email=new_user.email,
                address=new_user.address,
                role=role_model.role_name
            )
        except Exception as e:
            return e

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
