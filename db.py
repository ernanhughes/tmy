# File: db/search.py

import psycopg2
from psycopg2.extras import RealDictCursor
import numpy as np
from embeddings import get_embedding
from config import Config

# Load config
cfg = Config()

# Connect to PostgreSQL
def get_connection():
    return psycopg2.connect(
        dbname=cfg.DB_NAME,
        user=cfg.DB_USER,
        password=cfg.DB_PASSWORD,
        host=cfg.DB_HOST,
        port=cfg.DB_PORT
    )

def insert_missing_transcript(video_id, channel_id=None, title=None):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        INSERT INTO missing_transcripts (video_id, channel_id, title)
        VALUES (%s, %s, %s)
        ON CONFLICT DO NOTHING;
    """, (video_id, channel_id, title))
    conn.commit()
    cur.close()
    conn.close()

def embed_unprocessed_segments():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Step 1: Select unembedded segments
    cur.execute("""
        SELECT id, text FROM transcript_segments
        WHERE embedding IS NULL
        LIMIT %s
    """, (Config.EMBEDDING_BATCH_SIZE,))
    rows = cur.fetchall()

    if not rows:
        print("✅ No unprocessed segments found.")
        return

    print(f"🔄 Processing {len(rows)} transcript segments for embeddings...")

    for seg_id, text in rows:
        embedding = get_embedding(text)
        if embedding is not None:
            try:
                # Convert to pgvector-friendly format
                embedding_str = f"[{', '.join(map(str, embedding))}]"
                cur.execute("""
                    UPDATE transcript_segments
                    SET embedding = %s
                    WHERE id = %s
                """, (embedding_str, seg_id))
            except Exception as update_error:
                print(f"⚠️ Failed to update embedding for segment {seg_id}: {update_error}")
        else:
            print(f"⚠️ No embedding returned for segment {seg_id}")

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Embedding process complete.")


def insert_transcript_segment(video_id, start_time, text, embedding):
    """
    Insert a parsed transcript segment and its embedding into the database.
    """
    try:
        conn = get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute("""
            INSERT INTO transcript_segments (video_id, start_time, text, embedding)
            VALUES (%s, %s, %s, %s)
        """, (video_id, start_time, text, np.array(embedding).tolist()))

        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Failed to insert segment: {e}")


def search_transcripts_by_embedding(query_embedding, top_k=10):
    """
    Perform a similarity search in the transcripts table using pgvector.
    """
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    # Ensure the embedding is in the correct format for SQL
    embedding_array = np.array(query_embedding).tolist()
    embedding_str = f"[{', '.join(map(str, embedding_array))}]"

    cur.execute("""
        SELECT
            video_id,
            title,
            channel,
            published,
            url,
            summary,
            ts,
            text,
            1 - (embedding <=> %s::vector) AS similarity
        FROM transcripts
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, (embedding_str, embedding_str, top_k))

    results = cur.fetchall()
    cur.close()
    conn.close()

    return results


def insert_transcript_embedding(video_id, embedding, full_text):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cur.execute("""
            INSERT INTO transcript_embeddings (video_id, embedding, raw_text)
            VALUES (%s, %s, %s)
            ON CONFLICT (video_id) DO UPDATE
            SET embedding = EXCLUDED.embedding,
                raw_text = EXCLUDED.raw_text;
        """, (video_id, embedding, full_text))

        conn.commit()
        print(f"📝 Inserted/Updated embedding for {video_id}")
    except Exception as e:
        print(f"❌ Failed to insert embedding for {video_id}: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

