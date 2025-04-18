# File: ingest/transcript_parser.py

import json
from pathlib import Path
from db import insert_transcript_segment
from embeddings import get_embedding
from config import Config
from typing import List, Dict

def parse_transcript_file(filepath: Path) -> List[Dict]:
    """
    Parses a transcript .json3 file and extracts segments.
    Each segment includes: text, start (seconds), duration (seconds).
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            segments = []
            for event in data.get('events', []):
                if 'segs' in event:
                    text = ''.join(seg.get('utf8', '') for seg in event['segs'])
                    start = event.get('tStartMs', 0) / 1000.0
                    duration = event.get('dDurationMs', 0) / 1000.0
                    segments.append({
                        'video_id': filepath.stem,
                        'text': text.strip(),
                        'start': start,
                        'duration': duration
                    })
            return segments
    except Exception as e:
        print(f"Error parsing {filepath.name}: {e}")
        return []


def parse_and_store_segments(video_id):
    """
    Parses transcript JSON file and stores each segment with embedding into the database.
    """
    transcript_dir = Path(Config.get_transcript_dir())
    transcript_file = transcript_dir / f"{video_id}.en.json"

    if not transcript_file.exists():
        print(f"⚠️ Transcript file not found: {transcript_file}")
        return

    try:
        with open(transcript_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        events = data.get("events", [])
        inserted = 0

        for event in events:
            if 'segs' not in event:
                continue
            
            text = ''.join([seg.get("utf8", '') for seg in event.get("segs", [])]).strip()
            start_time = event.get("tStartMs", 0) / 1000.0
            duration = event.get("dDurationMs", 0) / 1000.0

            if not text:
                continue

            embedding = get_embedding(text)
            if embedding is None:
                continue

            insert_transcript_segment(video_id, start_time, duration, text, embedding)
            inserted += 1

        print(f"✅ Parsed and inserted {inserted} transcript segments for video {video_id}")

    except Exception as e:
        print(f"❌ Error processing transcript for {video_id}: {e}")