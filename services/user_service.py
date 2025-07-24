from database import execute_query, execute_read_query
from models.user import User
from utils.security import hash_password, verify_password

def get_all_users():
    """Get all users from the database"""
    query = "SELECT * FROM users"
    rows = execute_read_query(query)
    return [User.from_row(row).to_dict() for row in rows] if rows else []

def get_user_by_id(user_id):
    """Get a user by ID"""
    query = "SELECT * FROM users WHERE id = ?"
    rows = execute_read_query(query, (user_id,))
    return User.from_row(rows[0]) if rows else None

def create_user(name, email, password):
    """Create a new user"""
    hashed_password = hash_password(password)
    query = "INSERT INTO users (name, email, password) VALUES (?, ?, ?)"
    cursor = execute_query(query, (name, email, hashed_password))
    return cursor.lastrowid if cursor else None

def update_user(user_id, name, email):
    """Update a user's information"""
    query = "UPDATE users SET name = ?, email = ? WHERE id = ?"
    execute_query(query, (name, email, user_id))
    return get_user_by_id(user_id)

def delete_user(user_id):
    """Delete a user"""
    query = "DELETE FROM users WHERE id = ?"
    execute_query(query, (user_id,))
    return True

def search_users_by_name(name):
    """Search users by name"""
    query = "SELECT * FROM users WHERE name LIKE ?"
    rows = execute_read_query(query, (f'%{name}%',))
    return [User.from_row(row).to_dict() for row in rows] if rows else []

def authenticate_user(email, password):
    """Authenticate a user"""
    query = "SELECT * FROM users WHERE email = ?"
    rows = execute_read_query(query, (email,))
    if not rows:
        return None
    
    user = User.from_row(rows[0])
    if verify_password(user.password, password):
        return user
    return None