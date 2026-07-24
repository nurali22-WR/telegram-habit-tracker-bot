import sqlite3

def get_connection():
    conn = sqlite3.connect("habits.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_habits_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            completed_at TEXT,
            FOREIGN KEY (habit_id)
                REFERENCES habits(id)
                ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def add_habit(user_id, name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO habits (user_id, name)
        VALUES (?, ?)
    """, (user_id, name))

    conn.commit()
    conn.close()


def get_habits(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name
        FROM habits
        WHERE user_id = ?
    """, (user_id,))

    habits = cursor.fetchall()

    conn.close()
    return habits


def update_habit(name, id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE habits
        SET name = ?
        WHERE id = ? AND user_id = ?
    """, (name, id, user_id))

    conn.commit()
    conn.close()


def delete_habit(id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM habits
        WHERE id = ? AND user_id = ?
    """, (id, user_id))

    conn.commit()
    conn.close()


def complete_habit(habit_id, completed_at):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO habit_logs (habit_id, completed_at)
        VALUES (?, ?)
    """, (habit_id, completed_at))

    conn.commit()
    conn.close()


def is_habit_completed_today(habit_id, completed_at):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT completed_at
        FROM habit_logs
        WHERE habit_id = ? AND completed_at = ?
    """, (habit_id, completed_at))

    habit_completed_date = cursor.fetchone()

    conn.close()
    return habit_completed_date


def get_habit_logs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT habit_id, completed_at
        FROM habit_logs
    """)

    habit_logs = cursor.fetchall()

    conn.close()
    return habit_logs


def get_completed_dates(habit_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT completed_at
        FROM habit_logs
        WHERE habit_id = ?
        ORDER BY completed_at DESC
    """, (habit_id,))

    completed_dates = cursor.fetchall()

    conn.close()
    return completed_dates


def get_habit_name(habit_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM habits
        WHERE id = ?
    """, (habit_id,))

    habit_name = cursor.fetchone()

    conn.close()
    return habit_name