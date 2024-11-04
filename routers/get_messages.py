import json
from http.client import HTTPException

import redis.asyncio as redis
from fastapi import APIRouter

from routers.websocket_handlers import cache_key_messages

router = APIRouter()
redis_client = redis.Redis(host = 'localhost', port = 6379, db = 0)


@router.get("/get_messages/")
async def get_data():
    """Lấy dữ liệu từ Redis"""
    try:
        value = await redis_client.get(cache_key_messages)
        if value:
            value = json.loads(value)
            return value
        else:
            return {"message": "Không tìm thấy dữ liệu"}
    except Exception as e:
        raise HTTPException(500, str(e))
