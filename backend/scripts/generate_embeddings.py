"""
Script to generate embeddings for all movies and reviews.
Run this after inserting mock data to enable vector search.
"""

import sys
import time
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config
from utils.database import get_cursor, execute_query
from services.embedding_service import generate_embeddings_batch


def get_movies_without_embeddings():
    """Fetch movies that don't have embeddings yet."""
    sql = """
        SELECT id, title, plot
        FROM rag_movies
        WHERE plot_embedding IS NULL
        ORDER BY id
    """
    return execute_query(sql)


def get_reviews_without_embeddings():
    """Fetch reviews that don't have embeddings yet."""
    sql = """
        SELECT id, review_text
        FROM rag_reviews
        WHERE review_embedding IS NULL
        ORDER BY id
    """
    return execute_query(sql)


def update_movie_embedding(movie_id: int, embedding: list):
    """Update a movie's embedding."""
    embedding_str = '[' + ','.join(map(str, embedding)) + ']'
    sql = "UPDATE rag_movies SET plot_embedding = %s::vector WHERE id = %s"

    with get_cursor() as cursor:
        cursor.execute(sql, (embedding_str, movie_id))


def update_review_embedding(review_id: int, embedding: list):
    """Update a review's embedding."""
    embedding_str = '[' + ','.join(map(str, embedding)) + ']'
    sql = "UPDATE rag_reviews SET review_embedding = %s::vector WHERE id = %s"

    with get_cursor() as cursor:
        cursor.execute(sql, (embedding_str, review_id))


def process_movies_batch(movies: list, batch_size: int = 10):
    """Process movies in batches to avoid rate limits."""
    total = len(movies)
    processed = 0

    for i in range(0, total, batch_size):
        batch = movies[i:i + batch_size]

        # Prepare texts for embedding
        texts = [f"Movie: {m['title']}. Plot: {m['plot']}" for m in batch]

        try:
            # Generate embeddings for batch
            embeddings = generate_embeddings_batch(texts)

            # Update each movie
            for j, movie in enumerate(batch):
                update_movie_embedding(movie['id'], embeddings[j])
                processed += 1
                print(f"  [{processed}/{total}] Embedded: {movie['title']}")

            # Rate limit protection
            if i + batch_size < total:
                time.sleep(0.5)

        except Exception as e:
            print(f"Error processing batch starting at {i}: {e}")
            # Try one by one on error
            for movie in batch:
                try:
                    text = f"Movie: {movie['title']}. Plot: {movie['plot']}"
                    embedding = generate_embeddings_batch([text])[0]
                    update_movie_embedding(movie['id'], embedding)
                    processed += 1
                    print(f"  [{processed}/{total}] Embedded (retry): {movie['title']}")
                    time.sleep(0.2)
                except Exception as e2:
                    print(f"  Failed to embed {movie['title']}: {e2}")


def process_reviews_batch(reviews: list, batch_size: int = 10):
    """Process reviews in batches."""
    total = len(reviews)
    processed = 0

    for i in range(0, total, batch_size):
        batch = reviews[i:i + batch_size]

        texts = [r['review_text'] for r in batch]

        try:
            embeddings = generate_embeddings_batch(texts)

            for j, review in enumerate(batch):
                update_review_embedding(review['id'], embeddings[j])
                processed += 1
                print(f"  [{processed}/{total}] Embedded review ID: {review['id']}")

            if i + batch_size < total:
                time.sleep(0.5)

        except Exception as e:
            print(f"Error processing reviews batch: {e}")


def main():
    """Main function to generate all embeddings."""
    print("=" * 50)
    print("EMBEDDING GENERATION SCRIPT")
    print("=" * 50)

    if not config.OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY not found in environment")
        return

    # Process movies
    print("\n[1/2] Processing Movies...")
    movies = get_movies_without_embeddings()

    if movies:
        print(f"Found {len(movies)} movies without embeddings")
        process_movies_batch(movies)
    else:
        print("All movies already have embeddings")

    # Process reviews
    print("\n[2/2] Processing Reviews...")
    reviews = get_reviews_without_embeddings()

    if reviews:
        print(f"Found {len(reviews)} reviews without embeddings")
        process_reviews_batch(reviews)
    else:
        print("All reviews already have embeddings")

    print("\n" + "=" * 50)
    print("EMBEDDING GENERATION COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    main()
