from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class MessageCreate(BaseModel):
    content: str
    room_id: int
    message_type: str = "text"


class Message(BaseModel):
    id: int
    content: str
    created_at: datetime
    room_id: int
    user_id: int
    message_type: str

    class Config:
        orm_mode = True


class ChatRoomCreate(BaseModel):
    name: str
    is_public: bool = True


class ChatRoom(BaseModel):
    id: int
    name: str
    owner_id: int
    is_public: bool
    messages: List[Message] = []

    class Config:
        orm_mode = True
