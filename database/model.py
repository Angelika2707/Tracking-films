from os import getenv
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

# Creating tables needed for registration in the bot

# Create an asynchronous engine using the specified database URI(config.py)
engine = create_async_engine(getenv("SQL_ALCHEMY_DATABASE_URI"), echo=True)

# Create an asynchronous session factory
async_session = async_sessionmaker(engine)


# Base class for declarative models with asynchronous support
class Base(AsyncAttrs, DeclarativeBase):
    pass


# Model for movies
class Movies(Base):
    __tablename__ = "Movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    id_user: Mapped[str] = mapped_column(String(20))
    movie: Mapped[str] = mapped_column(String(20))
    genre: Mapped[str] = mapped_column(String(20))


async def create_database():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
