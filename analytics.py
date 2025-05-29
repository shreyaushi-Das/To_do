import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import date

def render_trend_chart():
    tasks = st.session_state.tasks
    trend_data = {}
    for t in tasks:
        if t.get("completed") and t.get("completed_on"):
            day = t["completed_on"]
            trend_data[day] = trend_data.get(day, 0) + 1
    if trend_data:
        df = pd.DataFrame({"Date": list(trend_data.keys()), "Completed": list(trend_data.values())})
        st.plotly_chart(px.line(df, x="Date", y="Completed", title="Daily Task Completions"), use_container_width=True)


def render_priority_heatmap():
    tasks = st.session_state.tasks
    heatmap_data = {
        "Date": [],
        "Priority": [],
        "Count": []
    }
    today = date.today()
    for t in tasks:
        if today <= t["deadline"] <= today + pd.Timedelta(days=14):
            heatmap_data["Date"].append(t["deadline"].strftime("%Y-%m-%d"))
            heatmap_data["Priority"].append(t["priority"])
            heatmap_data["Count"].append(1)
    if heatmap_data["Date"]:
        df = pd.DataFrame(heatmap_data)
        df = df.groupby(["Date", "Priority"]).sum().reset_index()
        st.plotly_chart(
            px.density_heatmap(df, x="Date", y="Priority", z="Count", histfunc="sum", title="Priority Heatmap (Next 2 Weeks)"),
            use_container_width=True
        )