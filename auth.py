from flask import Blueprint, request, jsonify
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
import json
from functools import wraps

from database import db

def admin_required(f):
    """Decorator to ensure the user has an 'admin' role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-User-Role') != 'admin':
            return jsonify({'error': 'Administrator access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    from automation import process_event
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400
    
    # Find user case-insensitively by using a regex with the 'i' option.
    user = db.users.find_one({'username': {'$regex': f"^{data['username']}$", '$options': 'i'}})
    if not user or not check_password_hash(user['password'], data['password']):
        logging.warning(f"Auth: Failed login attempt for user '{data['username']}'.")
        return jsonify({'error': 'Invalid username or password'}), 401

    logging.info(f"Auth: User '{user['username']}' logged in successfully.")
    # Trigger automation event for user login
    process_event('user_login', {'username': user['username']})
    # Don't send the password hash to the client
    user.pop('password', None)
    return json.loads(json_util.dumps({'status': 'success', 'user': user}))

@auth_bp.route('/api/users/all', methods=['GET'])
@admin_required
def get_all_users():
    users = list(db.users.find({}, {'password': 0})) # Exclude passwords
    return json.loads(json_util.dumps(users))

@auth_bp.route('/api/users/set-role', methods=['POST'])
@admin_required
def set_user_role():
    data = request.get_json()
    if not data or 'username' not in data or 'role' not in data:
        return jsonify({'error': 'Missing username or role'}), 400
    username_to_change = data['username']
    new_role = data['role']
    if new_role not in ['admin', 'user']:
        return jsonify({'error': 'Invalid role specified'}), 400
    # Prevent demoting the last admin
    user_to_demote = db.users.find_one({'username': username_to_change})
    if user_to_demote and user_to_demote.get('role') == 'admin' and new_role == 'user':
        if db.users.count_documents({'role': 'admin'}) <= 1:
            return jsonify({'error': 'Cannot demote the last administrator.'}), 400
    result = db.users.update_one({'username': username_to_change}, {'$set': {'role': new_role}})
    if result.matched_count == 0:
        return jsonify({'error': 'User not found'}), 404
    logging.info(f"Auth: User '{username_to_change}' role changed to '{new_role}'.")
    return jsonify({'status': 'success', 'message': f"User '{username_to_change}' role updated to '{new_role}'."})

@auth_bp.route('/api/users/create', methods=['POST'])
@admin_required
def create_user():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data or 'role' not in data:
        return jsonify({'error': 'Missing username, password, or role'}), 400
    username = data['username']
    if db.users.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 409
    if data['role'] not in ['admin', 'user']:
        return jsonify({'error': 'Invalid role specified'}), 400

    new_user = {
        'username': username,
        'password': generate_password_hash(data['password']),
        'role': data['role']
    }
    db.users.insert_one(new_user)
    logging.info(f"Auth: Admin created new user '{username}' with role '{data['role']}'.")   
    new_user.pop('password', None)
    return json.loads(json_util.dumps({'status': 'success', 'user': new_user})), 201

@auth_bp.route('/api/users/change-password', methods=['POST'])
@admin_required
def change_user_password():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or new password'}), 400
    hashed_password = generate_password_hash(data['password'])
    result = db.users.update_one({'username': data['username']}, {'$set': {'password': hashed_password}})
    if result.matched_count == 0:
        return jsonify({'error': 'User not found'}), 404
    logging.info(f"Auth: Password for user '{data['username']}' was changed by an admin.")
    return jsonify({'status': 'success', 'message': f"Password for '{data['username']}' has been updated."})

@auth_bp.route('/api/users/delete/<username>', methods=['DELETE'])
@admin_required
def delete_user(username):
    admin_username = request.headers.get('X-User-Username')
    if username == admin_username:
        return jsonify({'error': 'Administrators cannot delete their own account.'}), 400
    user_to_delete = db.users.find_one({'username': username})
    if not user_to_delete:
        return jsonify({'error': 'User not found'}), 404
    # Prevent deleting the last admin
    if user_to_delete.get('role') == 'admin' and db.users.count_documents({'role': 'admin'}) <= 1:
        return jsonify({'error': 'Cannot delete the last administrator.'}), 400
    db.users.delete_one({'username': username})
    logging.info(f"Auth: User '{username}' was deleted by admin '{admin_username}'.")
    return jsonify({'status': 'success', 'message': f"User '{username}' has been deleted."})