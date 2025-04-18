import psycopg2
import numpy as np

def insert_transcript_embedding(filename, content, embedding):
    try:
        conn = psycopg2.connect(
            dbname="tmy", user="tmy", password="tmy", host="localhost"
        )
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO transcripts (video_id, transcript_text, embedding)
            VALUES (%s, %s, %s)
            ON CONFLICT (video_id) DO NOTHING;
        """, (filename, content, np.array(embedding)))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error inserting transcript embedding: {e}")


def insert_video_segment(video_id, start_time, end_time, segment_text, segment_embedding=None):
    try:
        conn = psycopg2.connect(
            dbname="tmy", user="tmy", password="tmy", host="localhost"
        )
        cursor = conn.cursor()

        # Generate full-text search vector (tsvector) from text
        query = """
            INSERT INTO video_segments (
                video_id, start_time, end_time, segment_text,
                segment_embedding, segment_tsv
            )
            VALUES (%s, %s, %s, %s, %s, to_tsvector('english', %s))
        """
        cursor.execute(query, (
            video_id,
            start_time,
            end_time,
            segment_text,
            segment_embedding,
            segment_text
        ))

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error inserting video segment: {e}")
