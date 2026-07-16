import sqlite3

def create_db():
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