from typing import Optional
from fastapi import FastAPI, Request, Response, Depends, HTTPException, responses, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, base

from tortoise.contrib.fastapi import register_tortoise

from .api_v1.routers import open_api, internal

app = FastAPI()

app.include_router(internal.router)
app.include_router(open_api.router)

register_tortoise(
    app, 
    db_url='postgres://middleman:middlemanpassword@127.0.0.1:5432/middleman',
    modules={'models': ['middleman.user_accounts.models', 'middleman.sites.models']},
    generate_schemas=True,
    add_exception_handlers=True
)