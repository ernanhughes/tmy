# search/embeddings.py
import ollama
import numpy as np
import os
from db import insert_transcript_embedding
import json

# Function to get embeddings using Ollama
def get_embedding(text):
    try:
        embedding_data = ollama.embeddings(model="mxbai-embed-large", prompt=text)
        embedding_data = embedding_data["embedding"]  # Extract embedding
        return embedding_data
    except Exception as e:
        print(f" Unexpected error generating embedding: {e}")
    return None  # Return None if an error occurs


def embed_transcripts_from_dir():
    transcript_dir = "./transcript"
    for filename in os.listdir(transcript_dir):
        if filename.endswith(".json"):
            video_id = filename.replace(".json", "")
            transcript_path = os.path.join(transcript_dir, filename)

            try:
                with open(transcript_path, "r", encoding="utf-8") as f:
                    transcript_data = json.load(f)

                if "subtitles" not in transcript_data or not transcript_data["subtitles"]:
                    print(f"⚠️ No subtitles found in {filename}")
                    continue

                full_text = " ".join(
                    part["text"] for subtitle in transcript_data["subtitles"]
                    for part in subtitle["events"] if "text" in part
                )

                embedding = get_embedding(full_text)
                if embedding:
                    insert_transcript_embedding(video_id, embedding, full_text)
                    print(f"✅ Embedded transcript for {video_id}")
                else:
                    print(f"⚠️ Embedding failed for {video_id}")

            except Exception as e:
                print(f"❌ Error processing {filename}: {e}")
