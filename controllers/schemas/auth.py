from pydantic import BaseModel


class UserRoleSchema(BaseModel):
    id: int
    name: str


class CreateUserSchema(BaseModel):
    username: str
    password: str
    role_id: int = 1


class UserSchema(BaseModel):
    id: int
    username: str
    hashed_password: str
    role: UserRoleSchema


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

