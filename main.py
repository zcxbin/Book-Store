from http.client import HTTPException

import redis.asyncio as redis
from fastapi import Depends, FastAPI, WebSocket

from configs import authentication
from routers.authentication import router as authentication_router
from routers.book import router as book_router
from routers.chatbot import router as chatbot_router
from routers.get_messages import router as get_messages_router
from routers.order import router as order_router
from routers.permission import router as permission_router
from routers.review import router as review_router
from routers.role_permission import router as role_permission_router
from routers.websocket_handlers import time_room, connected_users
from websocket_rooms import Room

redis_client = redis.Redis(host = 'localhost', port = 6379, db = 0)
app = FastAPI()

app.include_router(authentication_router, prefix = "/auth", tags = ["Authentication"])
app.include_router(book_router, prefix = "/book", tags = ["Books"])
app.include_router(review_router, prefix = "/review", tags = ["Reviews"])

app.include_router(order_router, prefix = "/order", tags = ["Orders"])
app.include_router(permission_router, prefix = "/permission", tags = ["Permissions"])
app.include_router(role_permission_router, prefix = "/role_permission", tags = ["RolePermissions"])
app.include_router(chatbot_router, prefix = "/chatbot", tags = ["AI"])
app.include_router(get_messages_router, prefix = "/get_messages", tags = ["Messages"])


@app.websocket("/current_time")
async def connect_websocket(websocket: WebSocket, room: Room = Depends(time_room)):
    await websocket.accept()

    try:
        token = await websocket.receive_text()
        username = await authentication.get_username_from_token(token.replace("Bearer ", ""))
        connected_users[websocket.client.host] = username
    except HTTPException:
        await websocket.close(code = 1008)
        return

    await room.connect(websocket)
