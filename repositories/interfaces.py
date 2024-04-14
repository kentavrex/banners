from abc import ABC, abstractmethod

from controllers.schemas.auth import UserRoleSchema


class DBRepositoryInterface(ABC):
    @abstractmethod
    async def get_roles(self) -> list[UserRoleSchema]:
        ...


class Cache(ABC):

    @abstractmethod
    def get_cached_or_call(self, *args, **kwargs):
        pass
