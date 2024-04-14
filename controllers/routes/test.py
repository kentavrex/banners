from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from controllers.auth import get_current_active_user
from controllers.schemas.auth import UserSchema

router = APIRouter()


class OutputTestSchema(BaseModel):
    message: str = "Hello World!"


@router.get("/test")
async def test(current_user: Annotated[UserSchema, Depends(get_current_active_user)]):
    return OutputTestSchema()
