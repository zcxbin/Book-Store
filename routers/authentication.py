from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from configs.authentication import get_current_user
from configs.database import get_db
from schemas.authentication import Register, UpdateUser, LoginReq
from services.authentication_service import get_authentication_service

router = APIRouter()


@router.post('/swagger-login')
def login(login_data=Depends(OAuth2PasswordRequestForm), authentication_service=Depends(get_authentication_service)
          , db=Depends(get_db)):
    try:
        response = authentication_service.authenticate_user(login_data, db)
        return response
    except Exception as e:
        return e


@router.post('/login')
def login(login_data: LoginReq, authentication_service=Depends(get_authentication_service)
          , db=Depends(get_db)):
    try:
        response = authentication_service.login(login_data, db)
        return response
    except Exception as e:
        return e


@router.get("/get_user_by_id")
def get_user_by_id(
        id: int,
        authentication_service=Depends(get_authentication_service),
        db=Depends(get_db)
):
    try:
        return authentication_service.get_user_by_id(id, db)
    except Exception as e:
        return e


@router.post('/register')
def register(register_data: Register,
             authentication_service=Depends(get_authentication_service),
             db=Depends(get_db)):
    try:
        return authentication_service.register_user(register_data, db)
    except Exception as e:
        return e


@router.put('/update')
def update_user(update_data: UpdateUser, db=Depends(get_db),
                authentication_service=Depends(get_authentication_service),
                user=Depends(get_current_user)):
    try:
        return authentication_service.update_user(update_data, db, user.id)
    except Exception as e:
        print(e)


@router.delete('/delete')
def delete_user(db=Depends(get_db),
                authentication_service=Depends(get_authentication_service),
                user=Depends(get_current_user)):
    try:
        return authentication_service.delete_user(db, user.id)
    except Exception as e:
        print(e)
