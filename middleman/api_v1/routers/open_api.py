from typing import Optional
import gzip
import requests
import json
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from fastapi import FastAPI, Request, Response
from typing import Optional
import json
from fastapi import APIRouter
from passlib.hash import bcrypt

from ...sites.models import ApiHit, Site

router = APIRouter()

@router.get("{rest_of_path:path}")
@router.post("{rest_of_path:path}")
async def root(request: Request, rest_of_path: str):
    site = await Site.get(id=1)
    body = await request.body()
    headers = dict(request.headers)
    request_data = {}
    request_data['headers'] = headers
    request_data['request_body'] = body.decode('utf-8')

    api_hit = ApiHit(
        site=site,
        method=request.method,
        request_data=json.dumps(request_data)
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
