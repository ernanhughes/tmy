import os
from config import Config
from database.insert import insert_transcript_embedding
from search.embeddings import get_embedding

def embed_transcripts_from_dir():
    transcripts_dir =Config.get_transcript_dir()
    os.makedirs(transcripts_dir, exist_ok=True)
    print(f"🔄 Processing transcripts in: {transcripts_dir}")
    for filename in os.listdir(transcripts_dir):
        if filename.endswith(".txt"):
            file_path = os.path.join(transcripts_dir, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                embedding = get_embedding(content)
                if embedding:
                    insert_transcript_embedding(filename, content, embedding)
