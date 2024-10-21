from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List

from ..schemas.chat import ChatRoomCreate, MessageCreate, ChatRoom, Message
from ..models import chat, user
from services. import ChatService
from ..dependencies import get_db, get_current_user

router = APIRouter()