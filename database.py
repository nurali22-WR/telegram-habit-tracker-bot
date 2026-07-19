import sqlite3

def create_habits_db():
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT
        )
    """)

    conn.commit()
    conn.close()

def create_habit_logs_db():
    conn = sqlite3.connect("habit_logs.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habit_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            completed_at TEXT,
            FOREIGN KEY (habit_id) REFERENCES habits(id)
        )
    """)

    conn.commit()
    conn.close()



def add_habit(user_id, name):
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO habits (user_id, name) 
    VALUES (?, ?);
    """,
    (user_id, name)
    )

    conn.commit()
    conn.close()

def get_habits(user_id):
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, name
    FROM habits
    WHERE user_id = ?
    """,
    (user_id,)
    )
    
    habits = cursor.fetchall()

    conn.close()
    return habits

def update_habit(name, id, user_id):
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE habits
    SET name = ? 
    WHERE id = ? AND user_id = ?
    """,
    (name, id, user_id)
    )

    conn.commit()
    conn.close()

def delete_habit(id, user_id):
    conn = sqlite3.connect("habits.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM habits
    WHERE id = ? AND user_id = ?
    """,
    (id, user_id)
    )

    conn.commit()
    conn.close()

def complete_habit(habit_id, completed_at):
    conn = sqlite3.connect("habit_logs.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO habit_logs (habit_id, completed_at) 
    VALUES (?, ?);
    """,
    (habit_id, completed_at)
    )

    conn.commit()
    conn.close()

def is_habit_completed_today(habit_id, completed_at):
    conn = sqlite3.connect("habit_logs.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT completed_at
    FROM habit_logs
    WHERE habit_id = ? AND completed_at = ?
    """,
    (habit_id, completed_at)
    )
    
    habit_completed_date = cursor.fetchone()

    conn.close()
    return habit_completed_date

def get_habit_logs():
    conn = sqlite3.connect("habit_logs.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT habit_id, completed_at
    FROM habit_logs
    """
    )
    
    habit_logs = cursor.fetchall()
    
    conn.close()
    return habit_logs















def delete_habit_logs():
    conn = sqlite3.connect("habit_logs.db")
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM habit_logs
    WHERE id = 4
    """,
    )

    conn.commit()
    conn.close()
delete_habit_logs()