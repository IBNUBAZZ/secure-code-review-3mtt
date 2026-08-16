import sqlite3
from werkzeug.security import generate_password_hash

DB = "users.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS users")
cur.execute(
    '''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    '''
)

# The secure application uses the same database but verifies the stored hash.
cur.execute(
    "INSERT INTO users (username, password) VALUES (?, ?)",
    ("student", generate_password_hash("ChangeMe123!"))
)

conn.commit()
conn.close()

print("Created users.db with demo account: student / ChangeMe123!")
