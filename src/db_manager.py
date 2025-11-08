"""This module is meant to habdle the databases"""
import sqlite3
import os

class DatabaseManager:
    
    def __init__(self) -> None:
        """Initialize the database and assign database path to self.db_path"""
        
        #Double dirname to get the parent directory of the current directory
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database.db')
        self.initialize()
    
    def initialize(self) -> None:
        """Helper function only used to help with initialization"""
        
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS chats (
                id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        c.execute('''CREATE TABLE IF NOT EXISTS messages (
                id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT,
                chat_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
            )
        ''')
        conn.commit()
        conn.close()
    
    def get_connection(self) -> sqlite3.Connection:
        """Function for establishing a connection to the databse, with PRAGMA foregin_keys on"""
        
        conn = sqlite3.connect(self.db_path)
        conn.execute('PRAGMA foreign_keys = ON')
        return conn
