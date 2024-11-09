from fastapi import APIRouter, Depends

from configs.authentication import get_current_user
from configs.database import get_db
from schemas.review import ReviewCreate, ReviewResponse, ReviewUpdate
from services.review_service import get_review_service

router = APIRouter()


@router.get('/get_reviews_by_books', response_model = ReviewResponse)
async def get_reviews_by_books(
        book_id: int,
        db = Depends(get_db),
        review_service = Depends(get_review_service)
        ):
    try:
        reviews = review_service.get_reviews_by_books_id(db, book_id)
        return ReviewResponse(
            data = reviews,
            length = len(reviews)
            )
    except Exception as e:
        print(e)


@router.post('/create_review')
async def create_review(
        review_data: ReviewCreate,
        user = Depends(get_current_user),
        db = Depends(get_db),
        review_service = Depends(get_review_service)
        ):
    try:
        return review_service.create_review(review_data, db, user.id)
    except Exception as e:
        print(e)


@router.put('/update_review')
async def update_review(
        book_id: int,
        review_update: ReviewUpdate,
        db = Depends(get_db),
        review_service = Depends(get_review_service),
        user = Depends(get_current_user)
        ):
    try:
        return review_service.update_review(db, review_update, user.id, book_id)
    except Exception as e:
        print(e)


@router.delete('/delete_review')
async def delete_review(
        id: int,
        db = Depends(get_db),
        review_service = Depends(get_review_service),
        user = Depends(get_current_user)
        ):
    try:
        return review_service.delete_review(db, user.id, id)
    except Exception as e:
        print(e)
