"""
Fetch real movie data from TMDB API and update database.
Conservative approach: 500 movies, 5 requests/second (safe rate).
"""

import sys
import os
import time
import requests
from typing import Optional, Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import get_cursor
from config import config

# TMDB API Configuration
TMDB_BASE_URL = "https://api.themoviedb.org/3"
REQUESTS_PER_SECOND = 5  # Conservative rate (TMDB allows up to 50/sec)
DELAY_BETWEEN_REQUESTS = 1.0 / REQUESTS_PER_SECOND

# Popular movie IDs to start with (these are guaranteed to exist and have good data)
POPULAR_MOVIE_IDS = [
    238,    # The Godfather
    278,    # The Shawshank Redemption
    240,    # The Godfather Part II
    424,    # Schindler's List
    19404,  # Dilwale Dulhania Le Jayenge
    389,    # 12 Angry Men
    129,    # Spirited Away
    155,    # The Dark Knight
    497,    # The Green Mile
    13,     # Forrest Gump
    680,    # Pulp Fiction
    122,    # The Lord of the Rings: The Return of the King
    120,    # The Lord of the Rings: The Fellowship of the Ring
    121,    # The Lord of the Rings: The Two Towers
    637,    # Life Is Beautiful
    496243, # Parasite
    769,    # Goodfellas
    550,    # Fight Club
    27205,  # Inception
    372058, # Your Name
    372754, # Dune
    299536, # Avengers: Infinity War
    299534, # Avengers: Endgame
    603,    # The Matrix
    671,    # Harry Potter and the Philosopher's Stone
    672,    # Harry Potter and the Chamber of Secrets
    673,    # Harry Potter and the Prisoner of Azkaban
    674,    # Harry Potter and the Goblet of Fire
    675,    # Harry Potter and the Order of the Phoenix
    767,    # Harry Potter and the Half-Blood Prince
    12445,  # Harry Potter and the Deathly Hallows: Part 2
]

def fetch_movie_details(movie_id: int) -> Optional[Dict]:
    """
    Fetch detailed movie information from TMDB.

    Args:
        movie_id: TMDB movie ID

    Returns:
        Dict with movie data or None if failed
    """
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {
        'api_key': config.TMDB_API_KEY,
        'append_to_response': 'credits'  # Include cast/crew in same request
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Extract cast (limit to top 6 actors)
        cast = data.get('credits', {}).get('cast', [])
        actors = [actor['name'] for actor in cast[:6]]

        # Extract genres
        genres = [g['name'] for g in data.get('genres', [])]
        genre = genres[0] if genres else 'Drama'

        # Extract director
        crew = data.get('credits', {}).get('crew', [])
        directors = [person['name'] for person in crew if person['job'] == 'Director']
        director = directors[0] if directors else 'Unknown'

        return {
            'title': data.get('title', 'Unknown'),
            'year': int(data.get('release_date', '2000-01-01')[:4]) if data.get('release_date') else 2000,
            'director': director,
            'genre': genre,
            'plot': data.get('overview', 'No plot available.'),
            'rating': round(data.get('vote_average', 7.0), 1),
            'runtime_minutes': data.get('runtime', 120),
            'actors': actors
        }

    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error fetching movie {movie_id}: {e}")
        return None
    except (KeyError, ValueError, IndexError) as e:
        print(f"  ✗ Error parsing movie {movie_id}: {e}")
        return None

def discover_popular_movies(page: int = 1) -> List[int]:
    """
    Discover popular movies using TMDB's discover endpoint.

    Args:
        page: Page number (1-500)

    Returns:
        List of movie IDs
    """
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        'api_key': config.TMDB_API_KEY,
        'sort_by': 'vote_count.desc',  # Most voted movies (quality indicator)
        'vote_count.gte': 1000,  # At least 1000 votes
        'page': page
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return [movie['id'] for movie in data.get('results', [])]

    except requests.exceptions.RequestException as e:
        print(f"  ✗ Error discovering movies (page {page}): {e}")
        return []

def insert_movie(cursor, movie: Dict) -> bool:
    """
    Insert or update a movie in the database.

    Args:
        cursor: Database cursor
        movie: Movie data dict

    Returns:
        True if successful
    """
    try:
        cursor.execute("""
            INSERT INTO rag_movies (title, year, director, genre, plot, rating, runtime_minutes, actors)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (title, year) DO UPDATE SET
                director = EXCLUDED.director,
                genre = EXCLUDED.genre,
                plot = EXCLUDED.plot,
                rating = EXCLUDED.rating,
                runtime_minutes = EXCLUDED.runtime_minutes,
                actors = EXCLUDED.actors
        """, (
            movie['title'],
            movie['year'],
            movie['director'],
            movie['genre'],
            movie['plot'],
            movie['rating'],
            movie['runtime_minutes'],
            movie['actors']
        ))
        return True
    except Exception as e:
        print(f"  ✗ Error inserting movie '{movie['title']}': {e}")
        return False

def main():
    print("=" * 70)
    print("FETCH REAL MOVIES FROM TMDB")
    print("=" * 70)

    # Validate API key
    if not config.TMDB_API_KEY:
        print("\n✗ ERROR: TMDB_API_KEY not set in .env file!")
        print("  1. Get API key from: https://www.themoviedb.org/settings/api")
        print("  2. Add to .env: TMDB_API_KEY=your_key_here")
        return

    print(f"\n✓ TMDB API Key: {config.TMDB_API_KEY[:10]}...")
    print(f"✓ Rate limit: {REQUESTS_PER_SECOND} requests/second (conservative)")
    print(f"✓ Target: 500 movies")

    # Gather movie IDs
    print("\n" + "-" * 70)
    print("GATHERING MOVIE IDS")
    print("-" * 70)

    movie_ids = []

    # Add popular IDs
    movie_ids.extend(POPULAR_MOVIE_IDS)
    print(f"✓ Added {len(POPULAR_MOVIE_IDS)} popular movie IDs")

    # Discover more movies from TMDB
    pages_needed = (500 - len(movie_ids)) // 20 + 1  # 20 results per page

    for page in range(1, min(pages_needed + 1, 26)):  # Max 25 pages (500 movies)
        discovered_ids = discover_popular_movies(page)
        movie_ids.extend(discovered_ids)
        print(f"  Page {page}: Found {len(discovered_ids)} movies (total: {len(movie_ids)})")
        time.sleep(DELAY_BETWEEN_REQUESTS)

        if len(movie_ids) >= 500:
            break

    # Limit to 500
    movie_ids = movie_ids[:500]

    print(f"\n✓ Total movie IDs gathered: {len(movie_ids)}")

    # Fetch and insert movies
    print("\n" + "-" * 70)
    print("FETCHING MOVIE DATA")
    print("-" * 70)

    successful = 0
    failed = 0
    skipped = 0
    start_time = time.time()

    with get_cursor() as cursor:
        for i, movie_id in enumerate(movie_ids, 1):
            # Fetch details
            movie = fetch_movie_details(movie_id)

            if movie:
                # Insert to database
                if insert_movie(cursor, movie):
                    successful += 1
                    print(f"  [{i}/{len(movie_ids)}] ✓ {movie['title']} ({movie['year']}) - {len(movie['actors'])} actors")
                else:
                    failed += 1
            else:
                failed += 1

            # Rate limiting
            time.sleep(DELAY_BETWEEN_REQUESTS)

            # Progress update every 50 movies
            if i % 50 == 0:
                elapsed = time.time() - start_time
                rate = i / elapsed
                remaining = (len(movie_ids) - i) / rate if rate > 0 else 0
                print(f"\n  Progress: {i}/{len(movie_ids)} ({i/len(movie_ids)*100:.1f}%) - {rate:.1f} movies/sec - ~{remaining:.0f}s remaining\n")

    total_time = time.time() - start_time

    print("\n" + "=" * 70)
    print("COMPLETE")
    print("=" * 70)
    print(f"✓ Successful: {successful}")
    print(f"✗ Failed: {failed}")
    print(f"⊘ Skipped: {skipped}")
    print(f"⏱ Total time: {total_time:.1f}s ({total_time/60:.1f} minutes)")
    print(f"⚡ Average rate: {successful/total_time:.2f} movies/sec")

if __name__ == "__main__":
    main()
