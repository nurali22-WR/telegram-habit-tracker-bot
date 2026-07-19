from database import add_habit, get_habits, update_habit, delete_habit, complete_habit, is_habit_completed_today, get_habit_logs
from telebot import types
from datetime import datetime

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
        "/delete - удалить привычку\n"
        "/complete_habit - отметить выполнение привычки\n"
        "/today - выполненные привычки за сегодня\n"
        "/stats - статистика")

    @bot.message_handler(commands=['add'])
    def add(message):
        bot.send_message(message.chat.id, "Введите привычку: ")
        bot.register_next_step_handler(message, save_habit)

    def save_habit(message):
        user_id = message.from_user.id
        name = message.text

        add_habit(user_id, name)
    
        bot.send_message(message.chat.id, "✅ Готово! Ваша привычка успешно сохранилась! Список привычек /list")

    @bot.message_handler(commands=['list'])
    def show_list(message):
        user_id = message.from_user.id
        habits = get_habits(user_id)
        
        habits_list = []
        
        for habit in habits:
            habits_list.append(f"{habit[0]}. {habit[1]}")

        bot.send_message(message.chat.id, "📋 Ваши привычки:\n" + '\n'.join(habits_list))

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

        bot.send_message(message.chat.id, "✅ Готово! Название вашей привычки обновилось! Список привычек /list")
    
    @bot.message_handler(commands=['delete'])
    def delete(message):
        bot.send_message(message.chat.id, "✏️ Введите номер привычки:")
        bot.register_next_step_handler(message, process_delete_habit)

    def process_delete_habit(message):
        id = message.text
        user_id = message.from_user.id

        delete_habit(id, user_id)

        bot.send_message(message.chat.id, "✅ Готово! Ваша привычка удалена! Список привычек /list")

    @bot.message_handler(commands=['complete_habit'])
    def complete(message):
        user_id = message.from_user.id
        habits = get_habits(user_id)

        markup = types.InlineKeyboardMarkup()

        for habit in habits:
            markup.add(types.InlineKeyboardButton(f'{habit[1]}', callback_data=f'complete_{habit[0]}'))

        bot.send_message(message.chat.id, "📋 Ваши привычки: ", reply_markup=markup)

    @bot.message_handler(commands=['today'])
    def today(message):
        user_id = message.from_user.id
        habits = get_habits(user_id)
        today_date = datetime.now().strftime("%Y-%m-%d")

        today_list = []

        for habit in habits:
            habit_completed_date = is_habit_completed_today(habit[0], today_date)
            if habit_completed_date is not None:
                today_list.append(f"✅ {habit[0]}. {habit[1]}")
            else:
                today_list.append(f"❌ {habit[0]}. {habit[1]}")
        
        bot.send_message(message.chat.id, "📋 Выполненные привычки за сегодня:\n\n" + '\n'.join(today_list))

    @bot.message_handler(commands=['stats'])
    def stats(message):
        stats_list = []

        user_id = message.from_user.id
        habits = get_habits(user_id)
        today_date = datetime.now().strftime("%Y-%m-%d")

        "Количество всех привычек"
        total_habits = len(habits)

        "Количество выполненных привычек за сегодня"
        total_completed_today = 0
        for habit in habits:
            habit_completed_date = is_habit_completed_today(habit[0], today_date)
            if habit_completed_date is not None:
                total_completed_today += 1
        
        "Процент выполнения привычек"
        completed_habits_percent = 0
        if total_habits == 0:
            completed_habits_percent = 0
        else:
            completed_habits_percent = round((total_completed_today / total_habits) * 100)
        
        "Количество отметок"
        total_marks = len(get_habit_logs())

        stats_list.append(f"📋 Всего привычек: {total_habits}")
        stats_list.append(f"✅ Выполнено сегодня: {total_completed_today}")
        stats_list.append(f"❌ Осталось: {total_habits - total_completed_today}")
        stats_list.append(f"📈 Выполнение: {completed_habits_percent}%")
        stats_list.append(f"🏆 Всего отметок: {total_marks}")

        bot.send_message(message.chat.id, f"📊 Ваша статистика\n\n" + '\n'.join(stats_list))
            

    "======================================================================================================"
    "callback.data"
    @bot.callback_query_handler(func=lambda call:True)
    def callback(call):
            if call.data == 'help':
                bot.answer_callback_query(
                    call.id,
                    text="Список команд открыт!"
            )
            elif call.data.startswith('complete_'):
                habit_id = int(call.data.split('_')[1])
                today_date = datetime.now().strftime("%Y-%m-%d")
                habit_completed_date = is_habit_completed_today(habit_id, today_date)

                if habit_completed_date is not None:
                    bot.send_message(call.message.chat.id, "Привычка уже отмечена!")
                else:
                    complete_habit(habit_id, today_date)
                    bot.send_message(call.message.chat.id, "✅ Готово! Ваша привычка отмечена!")

