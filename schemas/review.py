from pydantic import BaseModel


class ReviewCreate(BaseModel):
    rating: int
    comment: str

    class Config:
        from_attributes = True
