# File: ingest/parse_transcripts.py

import json
import os
from pathlib import Path
from config import Config
from database.insert import insert_video_segment
from search.embeddings import get_embedding

def load_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)
    

def load_vtt_as_text(file_path):
    lines = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if "-->" not in line and not line.startswith("WEBVTT") and not line.strip().isdigit() and line.strip():
                lines.append(line.strip())
    return " ".join(lines)


def parse_segments(transcript_json):
    segments = []
    events = transcript_json.get("events", [])
    for event in events:
        if "segs" in event and "tStartMs" in event:
            start_time = int(event["tStartMs"]) / 1000  # convert to seconds
            text = ''.join(seg.get("utf8", "") for seg in event["segs"]).strip()
            if text:
                segments.append((start_time, text))
    return segments

def process_transcript_file(file_path):
    video_id = Path(file_path).stem
    print(f"🔍 Processing transcript for video ID: {video_id}")
    try:
        transcript_data = load_vtt_as_text(file_path)
        print(f"📜 Loaded transcript data for {video_id}")
        segments = parse_segments(transcript_data)
        print(f"📝 Parsed {len(segments)} segments for {video_id}")
        for start_time, text in segments:
            embedding = get_embedding(text)
            if embedding:
                insert_video_segment(video_id, start_time, text, embedding)
    except Exception as e:
        print(f"⚠️ Failed to process {file_path}: {e}")

def process_all_transcripts():
    transcript_dir = Path(Config.get_transcript_dir())
    for file in transcript_dir.glob("*.json"):
        print(f"📄 Processing {file.name}")
        process_transcript_file(file)

if __name__ == "__main__":
    process_all_transcripts()
