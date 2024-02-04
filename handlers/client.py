from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram import types, Dispatcher
from create_bot import dp, bot, genius, weather_key
from keyboards import kb_client
from data_base import answers
from aiohttp import ClientSession

#import requests
from random import choice, seed, shuffle


class FSMSoviet(StatesGroup):
	soviet = State()

class FSMusic(StatesGroup):
	artist = State()
	song = State()  

class FSMPassword(StatesGroup):
	input_seed = State()
	input_number = State()

async def commands_start(message : types.Message):
	try:
		await bot.send_message(message.from_user.id, 'Приветствую!\nЯ - Кеня. Надеюсь я стану для тебя хорошим другом. Давай поговорим?)',\
			reply_markup=kb_client)
		await message.delete()
	except:
		await message.reply("Общение с Кеней через ЛС, напишите ему: \nhttp://t.me/KenyaTyanBot")

async def find_recommendation(message : types.Message):
	await bot.send_message(message.from_user.id, answers.select_ask(), reply_markup=ReplyKeyboardRemove())
	await FSMSoviet.soviet.set()

async def make_a_recommendation(message : types.Message, state : FSMContext):
	await bot.send_message(message.from_user.id, answers.select_soviet(), reply_markup=kb_client)
	await state.finish()


async def find_music_start(message : types.Message):
	await bot.send_message(message.from_user.id, 'Чью песню ищем?', reply_markup=ReplyKeyboardRemove())
	await FSMusic.artist.set()

async def find_music_artist(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data['artist'] = message.text
	await FSMusic.next()
	await bot.send_message(message.from_user.id, 'Название песни?')

async def find_music_song(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data['song'] = message.text
	try:
		lyrics = genius.search_song(data['song'], data['artist']).lyrics
		lyrics = lyrics[lyrics.find(']') + 2:]

		while len(lyrics) > 4096:
			mes = lyrics[:4096].rfind('\n') 
			await bot.send_message(message.from_user.id, lyrics[:mes])
			lyrics = lyrics[mes:]

		if 'Embed' in lyrics:
			lyrics = lyrics[:lyrics.rfind('Embed')]

		await state.finish()
		await bot.send_message(message.from_user.id, lyrics, reply_markup=kb_client)
	
	except:
		await bot.send_message(message.from_user.id, 'Ничего не нашёл', reply_markup=kb_client)
		await state.finish()

async def check_weather(message : types.Message):
	try:
	#	city = requests.get('https://ipinfo.io/json').json()['city']
		async with ClientSession() as session:
			
			url = "https://ipinfo.io/json"
			async with session.get(url=url) as responce:
				city = await responce.json()
				city = city['city']

			url = 'https://api.openweathermap.org/data/2.5/weather'
			params = {
			'q' : city,
			'appid' : weather_key,
			'units' : 'metric',
			'lang' : 'ru'
			}
			async with session.get(url=url, params=params) as responce:
				wea = await responce.json()

		smile = {
		'ясно' : "☀️",
		'облачно' : "🌤",
		'облачно с прояснениями' : "☁️",
		'дождь' : "🌧",
		'пасмурно' : "☁️",
		'снег' : '🌨'
		}

		answer = f"Погода - {wea['name']}:\n{wea['weather'][0]['description'].capitalize()}, "
		answer += f"{smile.get(wea['weather'][0]['description'], '')}"
		answer += f"\n{wea['main']['temp']} °C; ощущается как {wea['main']['feels_like']} °C."
		answer += f"\nВетер: {wea['wind']['speed']} м/с."

		await bot.send_message(message.from_user.id, answer)
	except:
		await bot.send_message(message.from_user.id, "Не могу получить данные о погоде")

async def take_password_start(message : types.Message):

    await bot.send_message(message.from_user.id, "Ожидаю кодовое слово...", reply_markup=ReplyKeyboardRemove())
    await FSMPassword.input_seed.set()


async def take_password_seed(message : types.Message, state : FSMContext):
	async with state.proxy() as data:
		data['seed'] = message.text
		data['number'] = 0

	await bot.send_message(message.from_user.id, "Номер...")
	await FSMPassword.input_number.set()

async def take_password_number(message : types.Message, state : FSMContext):

	async with state.proxy() as data:
		try:
			data['number'] = int(message.text)
		except:
			data['number'] = 1
			await bot.send_message(message.from_user.id, "Пиши цифру, дурак. Установлен номер 1.")

	digits = '0123456789'
	lowercase_letters = 'abcdefghijklmnopqrstuvwxyz'
	uppercase_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	punctuation = '!#$%&*+-=?@^_.'
	chars = '0123456789abcdefghijklmnopqrstuvwxyz!#$%&*+-=?@^_.'

	lst = [digits, lowercase_letters, uppercase_letters, punctuation]
	seed(data['seed'])

	for pas_num in range(data['number']):
		symbols = 2
		result = []

		for i in lst:
			for _ in range(symbols):
				result.append(choice(i))

		for i in range(symbols):
			result += choice(chars)

		shuffle(result)
		if pas_num == (data['number'] - 1):
			await bot.send_message(message.from_user.id, ''.join(result), reply_markup=kb_client)
	await state.finish()






def register_handlers_client(dp : Dispatcher):
	dp.register_message_handler(commands_start, commands=['start', 'help'])

	dp.register_message_handler(find_recommendation, commands=['Посоветоваться'], state=None)
	dp.register_message_handler(make_a_recommendation, state=FSMSoviet.soviet)

	dp.register_message_handler(find_music_start, commands=['Найти_текст_песни'], state=None)
	dp.register_message_handler(find_music_artist, state=FSMusic.artist)
	dp.register_message_handler(find_music_song, state=FSMusic.song)

	dp.register_message_handler(check_weather, commands=['Погода'])

	dp.register_message_handler(take_password_start, commands=['Пароль'], state=None)
	dp.register_message_handler(take_password_seed, state=FSMPassword.input_seed)
	dp.register_message_handler(take_password_number, state=FSMPassword.input_number)
