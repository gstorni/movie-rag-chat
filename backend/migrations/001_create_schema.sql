-- RAG Experiment Database Schema
-- Creates tables for movie database with pgvector support

-- Enable pgvector extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS vector;

-- Movies table with vector embedding for plot
CREATE TABLE IF NOT EXISTS rag_movies (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    year INTEGER NOT NULL,
    director TEXT NOT NULL,
    genre TEXT NOT NULL,
    plot TEXT NOT NULL,
    rating DECIMAL(3,1) NOT NULL CHECK (rating >= 0 AND rating <= 10),
    runtime_minutes INTEGER,
    plot_embedding vector(1536),  -- OpenAI text-embedding-3-small dimensions
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Reviews table with vector embedding
CREATE TABLE IF NOT EXISTS rag_reviews (
    id SERIAL PRIMARY KEY,
    movie_id INTEGER NOT NULL REFERENCES rag_movies(id) ON DELETE CASCADE,
    reviewer_name TEXT NOT NULL,
    review_text TEXT NOT NULL,
    rating DECIMAL(3,1) NOT NULL CHECK (rating >= 0 AND rating <= 10),
    review_date DATE NOT NULL DEFAULT CURRENT_DATE,
    review_embedding vector(1536),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for efficient searching
CREATE INDEX IF NOT EXISTS idx_rag_movies_year ON rag_movies(year);
CREATE INDEX IF NOT EXISTS idx_rag_movies_director ON rag_movies(director);
CREATE INDEX IF NOT EXISTS idx_rag_movies_genre ON rag_movies(genre);
CREATE INDEX IF NOT EXISTS idx_rag_movies_rating ON rag_movies(rating DESC);
CREATE INDEX IF NOT EXISTS idx_rag_reviews_movie_id ON rag_reviews(movie_id);

-- Vector indexes for similarity search (using IVFFlat for better performance)
-- Note: These indexes work best with at least 1000+ rows
-- For smaller datasets, sequential scan is used automatically
CREATE INDEX IF NOT EXISTS idx_rag_movies_plot_embedding ON rag_movies
    USING ivfflat (plot_embedding vector_cosine_ops) WITH (lists = 10);

CREATE INDEX IF NOT EXISTS idx_rag_reviews_embedding ON rag_reviews
    USING ivfflat (review_embedding vector_cosine_ops) WITH (lists = 10);

-- Full text search index on plot
CREATE INDEX IF NOT EXISTS idx_rag_movies_plot_fts ON rag_movies
    USING gin(to_tsvector('english', plot));

COMMENT ON TABLE rag_movies IS 'Movie database for RAG experiment';
COMMENT ON TABLE rag_reviews IS 'Movie reviews for RAG experiment';
COMMENT ON COLUMN rag_movies.plot_embedding IS 'OpenAI text-embedding-3-small vector (1536 dimensions)';
