import pandas as pd
import psycopg2

def get_chat_data(conn_params):
    try:
        conn = psycopg2.connect(**conn_params)
        query = """
        SELECT 
            id, session_id, , user_query, response, 
            token_count, timestamp, user_feedback
        FROM chat_logs
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print("DB Error:", e)
        return pd.DataFrame()
