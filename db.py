import shelve

DB_NAME = "tasks.db"

def load_tasks():
    with shelve.open(DB_NAME) as db:
        return db.get("tasks", [])

def save_tasks(tasks):
    with shelve.open(DB_NAME) as db:
        db["tasks"] = tasks

def load_history():
    with shelve.open(DB_NAME) as db:
        return db.get("history", [])

def save_history(history):
    with shelve.open(DB_NAME) as db:
        db["history"] = history