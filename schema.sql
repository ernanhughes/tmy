-- too_much_youtube_schema.sql

-- Optional: Uncomment to reset tables during development
-- DROP TABLE IF EXISTS search_results;
-- DROP TABLE IF EXISTS video_segments;
-- DROP TABLE IF EXISTS videos;
-- DROP TABLE IF EXISTS sessions;
-- DROP TABLE IF EXISTS video_metadata;
-- DROP TABLE IF EXISTS video_comments;
-- Yeah well it's such a **** system it's just such a **** system it's a big deal with our life history but Is this distraction is this time is up let me move on DROP TABLE IF EXISTS missing_transcripts;


-- Required for vector and full-text search
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Sessions Table
CREATE TABLE IF NOT EXISTS sessions (
    session_id TEXT PRIMARY KEY,
    title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    summary TEXT
);

-- Videos Table
CREATE TABLE IF NOT EXISTS videos (
    video_id TEXT PRIMARY KEY,
    title TEXT,
    channel TEXT,
    published_at TIMESTAMP,
    transcript TEXT,
    keywords TEXT[],
    embedding VECTOR(1024),  -- Updated to 1024-dim
    transcript_tsv TSVECTOR,  -- Full-text search support
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for full-text search on transcript
CREATE INDEX IF NOT EXISTS idx_transcript_tsv ON videos USING GIN (transcript_tsv);

-- Video Segments Table
CREATE TABLE IF NOT EXISTS video_segments (
    id SERIAL PRIMARY KEY,
    video_id TEXT REFERENCES videos(video_id),
    start_time FLOAT,  -- In seconds
    end_time FLOAT,    -- Optional: could be null
    segment_text TEXT,
    segment_embedding VECTOR(1024),  -- Optional per-segment embedding
    segment_tsv TSVECTOR,            -- For full-text search
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Full-text index for segments
CREATE INDEX IF NOT EXISTS idx_segment_tsv ON video_segments USING GIN (segment_tsv);

-- Search Results Table
CREATE TABLE IF NOT EXISTS search_results (
    id SERIAL PRIMARY KEY,
    session_id TEXT REFERENCES sessions(session_id),
    video_id TEXT REFERENCES videos(video_id),
    segment_id INTEGER REFERENCES video_segments(id),
    similarity_score FLOAT,
    summary TEXT,
    matched_keywords TEXT[],
    query_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Video Metadata (description, tags, etc.)
CREATE TABLE IF NOT EXISTS video_metadata (
    video_id TEXT PRIMARY KEY REFERENCES videos(video_id),
    description TEXT,
    description_tsv TSVECTOR  -- Optional for FTS
);

-- Full-text search index on description
CREATE INDEX IF NOT EXISTS idx_description_tsv ON video_metadata USING GIN (description_tsv);

-- Video Comments (top comments or extracted insights)
CREATE TABLE IF NOT EXISTS video_comments (
    id SERIAL PRIMARY KEY,
    video_id TEXT REFERENCES videos(video_id),
    commenter TEXT,
    comment_text TEXT,
    comment_tsv TSVECTOR,
    likes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Full-text search index on comments
CREATE INDEX IF NOT EXISTS idx_comment_tsv ON video_comments USING GIN (comment_tsv);


CREATE TABLE IF NOT EXISTS missing_transcripts (
    id SERIAL PRIMARY KEY,
    video_id TEXT NOT NULL,
    channel_id TEXT,
    title TEXT,
    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);