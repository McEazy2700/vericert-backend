from decouple import config
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import URL


username = str(config("PGUSER"))
password = str(config("PGPASSWORD"))
host = str(config("PGHOST"))
port = int(config("PGPORT"))
database = str(config("PGDATABASE"))

url = URL.create(
    "postgresql+asyncpg",
    username=username,
    password=password,
    host=host,
    port=port,
    database=database,
)

engine = create_async_engine(url)
async_db_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
