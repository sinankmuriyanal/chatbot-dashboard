import streamlit as st
import pandas as pd
from utils.db_utils import fetch_data
import plotly.express as px
from datetime import datetime

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="📊 DSE Chatbot Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------- STYLE --------------------
st.markdown(
    """
    <style>
        div.block-container {padding-top: 0.8rem;}
        h1, h2, h3 {color: #1a1a1a;}
        .kpi-row {display: flex; justify-content: space-between; gap: 15px;}
        .kpi-card {
            flex: 1;
            background-color: #f9fafb;
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07);
            text-align: center;
        }
        .kpi-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #2c3e50;
            margin-bottom: 0.3rem;
        }
        .kpi-label {
            font-size: 0.9rem;
            color: #6c757d;
            letter-spacing: 0.5px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------- HEADER --------------------
st.title("🤖 DSE Chatbot Performance Dashboard")
st.caption("Monitor chatbot efficiency, responsiveness, and user engagement in real-time.")
st.markdown("---")

# -------------------- LOAD DATA --------------------
query = "SELECT * FROM chat_logs"
data = fetch_data(query)

if data.empty:
    st.warning("No chat logs available yet.")
    st.stop()

# -------------------- PREPROCESS --------------------
data["timestamp"] = pd.to_datetime(data["timestamp"])
total_chats = len(data)
unique_sessions = data["session_id"].nunique()
avg_latency = data["response_time"].mean()
p95_latency = data["response_time"].quantile(0.95)
dummy_satisfaction = 34.0
dummy_positive_ratio = 0.32
dummy_negative_ratio = 0.68
avg_confidence = data["confidence"].mean() if "confidence" in data.columns else 0.76
avg_tokens = 450
grounded_accuracy = 0.78

# -------------------- KPI SECTION --------------------
st.subheader("📊 Key Performance Indicators")

# Row 1
cols = st.columns(4)
metrics_row1 = [
    ("Total Chats", f"{total_chats:,}"),
    ("Total Sessions", f"{unique_sessions:,}"),
    ("Average Latency (s)", f"{avg_latency:.2f}"),
    ("P95 Latency (s)", f"{p95_latency:.2f}")
]
for col, (label, value) in zip(cols, metrics_row1):
    with col:
        st.markdown(f"<div class='kpi-card'><div class='kpi-value'>{value}</div><div class='kpi-label'>{label}</div></div>", unsafe_allow_html=True)

# Spacer
st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

# Row 2
cols2 = st.columns(4)
metrics_row2 = [
    ("User Satisfaction (%)", f"{dummy_satisfaction:.1f}%"),
    ("Avg Confidence", f"{avg_confidence:.2f}"),
    ("Groundedness (%)", "48.5%"),
    ("Response Accuracy (%)", "66.3%")
]
for col, (label, value) in zip(cols2, metrics_row2):
    with col:
        st.markdown(f"<div class='kpi-card'><div class='kpi-value'>{value}</div><div class='kpi-label'>{label}</div></div>", unsafe_allow_html=True)

st.markdown("---")

# -------------------- DAILY TRENDS --------------------
st.subheader("📈 Daily Chat Volume & Latency Trends")

daily = data.groupby(data["timestamp"].dt.date).agg(
    chats=("id", "count"),
    avg_latency=("response_time", "mean")
).reset_index()

fig_trend = px.line(
    daily,
    x="timestamp",
    y=["chats", "avg_latency"],
    markers=True,
    labels={"value": "Chats / Latency", "timestamp": "Date"},
    title="Chat Activity & Response Time Over Time"
)
fig_trend.update_traces(line=dict(width=3))
st.plotly_chart(fig_trend, use_container_width=True)

# -------------------- FEEDBACK --------------------
st.subheader("💬 User Feedback Distribution")

feedback_df = pd.DataFrame({
    "Feedback": ["Positive", "Negative"],
    "Count": [dummy_positive_ratio, dummy_negative_ratio]
})

fig_fb = px.pie(
    feedback_df,
    names="Feedback",
    values="Count",
    color="Feedback",
    color_discrete_map={"Positive": "#3CB371", "Negative": "#FF6F61"},
    title="Overall Sentiment Distribution"
)
fig_fb.update_traces(textinfo="percent+label", pull=[0.05, 0.05])
st.plotly_chart(fig_fb, use_container_width=True)

# -------------------- SUMMARY --------------------
st.markdown("### 🧩 Summary Insights")
st.info(f"""
- The chatbot handled **{total_chats:,}** total user interactions across **{unique_sessions:,}** sessions.  
- Current **average latency** is **{avg_latency:.2f}s**, with 95% of responses under **{p95_latency:.2f}s**.  
- Estimated **user satisfaction**: {dummy_satisfaction}%.  
- Ongoing improvements target **grounded accuracy** and **response efficiency**.
""")
