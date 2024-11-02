import json
from datetime import datetime
from http.client import HTTPException

import redis.asyncio as redis

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

cache_key_messages = "cache_messages"
redis_client = redis.Redis(host = 'localhost', port = 6379, db = 0)
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
        value = await redis_client.get(cache_key_messages)
        if not value:
            messages = {
                "messages": []
                }
            messages["messages"].append({
                "user_name": username,
                "message": message,
                "time": datetime.now()
                }
                )
            await redis_client.set(cache_key_messages, json.dumps(messages))

        elif value:
            value = await redis_client.get(cache_key_messages)
            value = json.loads(value)
            value["messages"].append({
                "user_name": username,
                "message": message,
                "time": datetime.now()
                }
                )
            if len(value["messages"]) > 100:
                value["messages"].pop(0)
            await redis_client.set(cache_key_messages, json.dumps(value))

        await room.push_text(f"{username}: {message}")

    except Exception as ex:
        raise HTTPException(ex)
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


@app.get("/get_messages/")
async def get_data():
    """Lấy dữ liệu từ Redis"""
    try:
        value = await redis_client.get(cache_key_messages)
        if value:
            value = json.loads(value)
            return value["messages"]
        else:
            return {"message": "Không tìm thấy dữ liệu"}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
