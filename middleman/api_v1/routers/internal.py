from typing import Optional
import json
from fastapi import Depends
from passlib.hash import bcrypt
from fastapi import (
    FastAPI,
    Request,
    Response,
    Depends,
    HTTPException,
    responses,
    status,
    WebSocket,
    WebSocketDisconnect
)
from ...auth import get_current_user
from ...sites.models import ApiHit, Site
from ...user_accounts.models import User
from fastapi import APIRouter, Depends, HTTPException, status
from ..schemas.schema import User_Pydantic, UserIn_Pydantic, SiteIn
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from ...auth import authenticate_user, JWT_SECRET
import jwt


router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    # dependencies=[Depends(get_current_user)],
)


@router.get('/users/sites/{site_id}/')
async def get_api_hits(
        site_id: int,
        user: User_Pydantic=Depends(get_current_user)):
    api_hits = await ApiHit.filter(site_id=site_id)
    api_hits_data_list = []
    for api_hit in api_hits:
        request_data = api_hit.request_data
        response_data = api_hit.response_data
        request_data = json.loads(request_data)
        if response_data:
            response_data = json.loads(response_data)
        api_hits_data_list.append(
            {
                'request': request_data,
                'response': response_data
            }
        )
    return api_hits_data_list


@router.get('/users/sites/')
async def get_sites(user: User_Pydantic = Depends(get_current_user)):
    sites = await Site.filter(owner_id=user.id)
    sites_list = []
    for site in sites:
        site_data = {
            'id': site.id,
            'url': site.url
        }
        sites_list.append(site_data)
    return sites_list


@router.post('/users/sites/{site_id}/')
async def edit_site(site_id: int, site_data: Optional[SiteIn] = None, user: User_Pydantic = Depends(get_current_user)):
    if site_data:
        site = await Site.get(id=site_id)
        site.url = site_data.url
        await site.save()
    return site.url


@router.post('/users', response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)


@router.get('/users/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    return user


@router.put('/users/site/create')
async def create_site(site: SiteIn, user: User_Pydantic = Depends(get_current_user)):
    site = Site(url=site.url, owner_id=user.id)
    await site.save()
    return site.id


@router.post('/token')
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    user_obj = await User_Pydantic.from_tortoise_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return {'access_token' : token, 'token_type' : 'bearer'}


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Responses</title>
    </head>
    <body>
        <h1>Api hits</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <ul id='messages'>
        </ul>
        <script>
            var site_id = 1
            document.querySelector("#ws-id").textContent = site_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${site_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, site_id: int):
        await websocket.accept()
        if not self.active_connections.get(site_id, []):
            self.active_connections[site_id] = [websocket]
        else:
            print(self.active_connections)
            self.active_connections[site_id].append(websocket)
        print(self.active_connections)

    def disconnect(self, websocket: WebSocket, site_id: int):
        print(self.active_connections)
        self.active_connections.get(site_id, []).remove(websocket)

    async def send_events(self, message: str, site_id: int):
        print(self.active_connections)
        print(self.active_connections.get(site_id, []))
        for socket in self.active_connections.get(site_id, []):
            await socket.send_text(message)


manager = ConnectionManager()


@router.get("/page")
async def get():
    return HTMLResponse(html)


@router.websocket("/ws/{site_id}")
async def websocket_endpoint(websocket: WebSocket, site_id: int):
    print(site_id)
    await manager.connect(websocket, site_id)
    try:
        while True:
            data = await websocket.receive_text()
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client #{site_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, site_id)
        # await manager.broadcast(f"Client #{site_id} left the chat")
