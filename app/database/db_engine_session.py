from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DOCKER_VOLUME_DATABASE_URL = "postgresql+asyncpg://postgres:root@db:5432/py-fast-todo"
NON_PROD_DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost:5432/py-fast-todo"
PROD_DATABASE_URL = "postgresql+asyncpg://postgres:root@192.168.1.72:5432/py-fast-todo"

engine = create_async_engine(DOCKER_VOLUME_DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False) # type: ignore