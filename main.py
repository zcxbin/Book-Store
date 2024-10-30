from datetime import datetime

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

messages_cache = []

app = FastAPI()

app.include_router(authentication_router, prefix = "/auth", tags = ["Authentication"])
app.include_router(book_router, prefix = "/book", tags = ["Books"])
app.include_router(review_router, prefix = "/review", tags = ["Reviews"])

app.include_router(order_router, prefix = "/order", tags = ["Orders"])
app.include_router(permission_router, prefix = "/permission", tags = ["Permissions"])
app.include_router(role_permission_router, prefix = "/role_permission", tags = ["RolePermissions"])

# html = """"
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#         <style>
#             /* Đặt chiều cao cho khung chat và khung tin nhắn */
#             body {
#                 font-family: Arial, sans-serif;
#                 display: flex;
#                 flex-direction: column;
#                 align-items: center;
#                 justify-content: center;
#                 height: 100vh;
#                 margin: 0;
#             }
#             h1 {
#                 margin-bottom: 20px;
#             }
#             #chatContainer {
#                 display: flex;
#                 flex-direction: column;
#                 width: 100%;
#                 max-width: 600px;
#                 height: 80vh;
#                 border: 1px solid #ccc;
#                 border-radius: 8px;
#                 overflow: hidden;
#             }
#             #messages {
#                 flex-grow: 1;
#                 overflow-y: auto;
#                 padding: 10px;
#                 border-bottom: 1px solid #ccc;
#             }
#             #messages li {
#                 list-style-type: none;
#                 margin-bottom: 10px;
#             }
#             #inputContainer {
#                 display: flex;
#                 padding: 10px;
#             }
#             #messageText {
#                 flex-grow: 1;
#                 padding: 8px;
#                 font-size: 16px;
#                 border: 1px solid #ccc;
#                 border-radius: 4px;
#                 margin-right: 10px;
#             }
#             button {
#                 padding: 8px 16px;
#                 font-size: 16px;
#                 border: none;
#                 border-radius: 4px;
#                 background-color: #4CAF50;
#                 color: white;
#                 cursor: pointer;
#             }
#             button:hover {
#                 background-color: #45a049;
#             }
#         </style>
#     </head>
#     <body>
#         <h1>Time WebSocket</h1>
#         <div id="chatContainer">
#             <ul id="messages">
#             </ul>
#             <div id="inputContainer">
#                 <input type="text" id="messageText" autocomplete="off" placeholder="Nhập tin nhắn..."/>
#                 <button onclick="sendMessage(event)">Gửi</button>
#             </div>
#         </div>
#         <script>
#             var ws = new WebSocket("ws://localhost:8000/current_time");
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages');
#                 var message = document.createElement('li');
#                 var content = document.createTextNode(event.data);
#                 message.appendChild(content);
#                 messages.appendChild(message);
#                 messages.scrollTop = messages.scrollHeight; // Tự động cuộn xuống cuối khung tin nhắn
#             };
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText");
#                 if (input.value.trim() !== "") {
#                     ws.send(input.value);
#                     input.value = '';
#                 }
#                 event.preventDefault();
#             }
#         </script>
#     </body>
# </html>
# """
#
#
# @app.get("/")
# async def get():
#     return HTMLResponse(html)

#
# time_room = Room()
#
#
# @time_room.on_receive("text")
# async def on_receive(room: Room, websocket: WebSocket, message: Any, user = Depends(get_current_user)) -> None:
#     try:
#         print("{}:{} just sent '{}'".format(user.username, websocket.client.port, message))
#         messages_cache.append({
#             "user_name": user.username,
#             "message": message,
#             "time": datetime.now()
#             }
#             )
#         if len(messages_cache) > 100:
#             messages_cache.pop(0)
#         await room.push_text(f"{user.username}: {message}")
#     except Exception as ex:
#         print("Exception: " + str(ex))
#         pass
#
#
# @time_room.on_connect("after")
# async def on_chatroom_connection(room: Room, websocket: WebSocket, user = Depends(get_current_user)) -> None:
#     try:
#         print("{}:{} joined the channel".format(websocket.client.host, websocket.client.port))
#         await room.push_text("{} joined the channel".format(user.username))
#     except Exception as ex:
#         print("Exception: " + str(ex))
#         pass
#
#
# @time_room.on_disconnect("after")
# async def on_chatroom_disconnect(room: Room, websocket: WebSocket, user = Depends(get_current_user)) -> None:
#     try:
#         print("{}:{} left the channel".format(websocket.client.host, websocket.client.port))
#         await room.push_text("{} left the channel".format(user.username))
#     except Exception as ex:
#         print("Exception: " + str(ex))
#         pass
#
#
# @app.websocket("/current_time")
# async def connect_websocket(websocket: WebSocket, room: Room = Depends(time_room)):
#     await room.connect(websocket)
#
#
# @app.get("/get_messages")
# async def get_messages():
#     return messages_cache
