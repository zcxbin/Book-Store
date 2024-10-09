from fastapi import APIRouter, Depends

from configs.authentication import get_current_user
from configs.database import get_db
from schemas.review import ReviewCreate
from services.review_service import get_review_service

router = APIRouter()


@router.post('/create_review')
async def create_review(
        book_id: int,
        review_data: ReviewCreate,
        user=Depends(get_current_user),
        db=Depends(get_db),
        review_service=Depends(get_review_service)
):
    try:
        return review_service.create_review(review_data, db, user.id, book_id)
    except Exception as e:
        print(e)
