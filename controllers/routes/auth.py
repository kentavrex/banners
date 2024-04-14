from fastapi import APIRouter
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from controllers.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_active_user
from controllers.dependencies import get_sql_db_repository
from controllers.schemas.auth import Token, CreateUserSchema, UserSchema
from repositories.db import SQLDBRepository
from usecases.auth import AuthUseCase


router = APIRouter()


@router.post("/reg_in")
async def reg_in_for_access_token(input_user: CreateUserSchema,
                                  db_repository: SQLDBRepository = Depends(get_sql_db_repository)) -> UserSchema:
    uc = AuthUseCase(db_repository=db_repository)
    user_exists = uc.check_user_exists(username=input_user.username)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User exists!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    created_user = await uc.create_user(user=CreateUserSchema(username=input_user.username,
                                                              password=input_user.password,
                                                              role_id=input_user.role_id))
    return created_user


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db_repository: SQLDBRepository = Depends(get_sql_db_repository)) -> Token:
    uc = AuthUseCase(db_repository=db_repository)
    user_exists = uc.check_user_exists(username=form_data.username)
    if not user_exists:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/me/", response_model=UserSchema)
async def read_users_me(
        current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    return current_user


@router.get("/users/roles/")
async def get_user_roles(db_repository: SQLDBRepository = Depends(get_sql_db_repository)):
    uc = AuthUseCase(db_repository=db_repository)
    roles = await uc.get_roles()
    return roles
