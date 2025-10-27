import pandas as pd
import numpy as np

def compute_latency_metrics(df):
    if "response_time" not in df.columns or df["response_time"].isna().all():
        return 0, 0
    avg_latency = df["response_time"].mean()
    p95_latency = np.percentile(df["response_time"].dropna(), 95)
    return avg_latency, p95_latency


def compute_feedback_metrics(df):
    if "feedback" not in df.columns or df["feedback"].isna().all():
        return 0
    total = df["feedback"].count()
    positive = df["feedback"].sum() if df["feedback"].dtype == bool else 0
    return (positive / total) * 100 if total > 0 else 0