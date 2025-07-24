import sqlite3
from sqlite3 import Error

def get_db_connection():
    """Create a database connection to the SQLite database"""
    try:
        conn = sqlite3.connect('users.db', check_same_thread=False)
        conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
        return conn
    except Error as e:
        raise Exception(f"Database connection error: {e}")

def execute_query(query, params=()):
    """Execute a query with parameters"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor
    except Error as e:
        raise Exception(f"Query execution error: {e}")
    finally:
        if conn:
            conn.close()

def execute_read_query(query, params=()):
    """Execute a read query with parameters"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchall()
        return result
    except Error as e:
        raise Exception(f"Query execution error: {e}")
        
    finally:
        if conn:
            conn.close()