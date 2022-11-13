# -*- coding: utf-8 -*-

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tortoise.contrib.fastapi import register_tortoise

from middleman.api_v1.routers import open_api, internal

app = FastAPI()

app.include_router(internal.router)
app.include_router(open_api.router)

from fastapi import FastAPI

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
