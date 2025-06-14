import os
import pandas as pd
import snowflake.connector
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def load_csv_to_snowflake(csv_file_path):
    try:
        # Snowflake credentials
        SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
        SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
        SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
        SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
        SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
        SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
        SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")

        # Connect to Snowflake
        conn = snowflake.connector.connect(
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            account=SNOWFLAKE_ACCOUNT,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA,
            role=SNOWFLAKE_ROLE,
        )
        cursor = conn.cursor()
        print("✅ Connected to Snowflake for loading data.")

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS youtube_videos (
                video_id STRING,
                title STRING,
                published_at TIMESTAMP_NTZ
            )
        """)

        # Read data from CSV
        df = pd.read_csv(csv_file_path)

        # Insert each row into the table
        for _, row in df.iterrows():
            cursor.execute(
                """
                INSERT INTO youtube_videos (video_id, title, published_at)
                VALUES (%s, %s, %s)
                """,
                (row['video_id'], row['title'], row['published_at'])
            )

        conn.commit()
        print("✅ Data loaded successfully into Snowflake!")

    except Exception as e:
        print("❌ Error loading data into Snowflake:", e)

    finally:
        cursor.close()
        conn.close()
