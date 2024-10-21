from datetime import datetime

from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from configs.database import Base


class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_public = Column(Integer, default=True)

    owner = relationship("User", back_populates="chat_rooms")
    messages = relationship("Message", back_populates="chat_room")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    message_type = Column(String, default="text")

    user = relationship("User", back_populates="messages")
    chat_room = relationship("ChatRoom", back_populates="messages")