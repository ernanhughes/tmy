import os
from dotenv import load_dotenv

# Load environment variables from .env file if available
load_dotenv()

class Config:
    # Embedding Model
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "mxbai-embed-large")
    EMBEDDING_BATCH_SIZE = os.getenv("EMBEDDING_BATCH_SIZE", "50")
    # Database Config
    DB_NAME = os.getenv("DB_NAME", "tmy")
    DB_USER = os.getenv("DB_USER", "tmy")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "tmy")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")

    # Embedding Vector Dimension
    VECTOR_DIM = int(os.getenv("VECTOR_DIM", "1024"))

    # Other toggles or future options
    ENABLE_FULLTEXT_SEARCH = os.getenv("ENABLE_FULLTEXT_SEARCH", "true").lower() == "true"
    DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"


    @staticmethod
    def get_channel_ids():
        raw = os.getenv("YOUTUBE_CHANNEL_IDS", "")
        return [cid.strip() for cid in raw.split(",") if cid.strip()]
    

    @staticmethod
    def get_max_video_results():
        return int(os.getenv("MAX_VIDEO_RESULTS", "10"))  # Default to 10 if not set
    
    @staticmethod
    def get_transcript_dir():
        return os.getenv("TRANSCRIPT_DIR", "transcripts")
    
    