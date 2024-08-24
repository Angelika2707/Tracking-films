import asyncio
import logging
import sys

from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import Message
from config import TOKEN

from database.requests import insert_movie, list_movie, delete_movie
from database.model import create_database

dp = Dispatcher()


class Form(StatesGroup):
    name = State()
    genre = State()


class DeleteForm(StatesGroup):
    name = State()


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Hello, i am a bot for tracking unwatched movies\nCommands:\n/add - add movie\n/delete - delete movie\n/list "
        "- list movies")


@dp.message(Command("list"))
async def command_list_movie_handler(message: Message) -> None:
    movies = await list_movie(str(message.from_user.id))
    result = "Your movies:\n"
    for movie in sorted(movies, key=lambda movie: movie[2]):
        result += movie[2].capitalize() + " - " + movie[3].title() + "\n"
    await message.answer(result)


@dp.message(Command("delete"))
async def command_delete_get_movie_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Write movie name")
    await state.set_state(DeleteForm.name)


@dp.message(DeleteForm.name)
async def command_delete_movie_handler(message: Message) -> None:
    await delete_movie(message.text.lower(), str(message.from_user.id))
    await message.answer("Movie deleted!")


@dp.message(Command("add"))
async def command_insert_movie_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Write movie name")
    await state.set_state(Form.name)


@dp.message(Form.name)
async def command_insert_movie_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text.lower())
    await state.set_state(Form.genre)
    await message.answer("Write movie genre")


@dp.message(Form.genre)
async def command_insert_genre_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(genre=message.text.lower())
    information_film = await state.get_data()
    await insert_movie(str(message.from_user.id), information_film.get("name"), information_film.get("genre"))
    await message.answer("Movie inserted successfully")
    await state.clear()


@dp.message()
async def echo_handler(message: Message) -> None:
    await message.answer("Please write command")


async def main() -> None:
    await create_database()

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
