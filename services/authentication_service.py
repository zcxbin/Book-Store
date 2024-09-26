from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import Update
from sqlalchemy.orm import Session
from models.user import User as UserModel
from schemas.authentication import Token, Register, UpdateUser
from configs.authentication import verify_password, get_password_hash, create_access_token

def get_authen_service():
    try:
        yield AuthenticationService()
    finally:
        pass


class AuthenticationService:
    def authenticate_user(self, login_data: OAuth2PasswordRequestForm, db: Session) -> Token:
        user = db.query(UserModel).filter(UserModel.username == login_data.username).first()
        if not user:
            return None
        if not verify_password(login_data.password, user.password):
            return None
        # print(user.username, user.role, user.id)

        access_token = create_access_token(data={
            'username': user.username,
            'role': user.role,
            'id': user.id
        })
        return Token(access_token=access_token)

