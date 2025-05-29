from datetime import date
import json
from db import save_tasks, save_history
import streamlit as st

def export_tasks():
    export_list = []
    for t in st.session_state.tasks:
        t_copy = t.copy()
        if hasattr(t_copy["deadline"], "isoformat"):
            t_copy["deadline"] = t_copy["deadline"].isoformat()
        export_list.append(t_copy)
    return json.dumps(export_list, indent=2)

def import_tasks(json_str):
    try:
        tasks = json.loads(json_str)
        for t in tasks:
            t["deadline"] = date.fromisoformat(t["deadline"])
        st.session_state.tasks = tasks
        save_tasks(tasks)
        return True
    except Exception as e:
        st.error(f"Import error: {e}")
        return False


def undo_last():
    if not st.session_state.undo_stack:
        st.warning("Nothing to undo.")
        return

    op = st.session_state.undo_stack.pop()

    if op[0] == "delete":
        _, task, index = op
        st.session_state.tasks.insert(index, task)
        st.session_state.history = [h for h in st.session_state.history if h["id"] != task["id"]]
        st.success(f"Undo: Restored '{task['name']}'")

    elif op[0] == "bulk_delete":
        _, removed_tasks = op
        for index, task in sorted(removed_tasks, key=lambda x: x[0]):
            st.session_state.tasks.insert(index, task)
        removed_ids = {task['id'] for _, task in removed_tasks}
        st.session_state.history = [h for h in st.session_state.history if h["id"] not in removed_ids]
        st.success(f"Undo: Restored {len(removed_ids)} tasks.")

    save_tasks(st.session_state.tasks)
    save_history(st.session_state.history)

def filter_and_sort_tasks(tasks, search_query, filter_option, sort_option):
    today = date.today()
    if search_query:
        tasks = [t for t in tasks if search_query.lower() in t["name"].lower() or search_query.lower() in t.get("description", "")]

    if filter_option == "Active":
        tasks = [t for t in tasks if not t["completed"] and (t["deadline"] >= today)]
    elif filter_option == "Completed":
        tasks = [t for t in tasks if t["completed"]]
    elif filter_option == "Overdue":
        tasks = [t for t in tasks if not t["completed"] and (t["deadline"] < today)]
    elif filter_option == "Today":
        tasks = [t for t in tasks if t["deadline"] == today]
    elif filter_option == "Upcoming":
        tasks = [t for t in tasks if (0 < (t["deadline"] - today).days <= 7) and not t["completed"]]

    if sort_option == "Deadline":
        tasks = sorted(tasks, key=lambda t: (t["deadline"], t["priority"]))
    elif sort_option == "Name":
        tasks = sorted(tasks, key=lambda t: t["name"].lower())
    elif sort_option == "Priority":
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        tasks = sorted(tasks, key=lambda t: priority_order[t["priority"]])

    return tasks