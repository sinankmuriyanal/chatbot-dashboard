import streamlit as st
import matplotlib.pyplot as plt

def plot_trends(df):
    if "timestamp" not in df or df.empty:
        st.info("No timestamp data for trend visualization.")
        return
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    daily = df.groupby(df["timestamp"].dt.date).size()
    fig, ax = plt.subplots()
    daily.plot(ax=ax, marker='o')
    ax.set_title("Chats Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Number of Chats")
    st.pyplot(fig)

def plot_pie_chart(metrics):
    labels = ["Positive Feedback", "Negative Feedback", "Neutral/Missing"]
    values = [metrics["user_satisfaction"], 100 - metrics["user_satisfaction"], 0]
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.set_title("User Sentiment Distribution (Dummy)")
    st.pyplot(fig)
