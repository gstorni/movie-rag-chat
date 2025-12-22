-- Add actors column to rag_movies table
-- Actors stored as TEXT array for flexible querying

-- Add actors column
ALTER TABLE rag_movies ADD COLUMN IF NOT EXISTS actors TEXT[];

-- Create GIN index for efficient array searches
CREATE INDEX IF NOT EXISTS idx_rag_movies_actors ON rag_movies USING gin(actors);

-- Comment for documentation
COMMENT ON COLUMN rag_movies.actors IS 'Array of actor names in the movie';
