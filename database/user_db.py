import hashlib
import json
import os
from datetime import datetime

DATA_FILE = "database/app_users.json"

def _load_data():
    os.makedirs("database", exist_ok=True)
    if not os.path.exists(DATA_FILE):
        initial = {
            "users": {
                "admin": hashlib.sha256("pharma2026".encode()).hexdigest()
            },
            "audits": {}
        }
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(initial, f, indent=2)
        return initial
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"users": {"admin": hashlib.sha256("pharma2026".encode()).hexdigest()}, "audits": {}}

def _save_data(data):
    os.makedirs("database", exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.strip().encode()).hexdigest()

def register_user(username: str, password: str) -> tuple[bool, str]:
    username = username.strip().lower()
    password = password.strip()
    
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters long."
    if not password or len(password) < 4:
        return False, "Password must be at least 4 characters long."

    data = _load_data()
    if username in data["users"]:
        return False, f"Username '{username}' is already taken. Please log in or choose another name."

    data["users"][username] = hash_password(password)
    _save_data(data)
    return True, "Account successfully created!"

def authenticate_user(username: str, password: str) -> bool:
    username = username.strip().lower()
    password = password.strip()
    
    data = _load_data()
    if username in data["users"]:
        return data["users"][username] == hash_password(password)
    return False

def save_audit_log(username: str, filename: str, jurisdiction: str, status: str, errors_count: int):
    username = username.strip().lower()
    data = _load_data()
    
    if "audits" not in data:
        data["audits"] = {}
    if username not in data["audits"]:
        data["audits"][username] = []

    entry = {
        "Filename": filename,
        "Jurisdiction": jurisdiction,
        "Status": status,
        "Errors": errors_count,
        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data["audits"][username].insert(0, entry)
    _save_data(data)

def get_user_audits(username: str):
    username = username.strip().lower()
    data = _load_data()
    return data.get("audits", {}).get(username, [])