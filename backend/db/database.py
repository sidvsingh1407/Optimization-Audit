import sqlite3
import os
from contextlib import contextmanager
from backend.config.settings import settings
from backend.utils.logger import app_logger

class DatabaseError(Exception):
    """Custom exception for database failures."""
    pass

@contextmanager
def get_db_connection():
    """
    Context manager for safe SQLite database connections.
    Ensures connections are properly closed even if errors occur.
    """
    db_path = settings.db_path

    # Ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        # Enable foreign keys and set row factory
        conn.execute("PRAGMA foreign_keys = 1")
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        app_logger.error(f"Database connection error: {e}")
        raise DatabaseError(f"Failed to connect to database: {e}") from e
    finally:
        if conn:
            conn.close()

def init_db():
    """
    Initializes lightweight SQLite tables if they don't exist.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Create a simple audits table as a starting point
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    company_name TEXT NOT NULL,
                    audit_date TEXT NOT NULL,
                    total_score INTEGER,
                    rating TEXT,
                    raw_data_path TEXT
                )
            ''')
            conn.commit()
            app_logger.info("Database initialized successfully.")
    except DatabaseError as e:
        app_logger.error(f"Failed to initialize database: {e}")
        # We don't raise here to allow graceful degradation (app can run without DB for MVP)

def safe_save_audit(company_name: str, audit_date: str, total_score: int, rating: str, raw_data_path: str = None) -> bool:
    """
    Safely saves an audit to the database.
    Returns True if successful, False otherwise.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO audits (company_name, audit_date, total_score, rating, raw_data_path)
                VALUES (?, ?, ?, ?, ?)
            ''', (company_name, audit_date, total_score, rating, raw_data_path))
            conn.commit()
            return True
    except DatabaseError as e:
        app_logger.error(f"Failed to save audit for {company_name}: {e}")
        return False
