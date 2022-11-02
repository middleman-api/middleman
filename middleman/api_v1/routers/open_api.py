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
    client_host = request.client.host
    site = await Site.get(incoming_url=client_host)
    user_id = site.owner_id
    body = await request.body()
    headers = dict(request.headers)
    print(headers)
    request_data = {}
    request_data['headers'] = headers
    request_data['request_body'] = body.decode('utf-8')
    await manager.send_events(json.dumps(request_data), site.pk)
    api_hit = ApiHit(
        site=site,
        method=request.method,
        request_data=json.dumps(request_data),
        request_headers=headers
    )
    base_url = site.url
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
    response_headers = dict(response.headers)
    if response_headers.get('Content-Encoding', '') == 'gzip':
        text_data = gzip.decompress(raw_content).decode('utf-8')
    else:
        text_data = raw_content

    response_data = {}
    response_data['headers'] = response_headers
    print(response_headers)
    try:
        response_data['request_body'] = json.loads(text_data)
    except Exception:
        response_data['request_body'] = text_data

    await manager.send_events(text_data, site.pk)
    api_hit.response_data = response_data
    api_hit.response_headers = response_headers
    await api_hit.save()
    print('--------------------------------------------')
    return Response(
            raw_content,
            headers=response.headers,
            status_code=response.status_code
        )
