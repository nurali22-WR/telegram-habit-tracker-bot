<div align="center">

<img src="assets/logo.png" width="180">

# 🤖 HabitTrackerBot

### Telegram-бот для отслеживания ежедневных привычек

Помогает формировать полезные привычки, отслеживать прогресс и поддерживать мотивацию.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![SQLite](https://img.shields.io/badge/SQLite-Database-green)
![Telegram](https://img.shields.io/badge/pyTelegramBotAPI-4.34.0-2CA5E0)
![Version](https://img.shields.io/badge/Version-v1.0-success)

</div>

---

## 📖 О проекте

**HabitTrackerBot** — это Telegram-бот, разработанный на Python для отслеживания ежедневных привычек.

Проект был создан в учебных целях и позволил изучить работу с базами данных SQLite, SQL-запросами, Telegram Bot API и организацией проекта на несколько модулей.

---

## ✨ Возможности

- ➕ Добавление привычек
- 📋 Просмотр списка привычек
- ✏️ Редактирование привычек
- 🗑️ Удаление с подтверждением
- ✅ Отметка выполнения привычек
- 🚫 Защита от повторного выполнения за один день
- 📅 Просмотр привычек за сегодня
- 📊 Статистика выполнения
- 🔥 Подсчёт текущей серии дней (Streak)
- 🎛️ Полностью интерактивное управление через Inline-кнопки

---

## 🛠 Используемые технологии

- Python
- pyTelegramBotAPI
- SQLite
- SQL
- Git
- GitHub
- python-dotenv

---

## 📸 Скриншоты

### Главное меню

![Главное меню](screenshots/main_menu.png)

---

### Статистика и серия дней

![Статистика](screenshots/statistics.png)

---

### Удаление привычки

![Удаление](screenshots/delete.png)

---

## 📁 Структура проекта

```text
HabitTrackerBot/
│
├── assets/
│   └── logo.png
│
├── screenshots/
│   ├── main_menu.png
│   ├── statistics.png
│   └── delete.png
│
├── config.py
├── database.py
├── handlers.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Установка

### 1. Клонировать репозиторий

```bash
git clone https://github.com/nurali22-WR/telegram-habit-tracker-bot.git
```

### 2. Перейти в папку проекта

```bash
cd telegram-habit-tracker-bot
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Создать файл `.env`

```env
TOKEN=ВАШ_ТОКЕН_БОТА
```

### 5. Запустить бота

```bash
python main.py
```

---

## 🎯 Что было изучено в ходе разработки

Во время создания проекта были освоены:

- Работа с SQLite
- CRUD-операции
- SQL-запросы
- Работа с несколькими таблицами
- Callback Query
- Inline-клавиатуры
- Работа с датами
- Подсчёт статистики
- Алгоритм вычисления текущей серии дней
- Организация проекта на несколько файлов
- Работа с Git и GitHub

---

## 🚀 Возможные улучшения

В будущем проект можно расширить:

- 🔔 Напоминания о привычках
- ☁️ Переход на PostgreSQL
- 🌐 Собственный REST API
- 📈 Более подробная аналитика
- 🐳 Docker
- 🌍 Веб-интерфейс

---

## 👨‍💻 Автор

Проект разработан в образовательных целях для изучения Python, SQLite и разработки Telegram-ботов.