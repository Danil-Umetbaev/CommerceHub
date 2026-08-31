from pydantic import BaseModel, ConfigDict, EmailStr, Field



class CredentialBase(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=256)
    model_config = ConfigDict(from_attributes=True)


class UserRegisterRequestSchema(CredentialBase):
    pass

class UserRegisterSchema(BaseModel):
    email: EmailStr
    password_hash: str = Field(min_length=8, max_length=256)
    model_config = ConfigDict(from_attributes=True)

class UserLoginSchema(CredentialBase):
    pass

class UserReadSchema(BaseModel):
    id: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class UserReadSchemaWithPassword(UserReadSchema):
    password_hash: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserReadSchema
    model_config = ConfigDict(from_attributes=True)
