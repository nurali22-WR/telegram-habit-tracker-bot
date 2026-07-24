from database import add_habit, get_habits, update_habit, delete_habit, complete_habit, is_habit_completed_today, get_habit_logs, get_completed_dates, get_habit_name
from telebot import types

import datetime
import telebot

def register_handlers(bot):
    @bot.message_handler(commands=['start'])
    def start(message):
        show_start(message.chat.id)

    def show_start(chat_id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f'❓ Помощь', callback_data='help'))
        bot.send_message(chat_id, "👋 Привет! Я трекер привычек, " \
        "который поможет тебе выработать полезные привычки.", reply_markup=markup)

    @bot.message_handler(commands=['help'])
    def help(message):
        show_help(message.chat.id)

    def show_help(chat_id):
        commands = {
            'start': "🏠 Главное меню",
            'add': "➕ Добавить привычку",
            'list': "📋 Мои привычки",
            'update': "✏️ Изменить привычку",
            'delete': "🗑️ Удалить привычку",
            'complete': "✅ Отметить выполнение",
            'today': "📅 Сегодня",
            'stats': "📊 Статистика",
            'streak': "🔥 Серия",
            'help': "❓ Помощь"
        }
        markup = types.InlineKeyboardMarkup()
        
        for key, value in commands.items():
            markup.add(types.InlineKeyboardButton(f'{value}', callback_data=f'{key}'))
        
        bot.send_message(chat_id, "Список команд\n", reply_markup=markup)

    "Добавить привычку"
    @bot.message_handler(commands=['add'])
    def add(message):
        bot.send_message(message.chat.id, "✏️ Введите привычку: ")
        bot.register_next_step_handler(message, save_habit)

    def save_habit(message):
        user_id = message.from_user.id
        name = message.text

        add_habit(user_id, name)
    
        bot.send_message(message.chat.id, "✅ Готово! Ваша привычка успешно сохранилась! Список привычек /list")

    "Список привычек"
    @bot.message_handler(commands=['list'])
    def list(message):
        show_list(message.chat.id, message.from_user.id)

    def show_list(chat_id, user_id):
        habits = get_habits(user_id)
        
        habits_list = []

        i = 0
        for habit in habits:
            i += 1
            habits_list.append(f"{i}. {habit[1]}")

        bot.send_message(chat_id, "📋 Ваши привычки:\n\n" + '\n'.join(habits_list))



    def show_habits(text, user_id):
        habits = get_habits(user_id)
        markup = types.InlineKeyboardMarkup()
        for habit in habits:
            markup.add(types.InlineKeyboardButton(f'{habit[1]}', callback_data=f'{text}_{habit[0]}'))
        return markup
    
    "Редактирование привычки"
    @bot.message_handler(commands=['update'])
    def update(message):
        show_update(message.chat.id, message.from_user.id)
    def show_update(chat_id, user_id):
        markup = show_habits('update', user_id)
        bot.send_message(chat_id, "📋 Ваши привычки: ", reply_markup=markup)
    def edit_habit(message, id):
        new_name = message.text
        user_id = message.from_user.id

        update_habit(new_name, id, user_id)

        bot.send_message(message.chat.id, "✅ Готово! Название вашей привычки обновилось! Список привычек /list")
    
    "Удалить привычку"
    @bot.message_handler(commands=['delete'])
    def delete(message):
        show_delete(message.chat.id, message.from_user.id)

    def show_delete(chat_id, user_id):
        markup = show_habits('delete', user_id)
        bot.send_message(chat_id, "🗑️ Удалить привычку", reply_markup=markup)

    def process_delete_habit(message, id, user_id):
        habit_name = get_habit_name(id)
        delete_habit(id, user_id)
        bot.send_message(message.chat.id, f"✅ Готово! Ваша привычка {habit_name[0]} успешно удалена! Список привычек /list")

    "Отметить привычку"
    @bot.message_handler(commands=['complete_habit'])
    def complete(message):
        show_complete(message.chat.id, message.from_user.id)

    def show_complete(chat_id, user_id):
        markup = show_habits('complete', user_id)
        bot.send_message(chat_id, "📋 Ваши привычки: ", reply_markup=markup)

    "Статистика за день"
    @bot.message_handler(commands=['today'])
    def today(message):
        show_today(message.chat.id, message.from_user.id)

    def show_today(chat_id, user_id):
        habits = get_habits(user_id)
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")

        today_list = []

        for habit in habits:
            habit_completed_date = is_habit_completed_today(habit[0], today_date)
            if habit_completed_date is not None:
                today_list.append(f"✅ {habit[0]}. {habit[1]}")
            else:
                today_list.append(f"❌ {habit[0]}. {habit[1]}")
        
        bot.send_message(chat_id, "📅 Выполненные привычки за сегодня:\n\n" + '\n'.join(today_list))

    "Общая статистика"
    @bot.message_handler(commands=['stats'])
    def stats(message):
        show_stats(message.chat.id, message.from_user.id)

    def show_stats(chat_id, user_id):
        stats_list = []
        
        habits = get_habits(user_id)
        today_date = datetime.datetime.now().strftime("%Y-%m-%d")

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

        bot.send_message(chat_id, f"📊 Ваша статистика\n\n" + '\n'.join(stats_list))

    "Серия дней!"
    @bot.message_handler(commands=['streak'])
    def streak(message):
        show_streak(message.chat.id, message.from_user.id)

    def show_streak(chat_id, user_id):
        markup = show_habits('streak', user_id)
        bot.send_message(chat_id, "🔥 Посмотреть серию", reply_markup=markup)

    "======================================================================================================"
    "callback.data"
    @bot.callback_query_handler(func=lambda call:True)
    def callback(call):
            if call.data == 'start':
                show_start(call.message.chat.id)

            elif call.data == 'help':
                show_help(call.message.chat.id)
                bot.answer_callback_query(
                    call.id,
                    text="Список команд открыт!"
                )

            elif call.data == 'add':
                bot.send_message(call.message.chat.id, "✏️ Введите привычку: ")
                bot.register_next_step_handler(call.message, save_habit)

            elif call.data == 'list':
                show_list(call.message.chat.id, call.from_user.id)
                bot.answer_callback_query(
                    call.id,
                    text="Список привычек открыт!"
                )

            elif call.data == 'update':
                show_update(call.message.chat.id, call.from_user.id)
            elif call.data.startswith('update_'):
                habit_id = int(call.data.split('_')[1])
                habit_name = get_habit_name(habit_id)

                bot.send_message(call.message.chat.id, f"🔁 Привычка: {habit_name[0]}\n✏️ Введите новое название привычки:")
                bot.register_next_step_handler(call.message, edit_habit, habit_id)

            elif call.data == 'delete':
                show_delete(call.message.chat.id, call.from_user.id)
            elif call.data.startswith('delete_'):
                habit_id = int(call.data.split('_')[1])
                habit_name = get_habit_name(habit_id)
                
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Удалить', callback_data=f'deletehabit_{habit_id}'), (types.InlineKeyboardButton('Отменить', callback_data='cancel')))

                bot.send_message(call.message.chat.id, f"🔁 Привычка: {habit_name[0]}\nУдалить её?", reply_markup=markup)
                bot.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=None
                )
            elif call.data.startswith('deletehabit_'):
                habit_id = int(call.data.split('_')[1])
                user_id = call.from_user.id

                process_delete_habit(call.message, habit_id, user_id)
                bot.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=None
                )
            elif call.data == 'cancel':
                bot.send_message(call.message.chat.id, "❌ Удаление привычки отменено.")
                bot.edit_message_reply_markup(
                    chat_id=call.message.chat.id,
                    message_id=call.message.message_id,
                    reply_markup=None
                )
                
            elif call.data == 'complete':
                show_complete(call.message.chat.id, call.from_user.id)
            elif call.data.startswith('complete_'):
                habit_id = int(call.data.split('_')[1])
                today_date = datetime.datetime.now().strftime("%Y-%m-%d")
                habit_completed_date = is_habit_completed_today(habit_id, today_date)

                habit_name = get_habit_name(habit_id)

                if habit_completed_date is not None:
                    bot.send_message(call.message.chat.id, f"Привычка: {habit_name[0]}\nУже отмечена!")
                    bot.answer_callback_query(
                        call.id,
                        text="Команда выполнена!"
                    )
                else:
                    complete_habit(habit_id, today_date)
                    bot.send_message(call.message.chat.id, f"✅ Готово! Ваша привычка: {habit_name[0]}\nОтмечена!")
                    bot.answer_callback_query(
                        call.id,
                        text="Команда выполнена!"
                    )

            elif call.data == 'today':
                show_today(call.message.chat.id, call.from_user.id)

            elif call.data == 'stats':
                show_stats(call.message.chat.id, call.from_user.id)

            elif call.data == 'streak':
                show_streak(call.message.chat.id, call.from_user.id)
            elif call.data.startswith('streak_'):
                habit_id = int(call.data.split('_')[1])
                today_date = datetime.datetime.now().date()
                dates_list = []
                completed_dates = get_completed_dates(habit_id)

                for date in completed_dates:
                    dates_list.append(date[0])

                streak = 0
                for i in range(len(dates_list)):
                    habit_date = datetime.datetime.strptime(dates_list[i], "%Y-%m-%d").date()
                    if today_date - datetime.timedelta(days=i) == habit_date:
                        streak += 1
                    else:
                        break
                    
                streak_message = ""
                if streak == 1:
                    streak_message = "день"
                elif streak > 1 and streak < 5:
                    streak_message = "дня"
                else:
                    streak_message = "дней"

                habit_name = get_habit_name(habit_id)

                bot.send_message(call.message.chat.id, f"🔁 Привычка: {habit_name[0]}\n🔥 Текущая серия: {streak} " + streak_message)
                bot.answer_callback_query(
                    call.id,
                    text="Команда выполнена!"
                )
