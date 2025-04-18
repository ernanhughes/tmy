# File: ingest/parse_transcripts.py

import json
import os
from pathlib import Path
from config import Config
from db import insert_transcript_segment
from embeddings import get_embedding

def load_transcript(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

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
    try:
        transcript_data = load_transcript(file_path)
        segments = parse_segments(transcript_data)
        for start_time, text in segments:
            embedding = get_embedding(text)
            if embedding:
                insert_transcript_segment(video_id, start_time, text, embedding)
    except Exception as e:
        print(f"⚠️ Failed to process {file_path}: {e}")

def process_all_transcripts():
    transcript_dir = Path(Config.get_transcript_dir())
    for file in transcript_dir.glob("*.json"):
        print(f"📄 Processing {file.name}")
        process_transcript_file(file)

if __name__ == "__main__":
    process_all_transcripts()
