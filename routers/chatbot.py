from fastapi import APIRouter, Depends

from configs.authentication import get_current_user
from configs.database import get_db
from services.book_service import get_book_service
from services.chatbot_service import get_chatbot_service

router = APIRouter()


@router.post("/chatbot/")
async def chatbot_response(
        message: str,
        db=Depends(get_db),
        book_service=Depends(get_book_service),
        chatbot_service=Depends(get_chatbot_service),
        user_service=Depends(get_current_user)
):
    try:
        return chatbot_service.gpt_response(message, db, book_service)
    except Exception as e:
        print(e)