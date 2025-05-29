import streamlit as st
from datetime import date, timedelta
from models import new_task
from db import save_tasks, save_history

def render_sidebar():
    st.sidebar.header("🎨 Options")
    st.sidebar.color_picker("Accent Color", value="#00b4d8")
    st.sidebar.checkbox("Dark Mode")

def render_add_task_form():
    with st.expander("➕ Add Task", expanded=True):
        with st.form("add_task", clear_on_submit=True):
            name = st.text_input("Task Name")
            col1, col2, col3 = st.columns(3)
            deadline = col1.date_input("Deadline", date.today())
            priority = col2.selectbox("Priority", ["High", "Medium", "Low"])
            recur = col3.selectbox("Recurring", ["None", "Daily", "Weekly", "Monthly"])
            desc = st.text_area("Description")
            subtasks = st.text_input("Subtasks (comma-separated)")
            if st.form_submit_button("Add Task"):
                task = new_task(name, deadline, priority, desc, recur, [s.strip() for s in subtasks.split(",") if s.strip()])
                st.session_state.tasks.append(task)
                save_tasks(st.session_state.tasks)
                st.success("Task added!")

def render_stats_dashboard():
    today = date.today()
    tasks = st.session_state.tasks
    total = len(tasks)
    completed = sum(t["completed"] for t in tasks)
    overdue = sum(1 for t in tasks if not t["completed"] and t["deadline"] < today)
    upcoming = sum(1 for t in tasks if (0 < (t["deadline"] - today).days <= 7) and not t["completed"])
    st.write(f"**Total:** {total} | **Completed:** {completed} | **Overdue:** {overdue} | **Upcoming:** {upcoming}")
    if total:
        st.progress(completed / total)

def render_bulk_ops():
    with st.expander("🗂️ Bulk Ops"):
        for t in st.session_state.tasks:
            if st.checkbox(f"{t['name']} - {t['deadline']}", key=f"bulk_{t['id']}"):
                st.session_state.bulk_selected_ids.add(t['id'])
            else:
                st.session_state.bulk_selected_ids.discard(t['id'])
        if st.button("Bulk Delete"):
            removed = []
            for tid in list(st.session_state.bulk_selected_ids):
                task = next((x for x in st.session_state.tasks if x["id"] == tid), None)
                if task:
                    st.session_state.tasks.remove(task)
                    removed.append(task)
            st.session_state.history.extend(removed)
            save_tasks(st.session_state.tasks)
            save_history(st.session_state.history)
            st.session_state.bulk_selected_ids.clear()
            st.success("Deleted selected tasks.")

def render_calendar_view():
    with st.expander("📅 Calendar View"):
        calendar = {}
        today = date.today()
        for t in st.session_state.tasks:
            if today <= t["deadline"] < today + timedelta(days=30):
                calendar.setdefault(t["deadline"], []).append(t["name"])
        rows = [{"Date": k, "Tasks": ", ".join(v)} for k, v in calendar.items()]
        if rows:
            import pandas as pd
            st.dataframe(pd.DataFrame(rows))
        else:
            st.info("No tasks in next 30 days.")

def render_task_list():
    st.subheader("📝 Task List")
    for t in st.session_state.tasks:
        col1, col2, col3 = st.columns([0.1, 0.6, 0.3])
        with col1:
            if st.button("✅" if t["completed"] else "⬜", key=f"toggle_{t['id']}"):
                t["completed"] = not t["completed"]
                if t["completed"]:
                    t["completed_on"] = date.today().isoformat()
                    st.session_state.history.append(t.copy())
                else:
                    t["completed_on"] = None
                save_tasks(st.session_state.tasks)
                save_history(st.session_state.history)
                st.rerun()

        with col2:
            st.markdown(f"**{t['name']}** — {t['priority']} — {t['deadline']}")
            if t.get("subtasks"):
                for s in t["subtasks"]:
                    st.markdown(f"- {s}")
            if t.get("description"):
                st.caption(t["description"])
        with col3:
            if st.button("❌", key=f"del_{t['id']}"):
                st.session_state.tasks.remove(t)
                st.session_state.history.append(t)
                save_tasks(st.session_state.tasks)
                save_history(st.session_state.history)
                st.rerun()


def render_history():
    with st.expander("🕓 History"):
        import pandas as pd
        if st.session_state.history:
            df = pd.DataFrame(st.session_state.history)
            st.dataframe(df.fillna("-"))
        else:
            st.info("No history yet.")
