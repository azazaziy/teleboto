import telebot
import config
import random
import pyowm
import time
from telebot import types


bot = telebot.TeleBot(config.TOKEN)
owm = pyowm.OWM(config.OWM_API, language = 'ru')
'''covid19 = COVID19Py.COVID19()'''

@bot.message_handler(commands = ['start'])
def send_welcome(message):

	#keyboard
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	rnd_button = types.KeyboardButton('рандомное число')
	how_button = types.KeyboardButton('Как дела?')
	sponsor_button = types.KeyboardButton('Спонсировать')
	weather_button = types.KeyboardButton('Узнать погоду')
	markup.add(rnd_button, how_button, sponsor_button, weather_button,)
	bot.send_message(message.chat.id,
					 "Приветствую, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный коварным гением.".format(message.from_user,
					 bot.get_me()),
					 parse_mode = 'html',
					 reply_markup = markup)

@bot.message_handler(commands = ['weather'])
def ask_place(message):
	city = bot.send_message(message.chat.id, 'Напишите название города в котором хотите узнать погоду')
	bot.register_next_step_handler(city, sendWeathaer)
def sendWeathaer(message):
	bot.send_message(message.chat.id, 'Ищу погоду в городе {city}'.format(city = message.text))
	time.sleep(2)
	try:
		observation = owm.weather_at_place(message.text)
		w = observation.get_weather()
		status = w.get_detailed_status()
		temp = w.get_temperature('celsius')['temp']
		bot.send_message(message.chat.id, 'В городе {city}, {status}\nТемпература около {temp}'.format(city = message.text,status = (status), temp = (temp)))
	except:
		bot.send_message(message.chat.id, 'Вы ошиблись в названии города')

@bot.message_handler(content_types = ['text'])
def chating(message):

	if message.chat.type == 'private':

		if message.text == 'рандомное число':
			bot.send_message(message.chat.id, str(random.randint(0,10000)))

		elif message.text == 'Как дела?':

			#inline keyboard
			markup = types.InlineKeyboardMarkup(row_width = 2)
			in_good = types.InlineKeyboardButton("хорошо", callback_data = 'good')
			in_bad = types.InlineKeyboardButton('плохо', callback_data = 'bad')
			markup.add(in_good, in_bad)
			bot.send_message(message.chat.id,
							 'Отлично!\nА у тебя, {0.first_name}?'.format(message.from_user,
							 bot.get_me()),
							 parse_mode = 'html',
							 reply_markup = markup)

		elif message.text == 'Спонсировать':

			#inline keyboard
			markup = types.InlineKeyboardMarkup(row_width=3)
			sber = types.InlineKeyboardButton('Cбербанк', callback_data= 'sberbank')
			tink = types.InlineKeyboardButton('Тинькофф', callback_data='tinkoff')
			qiwi = types.InlineKeyboardButton('Qiwi', callback_data='qiwi')
			markup.add(sber, tink, qiwi)
			bot.send_message(message.chat.id,
							 'Выберите кошелек которым хотите произвести тразакцию:',
							 reply_markup=markup)

		elif message.text == 'Узнать погоду':
			bot.send_message(message.chat.id, 'для того что бы узнать погоду напиши /weather')

		elif message.text == ('Коронавирус'):
			bot.send_message(message.chat.id, 'для того что бы узнать погоду напиши /virus')


		else:
			bot.send_message(message.chat.id, 'На этом мои полномочия все=(')


@bot.callback_query_handler(func = lambda call: True)
def callback_inline(call):
	try:

		if call.message:
			#HOW?
			if call.data == 'good':
				bot.send_message(call.message.chat.id, 'Отлично)')
				bot.edit_message_text(chat_id=call.message.chat.id,
									  message_id=call.message.message_id,
									  text='Как дела?',
									  reply_markup=None)

			elif call.data == 'bad':
				bot.send_message(call.message.chat.id, 'бывает')
				bot.edit_message_text(chat_id=call.message.chat.id,
									  message_id=call.message.message_id,
									  text='Как дела?',
									  reply_markup=None)

			elif call.data == 'sberbank':
				bot.send_message(call.message.chat.id,
								 'Реквизит для сбербанка:\nномер карты - 5469440021518288')
				bot.edit_message_text(chat_id=call.message.chat.id,
									  message_id=call.message.message_id,
									  text='Спонсировать',
									  reply_markup=None)
			#SPONSOR
			elif call.data == 'tinkoff':
				bot.send_message(call.message.chat.id,
								 'Реквизит для Тинькофф банка:\nномер карты - 5536913849893405')
				bot.edit_message_text(chat_id=call.message.chat.id,
									  message_id=call.message.message_id,
									  text='Спонсировать',
									  reply_markup=None)

			elif call.data == 'qiwi':
				bot.send_message(call.message.chat.id,
								 'Реквизиты для Qiwi:\nномер qiwi - 89133964934')
				bot.edit_message_text(chat_id=call.message.chat.id,
									  message_id=call.message.message_id,
									  text='Спонсировать',
									  reply_markup=None)

			bot.answer_callback_query(chat_id=call.message.chat.id,
									  show_alert=True,
									  text='ОпА аВоТ и ПоСхАлОЧКА')
	except Exception as e:
		print(repr(e))



#run
bot.polling(none_stop = True)