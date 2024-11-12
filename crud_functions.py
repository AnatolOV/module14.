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

def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    products = cursor.execute("SELECT * FROM Products").fetchall()
    connection.close()
    return products


# print(get_all_products())
