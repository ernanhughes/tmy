import ollama
import numpy as np

def get_embedding(text):
    try:
        embedding_data = ollama.embeddings(model="mxbai-embed-large", prompt=text)
        return embedding_data["embedding"]
    except Exception as e:
        print(f" Unexpected error generating embedding: {e}")
    return None
