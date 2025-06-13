# monolith.py

# --- Imports ---
from flask import Flask, jsonify, request

# --- Initialize Application ---
app = Flask(__name__)

# --- Data Model ---
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

# --- Utility Functions ---
def find_user_by_id(user_id):
    for user in users:
        if user["id"] == user_id:
            return user
    return None

def validate_user_data(data):
    if "name" not in data or "email" not in data:
        return False, "Name and email are required."
    return True, None

# --- Routes ---
@app.route("/")
def home():
    return jsonify({"message": "Welcome to the User API!"})

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users)

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = find_user_by_id(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    is_valid, error_message = validate_user_data(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400

    new_user = {
        "id": len(users) + 1,
        "name": data["name"],
        "email": data["email"]
    }
    users.append(new_user)
    return jsonify(new_user), 201

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    user = find_user_by_id(user_id)
    if user:
        users = [u for u in users if u["id"] != user_id]
        return jsonify({"message": "User deleted"})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "OK"})

# --- Main Entry Point ---
if __name__ == "__main__":
    app.run(debug=True)
