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
    return created_user
