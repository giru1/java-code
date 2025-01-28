from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import settings

if settings.MODE == "TEST":
    DATABASE_URL = (
        f"postgresql+asyncpg://{settings.TEST_DB_USER}:{settings.TEST_DB_PASS}@"
        f"{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    DATABASE_PARAMS = {"poolclass": NullPool}
else:
    DATABASE_URL = (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )
    DATABASE_PARAMS = {}


engine = create_async_engine(DATABASE_URL,
                             **DATABASE_PARAMS,
                            pool_size=20,  # Максимальное количество соединений
                            max_overflow=30,  # Дополнительные соединения при необходимости
                            pool_timeout=30,  # Таймаут ожидания соединения
                            pool_recycle=1800,  # Пересоздание соединений каждые 30 минут
                             )

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass
