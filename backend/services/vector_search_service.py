"""
Vector search service for semantic similarity queries.
Uses pgvector for efficient vector similarity search.
"""

from typing import List, Dict, Any
import sys
sys.path.append('..')
from config import config
from utils.database import execute_query
from services.embedding_service import create_search_embedding


def search_movies_by_similarity(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Search movies using vector similarity on plot embeddings.

    Args:
        query: Natural language search query
        limit: Maximum number of results

    Returns:
        List of movies with similarity scores
    """
    # Generate embedding for the query
    query_embedding = create_search_embedding(query)

    # Convert to pgvector format
    embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'

    sql = """
        SELECT
            m.id,
            m.title,
            m.year,
            m.director,
            m.genre,
            m.plot,
            m.rating,
            m.runtime_minutes,
            m.actors,
            1 - (m.plot_embedding <=> %s::vector) as similarity
        FROM rag_movies m
        WHERE m.plot_embedding IS NOT NULL
        ORDER BY m.plot_embedding <=> %s::vector
        LIMIT %s
    """

    results = execute_query(sql, (embedding_str, embedding_str, limit))
    return [dict(row) for row in results] if results else []


def search_reviews_by_similarity(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Search movie reviews using vector similarity.

    Args:
        query: Natural language search query
        limit: Maximum number of results

    Returns:
        List of reviews with similarity scores
    """
    query_embedding = create_search_embedding(query)
    embedding_str = '[' + ','.join(map(str, query_embedding)) + ']'

    sql = """
        SELECT
            r.id,
            r.movie_id,
            m.title as movie_title,
            r.reviewer_name,
            r.review_text,
            r.rating,
            r.review_date,
            1 - (r.review_embedding <=> %s::vector) as similarity
        FROM rag_reviews r
        JOIN rag_movies m ON m.id = r.movie_id
        WHERE r.review_embedding IS NOT NULL
        ORDER BY r.review_embedding <=> %s::vector
        LIMIT %s
    """

    results = execute_query(sql, (embedding_str, embedding_str, limit))
    return [dict(row) for row in results] if results else []


def hybrid_search(query: str, vector_limit: int = 5) -> Dict[str, List[Dict[str, Any]]]:
    """
    Perform hybrid search combining vector and keyword results.

    Args:
        query: Search query
        vector_limit: Max results per vector search

    Returns:
        Dictionary with 'movies' and 'reviews' results
    """
    return {
        'movies': search_movies_by_similarity(query, vector_limit),
        'reviews': search_reviews_by_similarity(query, vector_limit)
    }
