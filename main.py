from config import TOKEN
from database import create_habits_db
from handlers import register_handlers

import telebot

create_habits_db()

bot = telebot.TeleBot(TOKEN)

register_handlers(bot)

bot.polling(none_stop=True)