# File: cli.py

import argparse
from embeddings.embed_transcripts import embed_transcripts_from_dir
from ingest.transcript_ingest import download_transcripts_for_channels

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

    args = parser.parse_args()

    if args.download_transcripts:
        print("\n📥 Starting transcript download process...\n")
        download_transcripts_for_channels()
        print("\n✅ Transcript download complete.\n")

    if args.embed_transcripts:
        print("\n🧠 Starting transcript embedding process...\n")
        embed_transcripts_from_dir()
        print("\n✅ Embedding process completed.\n")

if __name__ == "__main__":
    main()
