from fastapi import APIRouter, Depends

from configs.authentication import get_current_user
from configs.database import get_db
from schemas.review import ReviewCreate, ReviewResponse
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


@router.get('/get_reviews_by_books', response_model=ReviewResponse)
async def get_reviews_by_books(
        book_id: int,
        db=Depends(get_db),
        review_service=Depends(get_review_service)
):
    try:
        reviews = review_service.get_reviews_by_books_id(db, book_id)
        return ReviewResponse(
            data=reviews,
            length=len(reviews)
        )
    except Exception as e:
        print(e)
