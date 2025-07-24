import sqlite3
from utils.security import hash_password

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Hash passwords before storing
    hashed_password1 = hash_password('password123')
    hashed_password2 = hash_password('secret456')
    hashed_password3 = hash_password('qwerty789')

    # Check if users already exist
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                      ('John Doe', 'john@example.com', hashed_password1))
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                      ('Jane Smith', 'jane@example.com', hashed_password2))
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                      ('Bob Johnson', 'bob@example.com', hashed_password3))

    conn.commit()
    conn.close()

    print("Database initialized with sample data")

if __name__ == "__main__":
    init_db()