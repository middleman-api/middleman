from .user_accounts.models import User
from fastapi import FastAPI, Request, Response, Depends, HTTPException, responses, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, base

JWT_SECRET = 'myjwtsecret'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False 
    if not user.verify_password(password):
        return False
    return user 

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid username or password'
        )

    return user