import logging
from uuid import uuid4

from asyncpg import Connection
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from config import settings

logger = logging.getLogger(__name__)


class CConection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f"__asyncpg_{prefix}_{uuid4()}__"


engine = create_async_engine(settings.PG_URL,
                             echo=True,
                             connect_args={
                                 "statement_cache_size": 0,
                                 "prepared_statement_cache_size": 0,
                                 "connection_class": CConection,
                             },
                             )
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)
Base = declarative_base()
