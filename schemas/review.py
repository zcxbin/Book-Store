from datetime import datetime
from typing import List

from pydantic import BaseModel


class ReviewCreate(BaseModel):
    rating: int
    comment: str

    class Config:
        from_attributes = True


class Review(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: int
    comment: str
    created_at: datetime

    class Config:
        from_attributes = True


class ReviewUpdate(BaseModel):
    rating: int
    comment: str

    class Config:
        from_attributes = True


class ReviewUpdateResponse(BaseModel):
    rating: int
    comment: str
    created_at: str

    class Config:
        from_attributes = True


class ReviewResponse(BaseModel):
    data: List[Review] = []
    length: int = 0
