from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from configs.database import get_db
from schemas.book import BookResponse
from services.book_service import get_book_service

router = APIRouter()


@router.get("/get_books", response_model=BookResponse)
async def get_books(db=Depends(get_db),
                    book_service=Depends(get_book_service)):
    try:
        books = book_service.get_all_books(db)
        return BookResponse(books=books,
                            length=len(books))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Book not found")


@router.get('/get_books_by_author_id', response_model=BookResponse)
async def get_books_by_author_id(
        author_id: str,
        db=Depends(get_db),
        book_service=Depends(get_book_service)):
    try:

        books = book_service.get_books_by_author_id(db, author_id)
        if not books:
            raise HTTPException(status_code=404, detail="Author not found")
        return BookResponse(
            books=books,
            length=len(books)
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while fetching books by author name.")


@router.get('/get_books_by_category_id', response_model=BookResponse)
async def get_books_by_category_id(
        category_id: str,
        db=Depends(get_db),
        book_service=Depends(get_book_service)):
    try:
        books = book_service.get_books_by_category_id(db, category_id)
        return BookResponse(
            books=books,
            length=len(books)
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while fetching books by category_id name.")
