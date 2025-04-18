import os
from config.config import get_config
from database.insert import insert_transcript_embedding
from search.embeddings import get_embedding

def embed_transcripts_from_dir():
    config = get_config()
    transcripts_dir = config["transcripts_dir"]

    for filename in os.listdir(transcripts_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(transcripts_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                embedding = get_embedding(content)
                if embedding:
                    insert_transcript_embedding(filename, content, embedding)
