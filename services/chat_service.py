from sqlalchemy.orm import Session
from schemas.chat import ChatRoomCreate, MessageCreate
from models import chat, user
class ChatService:
    def create_chat_room(self, room: ChatRoomCreate, db: Session, cu)