# make sqlite connection and create tables

import sqlite3

def create_connection():
    conn = sqlite3.connect('messages.db')
    return conn

def create_table(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message TEXT NOT NULL,
            room_code TEXT,
            password TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    cursor.close()
    
def insert_message(conn, message):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (message) VALUES (?)
    ''', (message,))
    conn.commit()
    cursor.close()
    
def get_messages(conn):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT message FROM messages
    ''')
    messages = cursor.fetchall()
    cursor.close()
    return messages