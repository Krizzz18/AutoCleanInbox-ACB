import json
import os

def get_users_path():
    return os.path.join(os.getcwd(), "users.json")

def save_user(email, password):
    path = get_users_path()
    users = []
    if os.path.exists(path):
        with open(path, "r") as f:
            users = json.load(f)
    users.append({"email": email, "password": password})
    with open(path, "w") as f:
        json.dump(users, f, indent=4)

def load_users():
    path = get_users_path()
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return []
