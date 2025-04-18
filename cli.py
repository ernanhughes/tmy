# File: cli.py

import argparse
from embeddings.embed_transcripts import embed_transcripts_from_dir
from ingest.transcript_ingest import download_transcripts_for_channels

import os
from config import Config
from ingest.parse_transcripts import process_transcript_file
from database.insert import insert_transcript_embedding
from search.embeddings import get_embedding

def import_transcripts(embed=False):
    transcript_dir = Config.get_transcript_dir()

    if not os.path.exists(transcript_dir):
        print(f"❌ Transcript directory not found: {transcript_dir}")
        return

    print(f"📂 Importing transcripts from: {transcript_dir}")
    for filename in os.listdir(transcript_dir):
        if filename.endswith(".vtt"):
            full_path = os.path.join(transcript_dir, filename)
            print(f"📄 Parsing: {filename}")
            segments = process_transcript_file(full_path)

            for segment in segments:
                embedding = get_embedding(segment["text"]) if embed else None
                insert_transcript_embedding(
                    video_id=segment["video_id"],
                    start_time=segment["start"],
                    end_time=segment["end"],
                    text=segment["text"],
                    embedding=embedding
                )
            print(f"✅ Imported {len(segments)} segments from {filename}")


def main():
    parser = argparse.ArgumentParser(description="Too Much YouTube CLI")

    parser.add_argument(
        "--embed-transcripts",
        action="store_true",
        help="Generate embeddings from downloaded transcript files."
    )

    parser.add_argument(
        "--download-transcripts",
        action="store_true",
        help="Download transcripts for configured channels."
    )

    parser.add_argument("--import-transcripts", action="store_true", help="Import parsed transcripts into the database")
    
    args = parser.parse_args()

    if args.download_transcripts:
        print("\n📥 Starting transcript download process...\n")
        download_transcripts_for_channels()
        print("\n✅ Transcript download complete.\n")

    if args.import_transcripts:
        print("\n📥 Starting transcript import process...\n")
        import_transcripts(embed=True)
        print("\n✅ Transcript import complete.\n")

    if args.embed_transcripts:
        print("\n🧠 Starting transcript embedding process...\n")
        embed_transcripts_from_dir()
        print("\n✅ Embedding process completed.\n")

if __name__ == "__main__":
    main()
