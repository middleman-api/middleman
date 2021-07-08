from typing import Dict, Optional, List
from fastapi import FastAPI, Request, Response, Depends, HTTPException, responses, status, WebSocket, WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, base

from tortoise.contrib.fastapi import register_tortoise

from .api_v1.routers import open_api, internal

app = FastAPI()

app.include_router(internal.router)
app.include_router(open_api.router)

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

TORTOISE_ORM = {
    'connections': {
        # Dict format for connection
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': '127.0.0.1',
                'port': '5432',
                'user': 'middleman',
                'password': 'middlemanpassword',
                'database': 'middleman',
            }
        },
        # Using a DB_URL string
        'default': 'postgres://middleman:middlemanpassword@127.0.0.1:5432/middleman'
    },
    'apps': {
        'models': {
            'models': ['middleman.user_accounts.models', 'middleman.sites.models', 'aerich.models'],
            # If no default_connection specified, defaults to 'default'
            'default_connection': 'default',
        }
    }
}

register_tortoise(
    app, 
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True
)