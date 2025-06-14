import os
import pandas as pd
import requests
from dotenv import load_dotenv

# Load API key and channel ID from .env
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Base URL for YouTube API
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"

def get_channel_stats(api_key, channel_id):
    url = f"{YOUTUBE_API_URL}/channels?part=snippet,statistics&id={channel_id}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    print("🔍 DEBUG: Channel Stats API Response ->", data)

    if "items" not in data or not data["items"]:
        raise Exception(f"API Error in channel stats: {data.get('error', data)}")

    return data["items"][0]

def get_recent_videos(api_key, channel_id, max_results=10):
    search_url = f"{YOUTUBE_API_URL}/search?key={api_key}&channelId={channel_id}&part=snippet,id&order=date&maxResults={max_results}"
    response = requests.get(search_url)
    data = response.json()
    print("🔍 DEBUG: Recent Videos API Response ->", data)

    videos = data.get("items", [])
    if not videos:
        raise Exception(f"API Error in video list: {data.get('error', data)}")

    video_data = []
    for video in videos:
        if video["id"]["kind"] == "youtube#video":
            video_data.append({
                "video_id": video["id"]["videoId"],
                "title": video["snippet"]["title"],
                "published_at": video["snippet"]["publishedAt"]
            })
    return video_data

def save_to_csv(video_data, output_path):
    df = pd.DataFrame(video_data)
    df.to_csv(output_path, index=False)
    print(f"✅ Data saved to {output_path}")

if __name__ == "__main__":
    print("📡 Fetching YouTube channel data...")

    try:
        channel_info = get_channel_stats(API_KEY, CHANNEL_ID)
        print(f"📺 Channel: {channel_info['snippet']['title']}")

        videos = get_recent_videos(API_KEY, CHANNEL_ID)
        output_path = os.path.join("data", "youtube_videos.csv")
        save_to_csv(videos, output_path)

    except Exception as e:
        print("❌ Error fetching data:", e)
