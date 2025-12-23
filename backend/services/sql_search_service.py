"""
SQL search service for structured database queries.
Handles filtering, aggregations, and exact matches.
"""

from typing import List, Dict, Any, Optional
import sys
sys.path.append('..')
from utils.database import execute_query


def get_movies_by_year(year: int) -> List[Dict[str, Any]]:
    """Get all movies from a specific year."""
    sql = """
        SELECT id, title, year, director, genre, plot, rating, runtime_minutes, actors
        FROM rag_movies
        WHERE year = %s
        ORDER BY rating DESC
    """
    results = execute_query(sql, (year,))
    return [dict(row) for row in results] if results else []


def get_movies_by_director(director: str) -> List[Dict[str, Any]]:
    """Get all movies by a specific director (case-insensitive partial match)."""
    sql = """
        SELECT id, title, year, director, genre, plot, rating, runtime_minutes, actors
        FROM rag_movies
        WHERE LOWER(director) LIKE LOWER(%s)
        ORDER BY year DESC
    """
    results = execute_query(sql, (f'%{director}%',))
    return [dict(row) for row in results] if results else []


def get_movies_by_genre(genre: str) -> List[Dict[str, Any]]:
    """Get all movies of a specific genre (case-insensitive partial match)."""
    sql = """
        SELECT id, title, year, director, genre, plot, rating, runtime_minutes, actors
        FROM rag_movies
        WHERE LOWER(genre) LIKE LOWER(%s)
        ORDER BY rating DESC
    """
    results = execute_query(sql, (f'%{genre}%',))
    return [dict(row) for row in results] if results else []


def get_movies_by_actor(actor: str) -> List[Dict[str, Any]]:
    """Get all movies featuring a specific actor (case-insensitive partial match)."""
    sql = """
        SELECT id, title, year, director, genre, plot, rating, runtime_minutes, actors
        FROM rag_movies
        WHERE EXISTS (
            SELECT 1 FROM unnest(actors) AS a
            WHERE LOWER(a) LIKE LOWER(%s)
        )
        ORDER BY rating DESC
    """
    results = execute_query(sql, (f'%{actor}%',))
    return [dict(row) for row in results] if results else []


def get_top_rated_movies(limit: int = 10) -> List[Dict[str, Any]]:
    """Get the highest rated movies."""
    sql = """
        SELECT id, title, year, director, genre, plot, rating, runtime_minutes, actors
        FROM rag_movies
        ORDER BY rating DESC
        LIMIT %s
    """
    results = execute_query(sql, (limit,))
    return [dict(row) for row in results] if results else []


def get_movies_by_rating_range(min_rating: float, max_rating: float = 10.0) -> List[Dict[str, Any]]:
    """Get movies within a rating range."""
    sql = """
        SELECT id, title, year, director, genre, plot, rating, runtime_minutes, actors
        FROM rag_movies
        WHERE rating >= %s AND rating <= %s
        ORDER BY rating DESC
    """
    results = execute_query(sql, (min_rating, max_rating))
    return [dict(row) for row in results] if results else []


def get_movie_with_reviews(movie_id: int) -> Optional[Dict[str, Any]]:
    """Get a movie with all its reviews."""
    movie_sql = """
        SELECT id, title, year, director, genre, plot, rating, runtime_minutes, actors
        FROM rag_movies
        WHERE id = %s
    """
    reviews_sql = """
        SELECT id, reviewer_name, review_text, rating, review_date
        FROM rag_reviews
        WHERE movie_id = %s
        ORDER BY review_date DESC
    """

    movies = execute_query(movie_sql, (movie_id,))
    if not movies:
        return None

    movie = dict(movies[0])
    reviews = execute_query(reviews_sql, (movie_id,))
    movie['reviews'] = [dict(r) for r in reviews] if reviews else []

    return movie


def search_movies_keyword(keyword: str) -> List[Dict[str, Any]]:
    """Search movies by keyword in title or plot."""
    sql = """
        SELECT id, title, year, director, genre, plot, rating, runtime_minutes, actors
        FROM rag_movies
        WHERE LOWER(title) LIKE LOWER(%s) OR LOWER(plot) LIKE LOWER(%s)
        ORDER BY rating DESC
    """
    pattern = f'%{keyword}%'
    results = execute_query(sql, (pattern, pattern))
    return [dict(row) for row in results] if results else []


def get_statistics() -> Dict[str, Any]:
    """Get basic database statistics."""
    sql = """
        SELECT
            COUNT(*) as total_movies,
            AVG(rating) as avg_rating,
            MIN(year) as earliest_year,
            MAX(year) as latest_year,
            COUNT(DISTINCT director) as unique_directors,
            COUNT(DISTINCT genre) as unique_genres,
            (SELECT COUNT(DISTINCT reviewer_name) FROM rag_reviews) as unique_reviewers,
            (SELECT COUNT(DISTINCT a) FROM rag_movies, unnest(actors) AS a) as unique_actors
        FROM rag_movies
    """
    results = execute_query(sql)
    return dict(results[0]) if results else {}


def get_detailed_statistics() -> Dict[str, Any]:
    """Get comprehensive database and vector statistics (cached in Redis for 1 hour)."""
    from services.redis_cache import get_cached_stats, cache_stats

    # Check cache first
    cached = get_cached_stats()
    if cached is not None:
        return cached

    stats = {}

    # Basic movie stats
    basic_sql = """
        SELECT
            COUNT(*) as total_movies,
            ROUND(AVG(rating)::numeric, 2) as avg_rating,
            ROUND(MIN(rating)::numeric, 2) as min_rating,
            ROUND(MAX(rating)::numeric, 2) as max_rating,
            ROUND(STDDEV(rating)::numeric, 2) as rating_stddev,
            MIN(year) as earliest_year,
            MAX(year) as latest_year,
            COUNT(DISTINCT director) as unique_directors,
            COUNT(DISTINCT genre) as unique_genres,
            ROUND(AVG(runtime_minutes)::numeric, 0) as avg_runtime,
            MIN(runtime_minutes) as min_runtime,
            MAX(runtime_minutes) as max_runtime,
            SUM(runtime_minutes) as total_runtime_minutes
        FROM rag_movies
    """
    basic = execute_query(basic_sql)
    if basic:
        stats['movies'] = dict(basic[0])

    # Review stats
    reviews_sql = """
        SELECT
            COUNT(*) as total_reviews,
            ROUND(AVG(rating)::numeric, 2) as avg_review_rating,
            COUNT(DISTINCT reviewer_name) as unique_reviewers,
            COUNT(DISTINCT movie_id) as movies_with_reviews
        FROM rag_reviews
    """
    reviews = execute_query(reviews_sql)
    if reviews:
        stats['reviews'] = dict(reviews[0])

    # Vector embedding stats
    vector_sql = """
        SELECT
            COUNT(*) as movies_with_embeddings,
            (SELECT COUNT(*) FROM rag_movies) as total_movies,
            ROUND(
                (COUNT(*)::float / NULLIF((SELECT COUNT(*) FROM rag_movies), 0) * 100)::numeric,
                1
            ) as embedding_coverage_percent
        FROM rag_movies
        WHERE plot_embedding IS NOT NULL
    """
    vectors = execute_query(vector_sql)
    if vectors:
        stats['vector_db'] = dict(vectors[0])

    # Review embeddings
    review_vectors_sql = """
        SELECT
            COUNT(*) as reviews_with_embeddings,
            (SELECT COUNT(*) FROM rag_reviews) as total_reviews,
            ROUND(
                (COUNT(*)::float / NULLIF((SELECT COUNT(*) FROM rag_reviews), 0) * 100)::numeric,
                1
            ) as embedding_coverage_percent
        FROM rag_reviews
        WHERE review_embedding IS NOT NULL
    """
    review_vectors = execute_query(review_vectors_sql)
    if review_vectors:
        stats['review_vector_db'] = dict(review_vectors[0])

    # Embedding dimension info
    embedding_dim_sql = """
        SELECT
            vector_dims(plot_embedding) as embedding_dimensions
        FROM rag_movies
        WHERE plot_embedding IS NOT NULL
        LIMIT 1
    """
    embedding_dim = execute_query(embedding_dim_sql)
    if embedding_dim and embedding_dim[0]['embedding_dimensions']:
        stats['vector_config'] = {
            'embedding_dimensions': embedding_dim[0]['embedding_dimensions'],
            'embedding_model': 'text-embedding-3-small',
            'distance_metric': 'cosine_similarity',
            'index_type': 'ivfflat'
        }

    # Genre distribution
    genre_sql = """
        SELECT genre, COUNT(*) as count
        FROM rag_movies
        GROUP BY genre
        ORDER BY count DESC
        LIMIT 15
    """
    genres = execute_query(genre_sql)
    if genres:
        stats['genre_distribution'] = [dict(g) for g in genres]

    # Decade distribution
    decade_sql = """
        SELECT
            (year / 10) * 10 as decade,
            COUNT(*) as count,
            ROUND(AVG(rating)::numeric, 2) as avg_rating
        FROM rag_movies
        GROUP BY (year / 10) * 10
        ORDER BY decade
    """
    decades = execute_query(decade_sql)
    if decades:
        stats['decade_distribution'] = [dict(d) for d in decades]

    # Rating distribution (buckets)
    rating_dist_sql = """
        SELECT
            CASE
                WHEN rating >= 9 THEN '9-10 (Excellent)'
                WHEN rating >= 8 THEN '8-9 (Great)'
                WHEN rating >= 7 THEN '7-8 (Good)'
                WHEN rating >= 6 THEN '6-7 (Above Average)'
                WHEN rating >= 5 THEN '5-6 (Average)'
                ELSE 'Below 5 (Poor)'
            END as rating_bucket,
            COUNT(*) as count
        FROM rag_movies
        GROUP BY rating_bucket
        ORDER BY MIN(rating) DESC
    """
    rating_dist = execute_query(rating_dist_sql)
    if rating_dist:
        stats['rating_distribution'] = [dict(r) for r in rating_dist]

    # Top directors by movie count
    directors_sql = """
        SELECT
            director,
            COUNT(*) as movie_count,
            ROUND(AVG(rating)::numeric, 2) as avg_rating
        FROM rag_movies
        GROUP BY director
        ORDER BY movie_count DESC
        LIMIT 10
    """
    directors = execute_query(directors_sql)
    if directors:
        stats['top_directors'] = [dict(d) for d in directors]

    # Runtime distribution
    runtime_sql = """
        SELECT
            CASE
                WHEN runtime_minutes < 90 THEN 'Short (<90 min)'
                WHEN runtime_minutes < 120 THEN 'Standard (90-120 min)'
                WHEN runtime_minutes < 150 THEN 'Long (120-150 min)'
                ELSE 'Epic (150+ min)'
            END as runtime_category,
            COUNT(*) as count
        FROM rag_movies
        GROUP BY runtime_category
        ORDER BY MIN(runtime_minutes)
    """
    runtime = execute_query(runtime_sql)
    if runtime:
        stats['runtime_distribution'] = [dict(r) for r in runtime]

    # Database storage info
    storage_sql = """
        SELECT
            pg_size_pretty(pg_total_relation_size('rag_movies')) as movies_table_size,
            pg_size_pretty(pg_total_relation_size('rag_reviews')) as reviews_table_size,
            pg_size_pretty(
                pg_total_relation_size('rag_movies') + pg_total_relation_size('rag_reviews')
            ) as total_size
    """
    storage = execute_query(storage_sql)
    if storage:
        stats['storage'] = dict(storage[0])

    # Index information
    index_sql = """
        SELECT
            indexname,
            pg_size_pretty(pg_relation_size(indexname::regclass)) as size
        FROM pg_indexes
        WHERE tablename IN ('rag_movies', 'rag_reviews')
        ORDER BY pg_relation_size(indexname::regclass) DESC
    """
    try:
        indexes = execute_query(index_sql)
        if indexes:
            stats['indexes'] = [dict(i) for i in indexes]
    except:
        stats['indexes'] = []

    # Add Redis cache statistics
    from services.redis_cache import get_redis_stats
    stats['redis_cache'] = get_redis_stats()

    # Cache the stats for 1 hour
    cache_stats(stats, ttl=3600)

    return stats


def get_reviews_for_movie(movie_id: int) -> List[Dict[str, Any]]:
    """Get all reviews for a specific movie."""
    sql = """
        SELECT r.id, r.reviewer_name, r.review_text, r.rating, r.review_date,
               m.title as movie_title
        FROM rag_reviews r
        JOIN rag_movies m ON m.id = r.movie_id
        WHERE r.movie_id = %s
        ORDER BY r.review_date DESC
    """
    results = execute_query(sql, (movie_id,))
    return [dict(row) for row in results] if results else []
