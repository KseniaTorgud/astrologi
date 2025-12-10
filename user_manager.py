import json
import os
from werkzeug.security import generate_password_hash, check_password_hash

USERS_FILE = "users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}

    with open(USERS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.decoder.JSONDecodeError:
            return {}


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)


def register_user(username, password):
    users = load_users()

    if username in users:
        return False, "Такой пользователь уже существует!"

    users[username] = {
        "password": generate_password_hash(password)
    }

    save_users(users)
    return True, "Регистрация успешна!"


def login_user(username, password):
    users = load_users()

    if username not in users:
        return False, "Пользователь не найден!"

    stored_hash = users[username]["password"]
    if not check_password_hash(stored_hash, password):
        return False, "Неверный пароль!"

    return True, "Вход выполнен!"

def update_birthday(username, birthday, zodiac):
    users = load_users()
    users[username]["birthday"] = birthday
    users[username]["zodiac"] = zodiac
    save_users(users)


def get_user(username):
    users = load_users()
    return users.get(username)
