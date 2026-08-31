from typing import Annotated

from fastapi import Depends, Request, HTTPException, status
from app.services import UserService
from app.database import DBDep
def get_token(request: Request):

    access_token = request.cookies.get('access_token')
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Не авторизован')
    return access_token

def get_current_user_id(token: str = Depends(get_token),):
    data = UserService().decode_jwt(token)
    return data['user_id']


userIdDep = Annotated[str, Depends(get_current_user_id)]