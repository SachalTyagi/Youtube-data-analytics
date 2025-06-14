from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add the scripts folder to Python path
sys.path.append('/opt/airflow/scripts')

# Import your ETL functions
from youtube_api_extract import get_channel_stats, get_recent_videos, save_to_csv
from load_to_snowflake import load_csv_to_snowflake

# Load environment variables
from dotenv import load_dotenv
load_dotenv(dotenv_path='/opt/airflow/.env')

# Env variables
API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")
CSV_FILE_PATH = '/opt/airflow/data/youtube_videos.csv'

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 6, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='youtube_etl_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='ETL pipeline to extract YouTube data and load to Snowflake',
)

def extract_transform():
    print("📡 Extracting YouTube data...")
    channel_info = get_channel_stats(API_KEY, CHANNEL_ID)
    videos = get_recent_videos(API_KEY, CHANNEL_ID)
    save_to_csv(videos, CSV_FILE_PATH)

def load_to_snowflake_task():
    load_csv_to_snowflake(CSV_FILE_PATH)

# Tasks
extract_transform_task = PythonOperator(
    task_id='extract_transform',
    python_callable=extract_transform,
    dag=dag
)

load_to_snowflake_airflow_task = PythonOperator(
    task_id='load_to_snowflake',
    python_callable=load_to_snowflake_task,
    dag=dag
)

# Task order
extract_transform_task >> load_to_snowflake_airflow_task
