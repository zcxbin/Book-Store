from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import Update

from configs.authentication import get_current_user
from configs.database import get_db
from schemas.authentication import Register, UpdateUser
from services.authentication_service import get_authentication_service
from schemas.user import User as UserSchema
router = APIRouter()


@router.post('/login')
def login(login_data: OAuth2PasswordRequestForm = Depends(), authentication_service=Depends(get_authentication_service)
          , db=Depends(get_db)):
    try:
        response = authentication_service.authenticate_user(login_data, db)
        if response is None:
            return None
        return response
    except Exception as e:
        return e


@router.post('/register', response_model=UserSchema)
def register(register_data: Register, authentication_service=Depends(get_authentication_service), db=Depends(get_db)):
    try:
        return authentication_service.register_user(register_data, db)
    except Exception as e:
        return e


@router.put('/update')
def update_user(update_data: UpdateUser, db=Depends(get_db), authentication_service=Depends(get_authentication_service), user=Depends(get_current_user)):
    try:
        return authentication_service.update_user(update_data, db, user.id)
    except Exception as e:
        print(e)
