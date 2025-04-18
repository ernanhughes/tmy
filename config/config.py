import os
from dotenv import load_dotenv

load_dotenv()

def get_config():
    return {
        "transcripts_dir": os.getenv("TRANSCRIPTS_DIR", "transcripts"),
        "embedding_model": os.getenv("EMBEDDING_MODEL", "mxbai-embed-large"),
        "max_results": int(os.getenv("MAX_RESULTS", 50)),
        "channel_list_path": os.getenv("CHANNEL_LIST_PATH", "channels.txt")
    }
