"""
Movies API routes.
Direct access to movie data and search endpoints.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import sys
sys.path.append('..')
from services.sql_search_service import (
    get_movies_by_year,
    get_movies_by_director,
    get_movies_by_genre,
    get_top_rated_movies,
    get_movie_with_reviews,
    search_movies_keyword,
    get_statistics,
    get_detailed_statistics,
    get_reviews_for_movie
)
from services.vector_search_service import search_movies_by_similarity, search_reviews_by_similarity

router = APIRouter(prefix="/movies", tags=["movies"])


class Movie(BaseModel):
    """Movie response model."""
    id: int
    title: str
    year: int
    director: str
    genre: str
    plot: str
    rating: float
    runtime_minutes: int


class Review(BaseModel):
    """Review response model."""
    id: int
    reviewer_name: str
    review_text: str
    rating: float
    review_date: str


class MovieWithReviews(Movie):
    """Movie with reviews response model."""
    reviews: List[Review] = []


@router.get("/", response_model=List[Movie])
async def get_movies(
    year: Optional[int] = Query(None, description="Filter by year"),
    director: Optional[str] = Query(None, description="Filter by director"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    keyword: Optional[str] = Query(None, description="Search in title/plot")
):
    """
    Get movies with optional filters.
    """
    try:
        if year:
            return get_movies_by_year(year)
        elif director:
            return get_movies_by_director(director)
        elif genre:
            return get_movies_by_genre(genre)
        elif keyword:
            return search_movies_keyword(keyword)
        else:
            return get_top_rated_movies(50)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/top", response_model=List[Movie])
async def get_top_movies(limit: int = Query(10, ge=1, le=50)):
    """Get top rated movies."""
    try:
        return get_top_rated_movies(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/semantic")
async def semantic_search(
    query: str = Query(..., description="Natural language search query"),
    limit: int = Query(5, ge=1, le=20)
):
    """
    Search movies using semantic similarity.
    Uses vector embeddings to find movies with similar themes/plots.
    """
    try:
        return search_movies_by_similarity(query, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/reviews")
async def search_reviews(
    query: str = Query(..., description="Search query for reviews"),
    limit: int = Query(5, ge=1, le=20)
):
    """Search reviews using semantic similarity."""
    try:
        return search_reviews_by_similarity(query, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
async def get_movie_stats():
    """Get basic database statistics."""
    try:
        return get_statistics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats/detailed")
async def get_detailed_stats():
    """
    Get comprehensive database and vector statistics.
    Includes: movie stats, review stats, vector DB coverage, genre/decade/rating distributions,
    storage info, and index information.
    """
    try:
        return get_detailed_statistics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{movie_id}", response_model=MovieWithReviews)
async def get_movie(movie_id: int):
    """Get a specific movie with its reviews."""
    try:
        movie = get_movie_with_reviews(movie_id)
        if not movie:
            raise HTTPException(status_code=404, detail="Movie not found")
        return movie
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{movie_id}/reviews", response_model=List[Review])
async def get_movie_reviews(movie_id: int):
    """Get all reviews for a specific movie."""
    try:
        return get_reviews_for_movie(movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
