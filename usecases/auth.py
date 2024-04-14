from controllers.auth import get_password_hash
from controllers.schemas.auth import UserRoleSchema, CreateUserSchema, UserSchema
from repositories.db import SQLDBRepository
from usecases.errors import NotFoundError


class AuthUseCase:
    def __init__(self, db_repository: SQLDBRepository):
        self._db_repository = db_repository

    async def check_user_exists(self, username: str) -> bool:
        try:
            await self._db_repository.get_user_by_username(username=username)
        except NotFoundError:
            return False
        return True

    async def get_user_by_username(self, username: str) -> UserSchema | None:
        try:
            user = await self._db_repository.get_user_by_username(username=username)
        except NotFoundError:
            return None
        return user

    async def get_roles(self) -> list[UserRoleSchema]:
        return await self._db_repository.get_roles()

    async def create_user(self, user: CreateUserSchema) -> UserSchema:
        return await self._db_repository.create_user(user=user, hashed_password=get_password_hash(user.password))

