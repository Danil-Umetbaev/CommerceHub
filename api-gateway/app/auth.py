import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, ValidationError
from typing import Annotated
from app.config import settings


class CurrentUser(BaseModel):
    id: str
    email: EmailStr


def decode_access_token(
    token: str,
):
    print("=== JWT TOKEN RECEIVED ===")
    print(token)
    try:
        payload = jwt.decode(
            jwt=token,
            key=settings.jwt_secret.get_secret_value(),
            algorithms=[settings.jwt_algorithm]
        )

        return payload

    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )

def get_token(request: Request):
    print("=== REQUEST COOKIES ===")
    print(request.cookies)
    access_token = request.cookies.get('access_token')
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не авторизован')
    return access_token

def get_current_user_id(token: str = Depends(get_token)):
    data = decode_access_token(token)
    return data['user_id']


userIdDep = Annotated[str, Depends(get_current_user_id)]