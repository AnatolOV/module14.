import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT Null
)
''')

# for i in range(10):
#     cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)", (f"User{i+1}", f"example{i+1}@gmail.com", (i+1)*10, 1000))
cursor.execute("UPDATE Users SET balance = 500 WHERE id % 2 != 0")
cursor.execute('DELETE FROM Users WHERE id IN (SELECT id FROM Users WHERE id % 3 = 1)')
cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != 60')
records = cursor.fetchall()

# Выводим записи в консоль в заданном формате
for record in records:
    username, email, age, balance = record
    print(f'Имя: {username} | Почта: {email} | Возраст: {age} | Баланс: {balance}')

connection.commit()
connection.close()
