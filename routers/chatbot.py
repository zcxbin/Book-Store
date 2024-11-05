from fastapi import APIRouter, Depends

from configs.database import get_db
from services.book_service import get_book_service
from services.chatbot import gpt_response

router = APIRouter()


@router.post("/chatbot/")
async def chatbot_response(message: str, db=Depends(get_db), book_service=Depends(get_book_service)):
    return gpt_response(message, db, book_service)
