import os
from dotenv import load_dotenv
from youtube_api_extract import get_channel_stats, get_recent_videos, save_to_csv
from load_to_snowflake import load_csv_to_snowflake

# Load environment variables
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def run_etl():
    print("🚀 Starting ETL process...")

    print("📡 Extracting YouTube data...")
    channel_info = get_channel_stats(API_KEY, CHANNEL_ID)
    print(f"📺 Channel: {channel_info['snippet']['title']}")

    videos = get_recent_videos(API_KEY, CHANNEL_ID)

    print("🧹 Transforming and saving data...")
    output_path = os.path.join("data", "youtube_videos.csv")
    save_to_csv(videos, output_path)

    print("📤 Loading data to Snowflake...")
    load_csv_to_snowflake(output_path)

    print("✅ ETL process completed!")

if __name__ == "__main__":
    run_etl()
