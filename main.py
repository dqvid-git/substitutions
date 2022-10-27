import telebot
import getSubs
import os

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
    msg = getSubs.getSubstitutions(message.text)
    bot.send_message(message.chat.id, msg)

print("Bot succesfully started.")
bot.polling(none_stop=True)
