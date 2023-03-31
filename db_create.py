import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

c.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
c.execute("INSERT INTO users (name, email) VALUES ('John Doe', 'john.doe@example.com')")

conn.commit()

c.execute("SELECT * FROM users")
users = c.fetchall()

for user in users:
    print(user)
