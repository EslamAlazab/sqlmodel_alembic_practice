from typing import Annotated
from sqlmodel import Session, create_engine
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import StaticPool
import os


sqlite_file_name = "db.sqlite"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {
    "check_same_thread": False}

engine = create_engine(
    sqlite_url,
    connect_args=connect_args,
    poolclass=StaticPool  # Prevents SQLAlchemy from using connection pooling
)

# POSTGRES_USER = os.getenv('POSTGRES_USER')
# POSTGRES_DB = os.getenv('POSTGRES_DB')
# POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
# POSTGRES_HOST = os.getenv('DB_HOST', 'studybud_postgres')
# POSTGRES_PORT = os.getenv('DB_PORT', '5432')

# syncDATABASE_URL = f'postgresql://{POSTGRES_USER}:{
#     POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

# engine = create_engine(syncDATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

DATABASE_URL = f"sqlite+aiosqlite:///{sqlite_file_name}"
async_engine = create_async_engine(DATABASE_URL)

# asyncDATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{
#     POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
# async_engine = create_async_engine(asyncDATABASE_URL, echo=True)


async def get_async_session():
    async with AsyncSession(async_engine) as session:
        yield session

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]
