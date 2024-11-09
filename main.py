from fastapi import Depends, FastAPI, WebSocket

from routers.authentication import router as authentication_router
from routers.book import router as book_router
from routers.chatbot import router as chatbot_router
from routers.order import router as order_router
from routers.permission import router as permission_router
from routers.review import router as review_router
from routers.role_permission import router as role_permission_router

from websocket_rooms import Room
from fastapi import Depends, FastAPI, WebSocket
from typing import Any, NoReturn
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from configs import authentication, database
from configs.database import engine

messages_cache = []
connected_users = {}

database.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(authentication_router, prefix = "/auth", tags = ["Authentication"])
app.include_router(book_router, prefix = "/book", tags = ["Books"])
app.include_router(review_router, prefix = "/review", tags = ["Reviews"])

app.include_router(order_router, prefix="/order", tags=["Orders"])
app.include_router(permission_router, prefix="/permission", tags=["Permissions"])
app.include_router(role_permission_router, prefix="/role_permission", tags=["RolePermissions"])
app.include_router(chatbot_router, prefix="/chatbot", tags=["AI"])


