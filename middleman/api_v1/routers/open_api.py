from typing import Optional
import gzip
import requests
import json
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Response, WebSocket, WebSocketDisconnect
from typing import Optional
import json
from fastapi import APIRouter
from passlib.hash import bcrypt

from ...sites.models import ApiHit, Site
from .internal import manager
router = APIRouter()

@router.get("{rest_of_path:path}")
@router.post("{rest_of_path:path}")
async def root(request: Request, rest_of_path: str):
    site = await Site.get(id=1)
    user_id = site.owner_id
    body = await request.body()
    headers = dict(request.headers)
    request_data = {}
    request_data['headers'] = headers
    request_data['request_body'] = body.decode('utf-8')
    await manager.send_events(json.dumps(request_data), user_id)
    api_hit = ApiHit(
        site=site,
        method=request.method,
        request_data=json.dumps(request_data)
    )
    base_url = site.url
    print(base_url + rest_of_path)
    await api_hit.save()
    headers['host'] = "entri.app"
    request_params = {
            "method": request.method,
            "url": base_url + rest_of_path,
            "headers": headers,
            "data": body,
            "params": request.query_params,
            "stream": True
    }
    response = requests.request(
        **request_params
    )
    raw_content = response.raw.read()
    text_data = gzip.decompress(raw_content)
    response_headers = dict(response.headers)
    response_data = {}
    response_data['headers'] = response_headers
    response_data['request_body'] = text_data.decode('utf-8')
    response_data = json.dumps(response_data)
    api_hit.response_data = response_data
    await api_hit.save()
    return Response(
            raw_content,
            headers=response.headers,
            status_code=response.status_code
        )


# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <h2>Your ID: <span id="ws-id"></span></h2>
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#             var client_id = 1
#             document.querySelector("#ws-id").textContent = client_id;
#             var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages')
#                 var message = document.createElement('li')
#                 var content = document.createTextNode(event.data)
#                 message.appendChild(content)
#                 messages.appendChild(message)
#             };
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """


# class ConnectionManager:
#     def __init__(self):
#         self.active_connections  = {}

#     async def connect(self, websocket: WebSocket, client_id: int):
#         await websocket.accept()
#         if not self.active_connections.get(client_id, []):
#             self.active_connections[client_id] = [websocket]
#         else:
#             self.active_connections[client_id].append(websocket)
    
#     def disconnect(self, websocket: WebSocket, client_id: int):
#         self.active_connections.get(client_id, []).remove(websocket)

#     async def send_events(self, message: str, client_id: int):
#         for sockets in self.active_connections.get(client_id, []):
#             for socket in sockets:
#                 await socket.send_text(message)


# manager = ConnectionManager()


# @router.get("/dashboard/page")
# async def get():
#     return HTMLResponse(html)


# @router.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket, client_id)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_personal_message(f"You wrote: {data}", websocket)
#             await manager.broadcast(f"Client #{client_id} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")
