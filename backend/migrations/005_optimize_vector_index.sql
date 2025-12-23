-- Optimize vector index for 10,000+ movies
-- Switch from HNSW to IVFFlat for better storage efficiency

-- Drop existing HNSW index
DROP INDEX IF EXISTS idx_rag_movies_plot_embedding;

-- Create IVFFlat index (much smaller, optimized for < 1M vectors)
-- Lists parameter: sqrt(rows) is optimal, using 100 for 10k movies
CREATE INDEX idx_rag_movies_plot_embedding ON rag_movies 
USING ivfflat (plot_embedding vector_cosine_ops)
WITH (lists = 100);

-- Also optimize reviews index if it exists
DROP INDEX IF EXISTS idx_rag_reviews_review_embedding;

CREATE INDEX idx_rag_reviews_review_embedding ON rag_reviews
USING ivfflat (review_embedding vector_cosine_ops)
WITH (lists = 50);

-- Analyze tables to update statistics
ANALYZE rag_movies;
ANALYZE rag_reviews;
