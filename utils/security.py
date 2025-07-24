import hashlib
import re

def hash_password(password):
    """Hash a password for storing"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    return stored_password == hash_password(provided_password)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[\w\.-]+@([\w\-]+\.)+[A-Za-z]{2,}$'
    return re.match(pattern, email) is not None

def validate_input(data, required_fields):
    """Validate that all required fields are present in the data"""
    errors = []
    for field in required_fields:
        if field not in data or not data[field]:
            errors.append(f"{field} is required")
    
    if 'email' in data and data['email'] and not validate_email(data['email']):
        errors.append("Invalid email format")
    
    return errors