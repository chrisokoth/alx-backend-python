import sqlite3

conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )
''')
cursor.execute("INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com')")
conn.commit()
conn.close()
