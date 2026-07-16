from database import add_habit, get_habits, update_habit, delete_habit

import telebot

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        bot.send_message(message.chat.id, "👋 Привет! Я трекер привычек, " \
        "который поможет тебе выработать полезные привычки.\nДополнительно /help")

    @bot.message_handler(commands=['help'])
    def help(message):
        bot.send_message(message.chat.id, "Команды:\n"
        "/start - начать работу с ботом\n"
        "/help - команды\n"
        "/add - добавить привычку\n"
        "/list - просмотр привычек\n"
        "/update - обновить название привычки\n"
        "/delete - удалить привычку")

    @bot.message_handler(commands=['add'])
    def add(message):
        bot.send_message(message.chat.id, "Введите привычку: ")
        bot.register_next_step_handler(message, save_habit)

    def save_habit(message):
        user_id = message.from_user.id
        name = message.text

        add_habit(user_id, name)
    
        bot.send_message(message.chat.id, "Готово! Ваша привычка успешно сохранилась! Список привычек /list")

    @bot.message_handler(commands=['list'])
    def list(message):
        user_id = message.from_user.id
        habits = get_habits(user_id)
        
        habits_list = []
        
        for habit in habits:
            habits_list.append(f"{habit[0]}. {habit[1]}")

        bot.send_message(message.chat.id, "Ваши привычки:\n" + '\n'.join(habits_list))

    @bot.message_handler(commands=['update'])
    def update(message):
        bot.send_message(message.chat.id, "✏️ Введите номер привычки:")
        bot.register_next_step_handler(message, process_edit_habit)

    def process_edit_habit(message):
        id = message.text
        bot.send_message(message.chat.id, "✏️ Введите новое название привычки:")
        bot.register_next_step_handler(message, edit_habit, id)

    def edit_habit(message, id):
        new_name = message.text
        user_id = message.from_user.id

        update_habit(new_name, id, user_id)

        bot.send_message(message.chat.id, "Готово! Название вашей привычки обновилось! Список привычек /list")
    
    @bot.message_handler(commands=['delete'])
    def delete(message):
        bot.send_message(message.chat.id, "✏️ Введите номер привычки:")
        bot.register_next_step_handler(message, process_delete_habit)

    def process_delete_habit(message):
        id = message.text
        user_id = message.from_user.id

        delete_habit(id, user_id)

        bot.send_message(message.chat.id, "Готово! Ваша привычка удалена! Список привычек /list")