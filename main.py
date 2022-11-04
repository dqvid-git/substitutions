import telebot
import getSubs
from time import sleep

API_TOKEN = ''

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Для того, чтобы воспользоваться функционалом бота введи комманду <b>/substitutions</b>', parse_mode='html')

@bot.message_handler(commands=['substitutions'], content_types=['text'])
def substitutuions(message):
    send = bot.send_message(message.chat.id, 'Отправьте название вашей группы. Пример: ПО-22к.')
    bot.register_next_step_handler(send, getSubstitutions)
def getSubstitutions(message):
    waitMsg = bot.send_message(message.chat.id, 'Подождите...')
    msg = getSubs.getSubstitutions(message.text)
    bot.delete_message(message.chat.id, waitMsg.id)
    bot.send_message(message.chat.id, msg)

def start():
    try:
        print("Bot succesfully started.")
        bot.polling(none_stop=True)
    except Exception as _ex:
        print(_ex)
        sleep(15)
        start()
start()
