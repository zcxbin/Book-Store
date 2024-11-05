import json
from datetime import datetime
from http.client import HTTPException
from typing import Any

import redis.asyncio as redis
from fastapi import WebSocket

from websocket_rooms import Room

time_room = Room()

cache_key_messages = "cache_messages"

connected_users = {}

redis_client = redis.Redis(host='localhost', port=6379, db=0)


@time_room.on_receive("text")
async def on_receive(room: Room, websocket: WebSocket, message: Any) -> None:
    username = connected_users.get(websocket.client.host)
    try:
        print("{}:{} just sent '{}'".format(username, websocket.client.port, message))
        value = await redis_client.get(cache_key_messages)
        if not value:
            messages = []
            messages.append(
                {
                    "user_name": username,
                    "message": message,
                    "time": datetime.now()
                }
            )
            await redis_client.set(cache_key_messages, json.dumps(messages))

        elif value:
            value = await redis_client.get(cache_key_messages)
            value = json.loads(value)
            value.append(
                {
                    "user_name": username,
                    "message": message,
                    "time": datetime.now()
                }
            )
            if len(value) > 100:
                value.pop(0)
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
