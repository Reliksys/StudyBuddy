import sqlite3
def init_db():
    conn = sqlite3.connect('database_of_project.db')
    cursor = conn.cursor()

    create_table_cards = """
    CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL UNIQUE,
        answer TEXT NOT NULL
    );
    """

    create_table_timetable = """
    CREATE TABLE IF NOT EXISTS timetable (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        deadline TEXT NOT NULL,
        difficulty INTEGER NOT NULL,
        priority TEXT NOT NULL,   -- <--- НОВАЯ КОЛОНКА
        start_date TEXT NOT NULL,
        status TEXT DEFAULT 'Active'
    );
    """

    cursor.execute(create_table_cards)
    cursor.execute(create_table_timetable)
    conn.commit()
    conn.close()


def create_task(title, deadline, difficulty, priority, start_date):
    conn = sqlite3.connect('database_of_project.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO timetable (title, deadline, difficulty, priority, start_date) VALUES (?, ?, ?, ?, ?)",
        (title, deadline, difficulty, priority, start_date)
    )
    conn.commit()
    conn.close()


def create_card(question, answer):
    conn = sqlite3.connect('database_of_project.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO flashcars (question, answer) VALUES (?, ?)",
        (question, answer)
    )
    conn.commit()
    conn.close()

def get_all_tasks():
    conn = sqlite3.connect('database_of_project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM timetable WHERE status = 'Active' ORDER BY deadline")
    tasks = cursor.fetchall()
    conn.close()    
    return tasks


def get_all_cards():
    conn = sqlite3.connect('database_of_project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM flashcards")
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def done_task(id):
    conn = sqlite3.connect('database_of_project.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE timetable SET status = 'Done' WHERE id = ?",
                   (id))
    conn.commit()
    conn.close()

