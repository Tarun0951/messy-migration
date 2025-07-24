from utils.security import hash_password

class User:
    def __init__(self, id=None, name=None, email=None, password=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
    
    @classmethod
    def from_row(cls, row):
        """Create a User object from a database row"""
        if row is None:
            return None
        return cls(
            id=row['id'],
            name=row['name'],
            email=row['email'],
            password=row['password']
        )
    
    def to_dict(self):
        """Convert User object to dictionary (excluding password)"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }
    
    def set_password(self, password):
        """Set hashed password"""
        self.password = hash_password(password)