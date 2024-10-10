from pydantic import BaseModel


class OrderItem(BaseModel):
    book_id: int
    quantity: int

    class Config:
        from_attributes: True




