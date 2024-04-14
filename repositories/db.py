from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from controllers.schemas.auth import UserRoleSchema, UserSchema, CreateUserSchema
from repositories.interfaces import DBRepositoryInterface
from repositories.sql.models import UserRole, User
from usecases.errors import NotFoundError


class SQLDBRepository(DBRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self._session = session

    # def _parse_user_role(self, role: UserRole) -> UserRoleSchema:
    #     return UserRoleSchema(
    #         id=report.id,
    #         status=ReportStatusSchema(id=report.status.id,
    #                                   name=report.status.name,
    #                                   display_name=report.status.display_name),
    #         user_id=report.user_id,
    #         type=ReportTypeSchema(id=report.type.id,
    #                               group=report.type.group,
    #                               name=report.type.name,
    #                               display_name=report.type.display_name,
    #                               description=report.type.description,
    #                               confluence_url=report.type.confluence_url),
    #         params=self._get_params(report_params=report.params),
    #         gsheet_url=report.gsheet_url,
    #         file=report.file,
    #         created_at=report.created_at,
    #     )
    async def get_user_by_username(self, username: str) -> UserSchema:
        query = select(User).where(User.username == username)
        user_result = await self._session.execute(query)
        user_row = user_result.scalar_one_or_none()

        if not user_row:
            raise NotFoundError("User not found")

        return UserSchema(
            id=user_row.id,
            username=user_row.username,
            hashed_password=user_row.hashed_password,
            role=UserRoleSchema(id=user_row.role.id, name=user_row.role.name)
        )

    async def get_roles(self) -> list[UserRoleSchema]:
        query = select(UserRole)
        roles = (await self._session.scalars(query)).unique()
        if not roles:
            raise NotFoundError(f"Roles not found")
        return [UserRoleSchema(**vars(role)) for role in roles]

    async def create_user(self, user: CreateUserSchema, hashed_password: str) -> UserSchema:
        new_user = User(
            username=user.username,
            hashed_password=hashed_password,
            role_id=user.role_id
        )

        async with self._session.begin():
            self._session.add(new_user)
            await self._session.commit()
            await self._session.refresh(new_user)

        return UserSchema(
            id=new_user.id,
            username=new_user.username,
            hashed_password=new_user.hashed_password,
            role=UserRoleSchema(id=new_user.role.id, name=new_user.role.name)
        )
