import sqlite3
import hashlib
import os

DB_PATH = "database/users_data.db"

def init_db():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    ''')
    # User Audit History Table (Private Per User)
    c.execute('''
        CREATE TABLE IF NOT EXISTS user_audits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            filename TEXT,
            jurisdiction TEXT,
            status TEXT,
            errors_count INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(username) REFERENCES users(username)
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username: str, password: str) -> tuple[bool, str]:
    if not username or not password:
        return False, "Username and password cannot be empty."
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT username FROM users WHERE username = ?", (username.lower(),))
    if c.fetchone():
        conn.close()
        return False, "Username already exists. Please choose another."
    
    c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
              (username.lower(), hash_password(password)))
    conn.commit()
    conn.close()
    return True, "Account created successfully! You can now log in."

def authenticate_user(username: str, password: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username = ?", (username.lower(),))
    result = c.fetchone()
    conn.close()
    if result and result[0] == hash_password(password):
        return True
    return False

def save_audit_log(username: str, filename: str, jurisdiction: str, status: str, errors_count: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO user_audits (username, filename, jurisdiction, status, errors_count) VALUES (?, ?, ?, ?, ?)",
              (username.lower(), filename, jurisdiction, status, errors_count))
    conn.commit()
    conn.close()

def get_user_audits(username: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT filename, jurisdiction, status, errors_count, timestamp FROM user_audits WHERE username = ? ORDER BY timestamp DESC", (username.lower(),))
    rows = c.fetchall()
    conn.close()
    return [{"Filename": r[0], "Jurisdiction": r[1], "Status": r[2], "Errors": r[3], "Date": r[4]} for r in rows]