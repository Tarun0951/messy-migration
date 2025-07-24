from flask import Blueprint, request, jsonify
from services import user_service
from utils.security import validate_input

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    users = user_service.get_all_users()
    return jsonify(users), 200

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user"""
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"error": "User not found"}), 404

@user_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        # Validate input
        errors = validate_input(data, ['name', 'email', 'password'])
        if errors:
            return jsonify({"errors": errors}), 400
        
        user_id = user_service.create_user(
            name=data['name'],
            email=data['email'],
            password=data['password']
        )
        
        if user_id:
            return jsonify({"message": "User created successfully", "user_id": user_id}), 201
        return jsonify({"error": "Failed to create user"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update a user"""
    try:
        data = request.get_json()
        
        # Validate input
        errors = validate_input(data, ['name', 'email'])
        if errors:
            return jsonify({"errors": errors}), 400
        
        user = user_service.update_user(
            user_id=user_id,
            name=data['name'],
            email=data['email']
        )
        
        if user:
            return jsonify({"message": "User updated successfully", "user": user.to_dict()}), 200
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    try:
        if user_service.get_user_by_id(user_id) is None:
            return jsonify({"error": "User not found"}), 404
            
        user_service.delete_user(user_id)
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/search', methods=['GET'])
def search_users():
    """Search users by name"""
    name = request.args.get('name')
    
    if not name:
        return jsonify({"error": "Please provide a name to search"}), 400
    
    users = user_service.search_users_by_name(name)
    return jsonify(users), 200

@user_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        
        # Validate input
        errors = validate_input(data, ['email', 'password'])
        if errors:
            return jsonify({"errors": errors}), 400
        
        user = user_service.authenticate_user(
            email=data['email'],
            password=data['password']
        )
        
        if user:
            return jsonify({"status": "success", "user_id": user.id}), 200
        return jsonify({"status": "failed", "error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500