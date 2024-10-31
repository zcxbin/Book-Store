from datetime import datetime
from http.client import HTTPException

from configs.authentication import get_current_user
from routers.authentication import router as authentication_router
from routers.book import router as book_router
from routers.review import router as review_router
from routers.order import router as order_router
from routers.permission import router as permission_router
from routers.role_permission import router as role_permission_router

from websocket_rooms import Room
from fastapi import Depends, FastAPI, WebSocket
from typing import Any, NoReturn
from fastapi.responses import HTMLResponse
from configs import authentication

messages_cache = []
connected_users = {}
app = FastAPI()

app.include_router(authentication_router, prefix = "/auth", tags = ["Authentication"])
app.include_router(book_router, prefix = "/book", tags = ["Books"])
app.include_router(review_router, prefix = "/review", tags = ["Reviews"])

app.include_router(order_router, prefix = "/order", tags = ["Orders"])
app.include_router(permission_router, prefix = "/permission", tags = ["Permissions"])
app.include_router(role_permission_router, prefix = "/role_permission", tags = ["RolePermissions"])

time_room = Room()


@time_room.on_receive("text")
async def on_receive(room: Room, websocket: WebSocket, message: Any) -> None:
    username = connected_users.get(websocket.client.host)
    try:
        print("{}:{} just sent '{}'".format(username, websocket.client.port, message))
        messages_cache.append({
            "user_name": username,
            "message": message,
            "time": datetime.now()
            }
            )
        if len(messages_cache) > 100:
            messages_cache.pop(0)
        await room.push_text(f"{username}: {message}")
    except Exception as ex:
        print("Exception: " + str(ex))
        pass


@time_room.on_connect("after")
async def on_chatroom_connection(room: Room, websocket: WebSocket) -> None:
    username = connected_users.get(websocket.client.host)
    try:
        print("{}:{} joined the channel".format(websocket.client.host, websocket.client.port))
        await room.push_text("{} joined the channel".format(username))
    except Exception as ex:
        print("Exception: " + str(ex))
        pass


@time_room.on_disconnect("after")
async def on_chatroom_disconnect(room: Room, websocket: WebSocket) -> None:
    username = connected_users.pop(websocket.client.host, None)
    try:
        print("{}:{} left the channel".format(websocket.client.host, websocket.client.port))
        await room.push_text("{} left the channel".format(username))
    except Exception as ex:
        print("Exception: " + str(ex))
        pass


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


@app.get("/get_messages")
async def get_messages():
    return messages_cache
