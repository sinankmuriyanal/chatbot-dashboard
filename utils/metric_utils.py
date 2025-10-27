import numpy as np

def calculate_metrics(df):
    if df.empty:
        # Dummy values for now
        return {
            "total_chats": 123,
            "total_sessions": 45,
            "total_tokens": 98765,
            "user_satisfaction": 34,
            "accuracy": 35,
            "groundedness": 56,
            "avg_response_time": 1.4,
            "retrieval_rate": 88,
        }

    metrics = {}
    metrics["total_chats"] = len(df)
    metrics["total_sessions"] = df["session_id"].nunique()
    metrics["total_tokens"] = df["token_count"].sum() if "token_count" in df else 0
    metrics["user_satisfaction"] = (
        df["user_feedback"].mean() * 100 if "user_feedback" in df and df["user_feedback"].notnull().any() else 34
    )
    
    # Industry-related dummy metrics (replace with real model evaluation later)
    metrics["accuracy"] = 78  # Placeholder for correctness/faithfulness check
    metrics["groundedness"] = 46  # Measures factual grounding to retrieved context
    metrics["avg_response_time"] = 1.4  # Placeholder
    metrics["retrieval_rate"] = 88  # Placeholder for % of responses using RAG context
    
    return metrics
