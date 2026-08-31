from fastapi import APIRouter, Response
from .schemas import TokenResponse, UserLoginSchema, UserReadSchemaWithPassword, UserRegisterRequestSchema
from .services import UserService
from .database import DBDep
from .dependencies import userIdDep
router = APIRouter(prefix='/auth')

@router.post("/register", response_model=TokenResponse)
async def register(
    user: UserRegisterRequestSchema,
    db: DBDep
):
    return await UserService(db).register_user(user)

@router.post("/login")
async def login(
    user: UserLoginSchema,
    response: Response,
    db: DBDep
):
    return await UserService(db).login_user(user, response)



@router.get("/me")
async def get_me(user_id: userIdDep):
    return {'data':user_id}


