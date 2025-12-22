"""Service modules for the RAG application."""

from .embedding_service import generate_embedding, generate_embeddings_batch, create_search_embedding
from .vector_search_service import search_movies_by_similarity, search_reviews_by_similarity, hybrid_search
from .sql_search_service import (
    get_movies_by_year,
    get_movies_by_director,
    get_movies_by_genre,
    get_top_rated_movies,
    get_movies_by_rating_range,
    get_movie_with_reviews,
    search_movies_keyword,
    get_statistics,
    get_reviews_for_movie
)
from .chat_service import process_chat_message
