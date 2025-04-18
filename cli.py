import argparse
from embeddings.embed_transcripts import embed_transcripts_from_dir

def main():
    parser = argparse.ArgumentParser(description="Too Much YouTube CLI")

    parser.add_argument(
        "--embed-transcripts",
        action="store_true",
        help="Generate embeddings from downloaded transcript files."
    )

    args = parser.parse_args()

    if args.embed_transcripts:
        print("\n🧠 Starting transcript embedding process...\n")
        embed_transcripts_from_dir()
        print("\n✅ Embedding process completed.\n")

if __name__ == "__main__":
    main()
