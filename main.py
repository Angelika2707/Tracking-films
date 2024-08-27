import asyncio
import logging
import sys

from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from os import getenv

from database.requests import insert_movie, list_movie, delete_movie
from database.model import create_database

dp = Dispatcher()


class Form(StatesGroup):
    name = State()
    genre = State()


class DeleteForm(StatesGroup):
    name = State()


genres = [
    [types.KeyboardButton(text="/cancel")],
    [types.KeyboardButton(text="Comedy")],
    [types.KeyboardButton(text="Action")],
    [types.KeyboardButton(text="Drama")],
    [types.KeyboardButton(text="Horror")],
    [types.KeyboardButton(text="Fantasy")],
    [types.KeyboardButton(text="Romance")],
    [types.KeyboardButton(text="Cartoon")]
]

commands = [
    [types.KeyboardButton(text="/start")],
    [types.KeyboardButton(text="/add")],
    [types.KeyboardButton(text="/delete")],
    [types.KeyboardButton(text="/list")],
    [types.KeyboardButton(text="/cancel")]
]

genres_keyboard = types.ReplyKeyboardMarkup(keyboard=genres)

commands_keyboard = types.ReplyKeyboardMarkup(keyboard=commands)


@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer(
        "Hello, i am a bot for tracking unwatched movies\nCommands:\n/add - add movie\n/delete - delete movie\n/list "
        "- list movies\n/cancel - cancel command", reply_markup=commands_keyboard)


@dp.message(Command("list"))
async def command_list_movie_handler(message: Message) -> None:
    movies = await list_movie(str(message.from_user.id))
    result = "Your movies:\n"
    for movie in sorted(movies, key=lambda movie: movie[2]):
        result += movie[2].capitalize() + " - " + movie[3].title() + "\n"
    await message.answer(result, reply_markup=commands_keyboard)


@dp.message(Command("delete"))
async def command_delete_get_movie_handler(message: Message, state: FSMContext) -> None:
    user_films = await list_movie(str(message.from_user.id))
    user_films = [[types.KeyboardButton(text=film[2].capitalize())] for film in
                  sorted(user_films, key=lambda movie: movie[2])]
    user_films.insert(0, [types.KeyboardButton(text="/cancel")])
    user_films_keyboard = types.ReplyKeyboardMarkup(keyboard=user_films)
    await message.answer("Enter movie name", reply_markup=user_films_keyboard)
    await state.set_state(DeleteForm.name)


@dp.message(DeleteForm.name)
async def command_delete_movie_handler(message: Message, state: FSMContext) -> None:
    user_films = await list_movie(str(message.from_user.id))
    user_films_types = [[types.KeyboardButton(text=film[2].capitalize())] for film in
                        sorted(user_films, key=lambda movie: movie[2])]
    user_films_names = [film[2] for film in user_films]
    user_films_keyboard = types.ReplyKeyboardMarkup(keyboard=user_films_types)

    if message.text == "/cancel":
        await message.answer("Deleting was canceled", reply_markup=commands_keyboard)
        await state.clear()
        return

    if message.text.lower().strip() not in user_films_names:
        await message.answer("Please select a movie using the keyboard below", reply_markup=user_films_keyboard)
        return

    await delete_movie(message.text.lower().strip(), str(message.from_user.id))
    await message.answer("Movie deleted!", reply_markup=commands_keyboard)
    await state.clear()


@dp.message(Command("add"))
async def command_insert_movie_handler(message: Message, state: FSMContext) -> None:
    await message.answer("Write movie name",
                         reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="/cancel")]]))
    await state.set_state(Form.name)


@dp.message(Form.name)
async def command_insert_movie_handler(message: Message, state: FSMContext) -> None:
    if message.text == "/cancel":
        await message.answer("Adding was canceled", reply_markup=commands_keyboard)
        await state.clear()
        return

    await state.update_data(name=message.text.lower().strip())
    await state.set_state(Form.genre)
    await message.answer("Write movie genre", reply_markup=genres_keyboard)


@dp.message(Form.genre)
async def command_insert_genre_handler(message: Message, state: FSMContext) -> None:
    if message.text == "/cancel":
        await message.answer("Adding was canceled", reply_markup=commands_keyboard)
        await state.clear()
        return

    if message.text.lower().strip().capitalize() not in ["Comedy", "Action", "Drama", "Horror", "Fantasy", "Romance",
                                                         "Cartoon"]:
        await message.answer("Please select a genre using the keyboard below", reply_markup=genres_keyboard)
        return

    await state.update_data(genre=message.text.lower().strip())
    information_film = await state.get_data()
    await insert_movie(str(message.from_user.id), information_film.get("name"), information_film.get("genre"))
    await message.answer("Movie inserted successfully", reply_markup=commands_keyboard)
    await state.clear()


@dp.message()
async def echo_handler(message: Message) -> None:
    if message.text == "/cancel":
        await message.answer("Nothing to cancel", reply_markup=commands_keyboard)
    else:
        await message.answer("Please write command", reply_markup=commands_keyboard)


async def main() -> None:
    await create_database()

    bot = Bot(token=getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
