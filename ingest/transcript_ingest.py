# File: ingest/transcript_ingest.py

import subprocess
import json
from config import Config
from pathlib import Path
from db import insert_missing_transcript
import os


def download_transcripts_for_channels():
    """
    Downloads transcripts for all configured YouTube channel IDs.
    """
    channels = Config.get_channel_ids()
    transcript_dir = Config.get_transcript_dir()

    os.makedirs(transcript_dir, exist_ok=True)

    for channel_id in channels:
        print(f"📺 Fetching transcripts for channel: {channel_id}")
        try:
            fetch_transcripts_for_channel(channel_id, transcript_dir)
        except Exception as e:
            print(f"❌ Failed to fetch transcripts for {channel_id}: {e}")


def get_configured_channel_ids():
    """
    Retrieve a list of YouTube channel IDs from the config.
    """
    channel_ids = Config.get_channel_ids()
    if not channel_ids:
        raise ValueError("No channel IDs configured in the environment variable YOUTUBE_CHANNEL_IDS.")
    return channel_ids

def fetch_latest_video_ids(channel_id):
    """
    Use yt-dlp to fetch latest video IDs for a given channel.
    The number of results is controlled by the config.
    """
    max_results = Config.get_max_video_results()

    ytdlp_cmd = [
        "yt-dlp",
        f"https://www.youtube.com/channel/{channel_id}",
        "--flat-playlist",
        "--dump-json",
        f"--playlist-end={max_results}"
    ]

    try:
        result = subprocess.run(ytdlp_cmd, capture_output=True, text=True, check=True)
        videos = [json.loads(line) for line in result.stdout.strip().split('\n')]
        video_ids = [video['id'] for video in videos if 'id' in video]
        return video_ids
    except subprocess.CalledProcessError as e:
        print(f"Error fetching videos for channel {channel_id}: {e.stderr}")
        return []

def download_transcript(video_id):
    """
    Downloads the transcript (if available) for a given YouTube video ID using yt-dlp.
    Saves the transcript as a JSON file in the configured transcripts directory.
    """
    transcript_dir = Path(Config.get_transcript_dir())
    transcript_dir.mkdir(parents=True, exist_ok=True)
    output_path = transcript_dir / f"{video_id}.json"

    ytdlp_cmd = [
        "yt-dlp",
        f"https://www.youtube.com/watch?v={video_id}",
        "--write-subs",
        "--sub-format", "json3",
        "--skip-download",
        "--sub-lang", "en",
        "-o", str(output_path.with_suffix(''))
    ]

    try:
        subprocess.run(ytdlp_cmd, check=True, capture_output=True)
        if not output_path.exists():
            print(f"⚠️ No transcript downloaded for {video_id}. Logging...")
            insert_missing_transcript(video_id, channel_id, title)
        else:
            print(f"✅ Transcript saved for {video_id}")
        print(f"✅ Transcript saved for {video_id}")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Could not download transcript for {video_id}: {e.stderr}")
        insert_missing_transcript(video_id, channel_id, title)

# File: ingest/transcript_ingestion.py

def fetch_transcripts_for_channel(channel_id: str, output_dir: str, max_results: int = 10):
    """
    Downloads transcripts from the latest videos in a given YouTube channel.
    
    Args:
        channel_id (str): The YouTube channel ID.
        output_dir (str): Directory to save transcript files.
        max_results (int): Maximum number of videos to fetch.
    """
    try:
        print(f"🔄 Fetching up to {max_results} videos from channel: {channel_id}")
        # Construct the channel URL
        channel_url = f"https://www.youtube.com/channel/{channel_id}/videos"

        # Build the yt-dlp command
        cmd = [
            "yt-dlp",
            "--skip-download",
            "--write-auto-sub",
            "--sub-lang", "en",
            "--sub-format", "vtt",
            "--output", os.path.join(output_dir, "%(id)s.%(ext)s"),
            "--max-downloads", str(max_results),
            "--no-playlist",
            channel_url
        ]

        # Run the command
        subprocess.run(cmd, check=True)
        print("✅ Transcripts downloaded successfully.")

    except subprocess.CalledProcessError as e:
        print(f"❌ yt-dlp failed with error: {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")


# Example usage
if __name__ == "__main__":
    try:
        channels = get_configured_channel_ids()
        for channel in channels:
            print(f"\n🔍 Channel: {channel}")
            video_ids = fetch_latest_video_ids(channel)
            print(f"Found {len(video_ids)} videos: {video_ids}")
            for vid in video_ids:
                download_transcript(vid)
    except ValueError as e:
        print("Configuration Error:", e)