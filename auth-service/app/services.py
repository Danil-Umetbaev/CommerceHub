from .repositories.repositories import  UserRepository
from .schemas import TokenResponse, UserLoginSchema, UserReadSchema, UserRegisterRequestSchema, UserRegisterSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings

import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Response, status
import bcrypt

class UserService:

    def __init__(self, db: AsyncSession | None = None):
        self.db = db

    async def login_user(self, user: UserLoginSchema, response: Response):
        user_in_db = await UserRepository(self.db).get_user_by_email_with_password(email=user.email)
        if not self.verify_password(user.password, user_in_db.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неправильный пароль!")
        access_token = self.create_access_token(user_in_db)
        response.set_cookie('access_token', access_token)
        return TokenResponse(access_token=access_token, user=user_in_db)



    def hash_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def create_access_token(self, user: UserReadSchema):
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes)

        payload = {
            "user_id": user.id,
            "email": user.email,
            "role": "user",
            "exp": expire
        }
        token = jwt.encode(
            payload,
            key=settings.jwt_secret.get_secret_value(),
            algorithm=settings.jwt_algorithm

        )
        return token

    async def register_user(self, user: UserRegisterRequestSchema):
        hash_password = self.hash_password(user.password)
        user_to_db = UserRegisterSchema(email=user.email, password_hash=hash_password)
        result_user = await UserRepository(self.db).add(user_to_db)
        await self.db.commit()
        access_token = self.create_access_token(result_user)
        return TokenResponse(access_token=access_token, user=result_user)


    def decode_jwt(self, token: str) -> dict:
        try:
            return jwt.decode(
                token, key=settings.jwt_secret.get_secret_value(), algorithms=[settings.jwt_algorithm]
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401,
                detail="Закончилось действие авторизации, зайдите снова",
            )
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Неверный токен")


