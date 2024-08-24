import os
from database.model import Movies, engine, async_session
from sqlalchemy import insert, select, delete


# functions for working with database

async def insert_movie(id_user: str, movie: str, genre: str) -> None:
    statement = insert(Movies).values(id_user=id_user, movie=movie, genre=genre)
    async with engine.connect() as connection:
        await connection.execute(statement)
        await connection.commit()


async def list_movie(id_user: str) -> None:
    statement = select(Movies).where(Movies.id_user == id_user)
    async with engine.connect() as connection:
        result = await connection.execute(statement)
    return result.all()


async def delete_movie(movie: str, id_user: str) -> None:
    statement = delete(Movies).where(Movies.movie == movie).where(Movies.id_user == id_user)
    async with engine.connect() as connection:
        await connection.execute(statement)
        await connection.commit()
