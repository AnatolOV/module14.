import sqlite3


def initiate_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
    );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL
        );
        ''')

    # Добавление нескольких записей для демонстрации
    products_to_insert = [
        (1, "Продукт 1", "Описание 1", 100),
        (2, "Продукт 2", "Описание 2", 200),
        (3, "Продукт 3", "Описание 3", 300),
        (4, "Продукт 4", "Описание 4", 400),
    ]

    # Делаем исправление: добавляем только те записи, которых ещё нет
    for product in products_to_insert:
        try:
            cursor.execute("INSERT INTO Products (id, title, description, price) VALUES (?, ?, ?, ?)", product)
        except sqlite3.IntegrityError:
            # Игнорируем, если продукт с таким id уже существует
            continue

    connection.commit()
    connection.close()
# initiate_db()
# def add_user(username, email, age):

def add_user(username, email, age):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        cursor.execute('''
        INSERT INTO Users (username, email, age, balance) 
        VALUES (?, ?, ?, ?)
        ''', (username, email, age, 1000))
        connection.commit()
        print("Пользователь добавлен успешно.")
    except sqlite3.IntegrityError:
        print("Ошибка: Пользователь уже существует.")
    connection.close()

def is_included(username):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('''
    SELECT EXISTS(SELECT 1 FROM Users WHERE username = ?)
    ''', (username,))

    return cursor.fetchone()[0] == 1
    connection.close()


def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    products = cursor.execute("SELECT * FROM Products").fetchall()
    connection.close()
    return products

# print(get_all_products())
