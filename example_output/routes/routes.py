from flask import request, jsonify
from utils.find_user_by_id import find_user_by_id
from utils.validate_user_data import validate_user_data

users = [
    {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
    {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
]

def register_routes(app):
    app.route('/')(home)
    app.route('/users', methods=['GET'])(get_users)
    app.route('/users/<int:user_id>', methods=['GET'])(get_user)
    app.route('/users', methods=['POST'])(create_user)
    app.route('/users/<int:user_id>', methods=['DELETE'])(delete_user)
    app.route('/health', methods=['GET'])(health_check)

def home():
    return jsonify({'message': 'Welcome to the User API!'})

def get_users():
    return jsonify(users)

def get_user(user_id):
    user = find_user_by_id(user_id)
    if user:
        return jsonify(user)
    else:
        return (jsonify({'error': 'User not found'}), 404)

def create_user():
    data = request.json
    is_valid, error_message = validate_user_data(data)
    if not is_valid:
        return (jsonify({'error': error_message}), 400)
    new_user = {'id': len(users) + 1, 'name': data['name'], 'email': data['email']}
    users.append(new_user)
    return (jsonify(new_user), 201)

def delete_user(user_id):
    global users
    user = find_user_by_id(user_id)
    if user:
        users = [u for u in users if u['id'] != user_id]
        return jsonify({'message': 'User deleted'})
    else:
        return (jsonify({'error': 'User not found'}), 404)

def health_check():
    return jsonify({'status': 'OK'})