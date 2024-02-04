from aiogram import Bot
from aiogram.dispatcher import Dispatcher 
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os
import lyricsgenius as lg


storage = MemoryStorage()

genius = lg.Genius(os.getenv('gTOKEN'))
genius.verbose = False
genius.remove_section_headers = False
genius.excluded_terms = ["(Remix)", "(Live)"]

weather_key = os.getenv('wKEY')

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot, storage=storage)
