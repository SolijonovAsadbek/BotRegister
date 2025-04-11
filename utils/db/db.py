import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
url = os.path.join(BASE_DIR, 'sqlite.db')
print(url)

conn = sqlite3.connect(url)
curr = conn.cursor()


def create_user():
    sql = """
    CREATE TABLE IF NOT EXISTS user (
    chat_id INTEGER NOT NULL, 
    fullname TEXT, 
    username TEXT,
    phone TEXT, 
    lang TEXT DEFAULT 'uz',
    PRIMARY KEY (chat_id AUTOINCREMENT )
    );
    """
    with conn:
        curr.execute(sql)
    print("`user` jadval muvafaqqiyatli yaratildi!")


def insert_user(chat_id, fullname, username, phone, lang):
    sql = """
    INSERT INTO user (chat_id, fullname, username, phone, lang)
    VALUES (?, ?, ?, ?, ?);
    """
    try:
        with conn:
            curr.execute(sql, (chat_id, fullname, username, phone, lang))
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
    except sqlite3.IntegrityError as e:
        print(f"UNIQUE Error: {e}")
    else:
        print(f"user id: {chat_id} fullname: {fullname} `user` jadvalga muvafaqqiyatli qo'shildi!")


if __name__ == '__main__':
    create_user()
    insert_user(1311, 'Alex Benjamin', '@alexpy007', '998902322334', 'uz')
