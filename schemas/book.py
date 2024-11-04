from typing import List

from pydantic import BaseModel


class Book(BaseModel):
    id: int
    title: str
    price: int
    discount: int
    description: str
    image_url: str
    quantity: int

    class Config:
        from_attributes = True


class BookResponse(BaseModel):
    books: List[Book]
    length: int
