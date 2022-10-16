from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator
from ...user_accounts.models import User

User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)


class SiteEditResponse(BaseModel):
    url: str


class SiteIn(BaseModel):
    url: str