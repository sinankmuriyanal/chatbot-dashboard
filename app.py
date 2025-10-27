import streamlit as st
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv
from utils.db_utils import get_chat_data
from utils.metric_utils import calculate_metrics
from utils.plot_utils import plot_trends, plot_pie_chart

# --- Load environment variables ---
load_dotenv()

st.set_page_config(page_title="LLM Chatbot Analytics", layout="wide")

# --- Database Connection ---
conn_params = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
}

# --- Load Data ---
df = get_chat_data(conn_params)
if df.empty:
    st.warning("No chat data available. Dummy metrics are displayed.")
else:
    st.success("Database connected successfully!")

# --- Calculate Metrics ---
metrics = calculate_metrics(df)

# --- Dashboard Layout ---
st.title("🤖 LLM Chatbot Analytics Dashboard")
st.markdown("Comprehensive metrics for performance, user experience, and response quality.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("🗨️ Total Chats", metrics["total_chats"])
col2.metric("💬 Total Sessions", metrics["total_sessions"])
col3.metric("🧠 Total Tokens Used", metrics["total_tokens"])
col4.metric("😊 User Satisfaction (%)", f"{metrics['user_satisfaction']}%")

col5, col6, col7, col8 = st.columns(4)
col5.metric("🎯 Accuracy (Dummy)", f"{metrics['accuracy']}%")
col6.metric("🧩 Groundedness Score", f"{metrics['groundedness']}%")
col7.metric("🕐 Avg Response Time", f"{metrics['avg_response_time']}s")
col8.metric("🗃️ Knowledge Retrieval Rate", f"{metrics['retrieval_rate']}%")

st.divider()

# --- Trend Section ---
st.subheader("📈 Chat Trends Over Time")
plot_trends(df)

# --- Feedback Distribution ---
st.subheader("📊 User Feedback Distribution")
plot_pie_chart(metrics)

# --- Data Preview ---
with st.expander("🔍 Raw Data Preview"):
    st.dataframe(df.head(20))
