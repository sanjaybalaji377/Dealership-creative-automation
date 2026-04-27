import sqlite3
import os
from ..config import BASE_DIR

DB_PATH = os.path.join(BASE_DIR, "database.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'admin'
    );
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_code TEXT NOT NULL UNIQUE,
        account_name TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS dealerships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_id INTEGER NOT NULL,
        dealer_code TEXT NOT NULL,
        dealer_name TEXT NOT NULL,
        panel_path TEXT,
        logo_light_path TEXT,
        logo_dark_path TEXT,
        FOREIGN KEY (account_id) REFERENCES accounts(id)
    );
    """)
    
    # Check if admin exists
    cursor.execute("SELECT * FROM users WHERE email = 'admin@dealercreative.com'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                       ('Admin', 'admin@dealercreative.com', 'Admin@123'))
        
    # Check if accounts exist (Load initial data)
    cursor.execute("SELECT COUNT(*) FROM accounts")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO accounts (account_code, account_name) VALUES (?, ?)", ('Tata-dealers', 'Tata'))
        cursor.execute("INSERT INTO accounts (account_code, account_name) VALUES (?, ?)", ('VW-dealers', 'Volkswagen'))
        
    conn.commit()
    conn.close()
