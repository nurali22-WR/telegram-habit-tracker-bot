from database import add_habit

import telebot

def register_handlers(bot):
    @bot.message_handler(commands=['add'])
    def add(message):
        bot.send_message(message.chat.id, "Введите привычку: ")
        bot.register_next_step_handler(message, save_habit)

    def save_habit(message):
        user_id = message.from_user.id
        name = message.text

        add_habit(user_id, name)
    
        bot.send_message(message.chat.id, "Готово!")
    