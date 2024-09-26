from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import Update

from configs.authentication import get_current_user
from configs.database import get_db
from schemas.authentication import Register, UpdateUser
from services.authentication_service import get_authen_service

router = APIRouter()


@router.post('/login')
def login(login_data: OAuth2PasswordRequestForm = Depends(), authentication_service=Depends(get_authen_service)
          , db=Depends(get_db)):
    try:
        response = authentication_service.authenticate_user(login_data, db)
        if response is None:
            return None
        return response
    except Exception as e:
        return e
