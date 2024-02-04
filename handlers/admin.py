from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from create_bot import dp, bot


ID = None

class FSMAdmin(StatesGroup):
	user_id = State()
	user_name = State()
