import sqlite3
from typing import List

def get_connection():
    """Создание подключения к базе данных"""
    return sqlite3.connect('database_of_project.db')

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

def create_card(front: str, back: str, category: str, difficulty: int) -> None:
    """Создать новую карточку"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            front TEXT NOT NULL,
            back TEXT NOT NULL,
            category TEXT,
            difficulty INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute(
        "INSERT INTO cards (front, back, category, difficulty) VALUES (?, ?, ?, ?)",
        (front, back, category, difficulty)
    )
    conn.commit()
    conn.close()

def get_all_cards() -> List[tuple]:
    """Получить все карточки"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cards ORDER BY created_at DESC")
    cards = cursor.fetchall()
    conn.close()
    return cards

def get_cards_by_ids(ids: List[int]) -> List[tuple]:
    """Получить карточки по списку ID"""
    if not ids:
        return []
    conn = get_connection()
    cursor = conn.cursor()
    placeholders = ','.join('?' * len(ids))
    cursor.execute(f"SELECT * FROM cards WHERE id IN ({placeholders})", ids)
    cards = cursor.fetchall()
    conn.close()
    return cards

def get_cards_by_category(category: str) -> List[tuple]:
    """Получить карточки по категории"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cards WHERE category = ?", (category,))
    cards = cursor.fetchall()
    conn.close()
    return cards

def get_categories() -> List[str]:
    """Получить список всех категорий"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM cards WHERE category IS NOT NULL")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

def update_card(card_id: int, front: str, back: str, category: str, difficulty: int) -> None:
    """Обновить карточку"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE cards 
        SET front = ?, back = ?, category = ?, difficulty = ?
        WHERE id = ?
    ''', (front, back, category, difficulty, card_id))
    conn.commit()
    conn.close()

def delete_card(card_id: int) -> None:
    """Удалить карточку"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
    conn.commit()
    conn.close()

