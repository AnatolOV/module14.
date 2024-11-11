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
# cursor.execute("UPDATE Users SET balance = 500 WHERE id % 2 != 0")
# cursor.execute('DELETE FROM Users WHERE id IN (SELECT id FROM Users WHERE id % 3 = 1)')
# cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != 60')

#удаляем 6-й элемент:
# cursor.execute("DELETE FROM Users WHERE id = 6")

#считаем общее количество пользователей:
# cursor.execute("SELECT COUNT (*) FROM Users")

# считаем сумму всех балансов:
# cursor.execute("SELECT SUM(balance) FROM Users")

# Выводим в консоль средний баланс всех пользователей:
# 1-й вариант:
# cursor.execute("SELECT SUM(balance) FROM Users")
# total1 = cursor.fetchone()[0]
# print(total1)
# cursor.execute("SELECT COUNT(*) FROM Users")
# total2 = cursor.fetchone()[0]
# print(total1/total2)

# 2-й вариант:
# cursor.execute("SELECT AVG(balance) FROM Users")
# print(cursor.fetchone()[0])

records = cursor.fetchall()
print(records)

connection.commit()
connection.close()