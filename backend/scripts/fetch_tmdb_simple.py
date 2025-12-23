"""
Simple TMDB fetcher that outputs SQL INSERT statements.
Run this locally, then pipe the output to psql on the VM.
"""

import time
import requests
import sys

TMDB_API_KEY = "1ada2b99896a96c972ac8cfef1e28e3a"
TMDB_BASE_URL = "https://api.themoviedb.org/3"
REQUESTS_PER_SECOND = 10
DELAY = 1.0 / REQUESTS_PER_SECOND

# Popular movie IDs
MOVIE_IDS = [
    238, 278, 240, 424, 19404, 389, 129, 155, 497, 13,
    680, 122, 120, 121, 637, 496243, 769, 550, 27205, 372058,
    372754, 299536, 299534, 603, 671, 672, 673, 674, 675, 767, 12445
]

def escape_sql(s):
    """Escape single quotes for SQL."""
    if s is None:
        return ''
    return str(s).replace("'", "''")

def fetch_movie(movie_id):
    """Fetch movie from TMDB."""
    url = f"{TMDB_BASE_URL}/movie/{movie_id}"
    params = {'api_key': TMDB_API_KEY, 'append_to_response': 'credits'}

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        # Extract data
        title = escape_sql(data.get('title', ''))
        year = int(data.get('release_date', '2000')[:4]) if data.get('release_date') else 2000

        # Director
        crew = data.get('credits', {}).get('crew', [])
        directors = [p['name'] for p in crew if p['job'] == 'Director']
        director = escape_sql(directors[0] if directors else 'Unknown')

        # Genre
        genres = data.get('genres', [])
        genre = escape_sql(genres[0]['name'] if genres else 'Drama')

        # Plot
        plot = escape_sql(data.get('overview', 'No plot available.'))

        # Rating & runtime
        rating = round(data.get('vote_average', 7.0), 1)
        runtime = data.get('runtime', 120)

        # Actors (top 6)
        cast = data.get('credits', {}).get('cast', [])
        # Escape quotes for array literals: double quotes need to be doubled inside array
        actors = [a['name'].replace('"', '""') for a in cast[:6]]
        # Single quotes in actors are fine inside double-quoted array elements
        actors_array = '{' + ','.join(f'"{a}"' for a in actors) + '}'

        # Generate SQL
        sql = f"INSERT INTO rag_movies (title, year, director, genre, plot, rating, runtime_minutes, actors) VALUES ('{title}', {year}, '{director}', '{genre}', '{plot}', {rating}, {runtime}, '{actors_array}');"

        return sql

    except Exception as e:
        print(f"-- Error fetching {movie_id}: {e}", file=sys.stderr)
        return None

print("-- TMDB Movie Data", file=sys.stderr)
print("-- Fetching 9,500 more movies (total will be 10,000)...", file=sys.stderr)
print("BEGIN;")

# Fetch from discover API
# We already have 510 movies, so fetch 9,500 more to reach 10,000 total
# Start from page 26 (we already fetched pages 1-25)
for page in range(26, 501):  # Pages 26-500 = 475 pages × 20 = 9,500 movies
    url = f"{TMDB_BASE_URL}/discover/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'sort_by': 'vote_count.desc',
        'vote_count.gte': 1000,
        'page': page
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        results = r.json().get('results', [])

        for movie in results:
            movie_id = movie['id']
            sql = fetch_movie(movie_id)
            if sql:
                print(sql)
            time.sleep(DELAY)

        print(f"-- Page {page} complete ({len(results)} movies)", file=sys.stderr)

    except Exception as e:
        print(f"-- Error on page {page}: {e}", file=sys.stderr)

    time.sleep(DELAY)

print("COMMIT;")
print("-- Done!", file=sys.stderr)
