from datetime import date, timedelta
import uuid

def new_task(name, deadline, priority, description, recur, subtasks, tags=None):
    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "completed": False,
        "deadline": deadline,
        "priority": priority,
        "description": description,
        "recurring": recur,
        "subtasks": subtasks or [],
        "created": date.today().isoformat(),
        "completed_on": None,
        "tags": tags or []
    }

def recurring_next_date(deadline, recur):
    if recur == "Daily":
        return deadline + timedelta(days=1)
    if recur == "Weekly":
        return deadline + timedelta(weeks=1)
    if recur == "Monthly":
        return deadline + timedelta(days=30)
    return None