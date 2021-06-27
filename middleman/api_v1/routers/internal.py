from typing import Optional
import json
from fastapi import Depends
from passlib.hash import bcrypt

from ...auth import get_current_user
from ...sites.models import ApiHit, Site
from ...user_accounts.models import User
from fastapi import APIRouter
from ..schemas.schema import User_Pydantic, UserIn_Pydantic, SiteIn

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
    dependencies=[Depends(get_current_user)],
)

@router.get('/users/sites/{site_id}/')
async def get_api_hits(site_id: int, user: User_Pydantic = Depends(get_current_user)):
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