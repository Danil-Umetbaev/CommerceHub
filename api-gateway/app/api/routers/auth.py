from fastapi import APIRouter, Response
from app.api_client import request_service
from app.config import settings
from app.auth import userIdDep


from app.schemas.auth import CurrentUser, UserRegisterRequestSchema, UserLoginSchema
router = APIRouter(prefix='/auth')

@router.post('/register')
async def register(user: UserRegisterRequestSchema):
    data = user.model_dump(mode='json')
    return await request_service("POST", url=f"{settings.AUTH_SERVICE_URL}/auth/register", json_data=data)

@router.post('/login')
async def login(user: UserLoginSchema, response: Response):
    data = user.model_dump(mode='json')
    return await request_service("POST", url=f"{settings.AUTH_SERVICE_URL}/auth/login", json_data=data, fastapi_response=response)

@router.get("/me")
async def get_me(current_user: userIdDep):
    return current_user
