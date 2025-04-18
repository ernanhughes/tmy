import argparse
import sys
from core.search_engine import SearchEngine  # Assumes core/search_engine.py handles embedding + search
from core.config import config  # Global config loaded from .env or default


def run_match(filename):
    print(f"\n🔍 Running match on: {filename}\n")
    searcher = SearchEngine(config)
    results = searcher.search_file(filename)

    if not results:
        print("No relevant matches found.")
        return

    for i, res in enumerate(results[:10], 1):
        print(f"{i}. 📺 {res['title']} ({res['score']*100:.1f}%)")
        print(f"   ⏱️  Timestamp: {res['timestamp']}s")
        print(f"   🔗  https://youtube.com/watch?v={res['video_id']}&t={res['timestamp']}s")
        print(f"   ✏️  Why: {res['summary']}\n")


def main():
    parser = argparse.ArgumentParser(description="Too Much YouTube CLI")
    parser.add_argument("match", help="Run search based on a session markdown file")
    parser.add_argument("filepath", help="Path to the markdown session file")
    args = parser.parse_args()

    if args.match == "match":
        run_match(args.filepath)
    else:
        print("⚠️  Unknown command. Try: python tmy.py match session.md")
        sys.exit(1)


if __name__ == "__main__":
    main()
Why is there no noise in my ****