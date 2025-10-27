# utils/db_utils.py

import os
import pandas as pd
from sqlalchemy import create_engine

# --- Database Connection ---
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://chat_logsdb_user:KxwkWMrzG1qgP7BEmuLPh8qTGi6hYhiU@dpg-d3pmr9ogjchc73anf1dg-a.oregon-postgres.render.com/chat_logsdb"
)

def fetch_data(query: str) -> pd.DataFrame:
    """Fetch data from PostgreSQL and return as DataFrame."""
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print(f"❌ Database fetch error: {e}")
        return pd.DataFrame()
