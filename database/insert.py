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
