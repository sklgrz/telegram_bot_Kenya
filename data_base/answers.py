from random import randint


def select_ask():
	ask = ['Поделись проблемкой, мяу :з', 'Расскажи, что тебя беспокоит?', 'Жду!', 'Скажи в чём беда, я помогу!',
				"Слушаю!!", "Наконец-то! Говори, подскажу!", "мяу мяу мяу!! жду вопрос!!!"]
	return ask[randint(0, len(ask) - 1)]

def select_soviet():
	soviet = ["Бесспорно", "Предрешено", "Никаких сомнений", "Определённо да","Можешь быть уверен в этом", "Мне кажется - да",
				"Вероятнее всего","Хорошие перспективы", "Знаки говорят - да", "Спроси позже",
				"Лучше не рассказывать", "Не знаю, мяу((", "Даже не думай",
				"Мой ответ - нет", "По моим данным - нет", "Перспективы не очень хорошие", "Весьма сомнительно"]
	return soviet[randint(0, len(soviet) - 1)]