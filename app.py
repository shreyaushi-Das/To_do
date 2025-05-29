import streamlit as st
from datetime import date
from db import load_tasks, save_tasks, load_history, save_history
from ui import render_sidebar, render_add_task_form, render_task_list, render_stats_dashboard, render_calendar_view, render_history, render_bulk_ops
from utils import filter_and_sort_tasks, export_tasks, import_tasks, undo_last
from analytics import render_trend_chart, render_priority_heatmap


if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()
if "history" not in st.session_state:
    st.session_state.history = load_history()
if "undo_stack" not in st.session_state:
    st.session_state.undo_stack = []
if "bulk_selected_ids" not in st.session_state:
    st.session_state.bulk_selected_ids = set()

st.title("📝 To-Do Pro+ (Ultimate Edition)")
render_sidebar()
render_add_task_form()
render_stats_dashboard()
render_trend_chart()
render_priority_heatmap()
render_bulk_ops()
render_calendar_view()
render_task_list()
render_history()

with st.expander("⬇️⬆️ Import / Export"):
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Exported JSON", value=export_tasks(), height=150)
    with col2:
        json_input = st.text_area("Paste JSON")
        if st.button("Import"):
            if import_tasks(json_input):
                st.success("Imported successfully!")

if st.sidebar.button("Undo Last Delete"):
    undo_last()

st.markdown("---")
st.markdown("<center>Copyright TooDoo 2025</center>", unsafe_allow_html=True)