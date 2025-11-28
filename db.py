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
        start_date TEXT NOT NULL
    );
    """

    cursor.execute(create_table_cards)
    cursor.execute(create_table_timetable)
    conn.commit()
    conn.close()


def create_task(title, deadline, difficulty, start_date):
    conn = sqlite3.connect('database_of_project.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO timetable (title, deadline, difficulty, start_date) VALUES (?, ?, ?, ?)",
        (title, deadline, difficulty, start_date)
    )

    conn.commit()
    conn.close()


def create_card(question, answer):
    conn = sqlite3.connect('database_of_project.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO timetable (question, answer) VALUES (?, ?)",
        (question, answer)
    )

def get_all_tasks():
    conn = sqlite3.connect('database_of_project.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM timetable ORDER BY deadline")
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
