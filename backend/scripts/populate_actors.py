"""
Populate actors for existing movies that don't have them.
"""

import sys
import os
import random
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import execute_query, get_cursor

# Same actors list as in generate_massive_dataset.py
ACTORS = [
    # Hollywood A-List
    "Tom Hanks", "Leonardo DiCaprio", "Brad Pitt", "Denzel Washington", "Morgan Freeman",
    "Robert De Niro", "Al Pacino", "Meryl Streep", "Cate Blanchett", "Nicole Kidman",
    "Sandra Bullock", "Julia Roberts", "Angelina Jolie", "Johnny Depp", "Will Smith",
    "George Clooney", "Matt Damon", "Christian Bale", "Joaquin Phoenix", "Tom Cruise",
    "Scarlett Johansson", "Emma Stone", "Jennifer Lawrence", "Natalie Portman", "Anne Hathaway",
    "Kate Winslet", "Amy Adams", "Viola Davis", "Margot Robbie", "Charlize Theron",
    "Samuel L. Jackson", "Michael B. Jordan", "Dwayne Johnson", "Ryan Gosling", "Jake Gyllenhaal",
    "Oscar Isaac", "Adam Driver", "Timothée Chalamet", "Florence Pugh", "Zendaya",
    # Action Stars
    "Keanu Reeves", "Jason Statham", "Vin Diesel", "Michelle Rodriguez", "Gal Gadot",
    "Chris Hemsworth", "Chris Evans", "Chris Pratt", "Robert Downey Jr.", "Mark Ruffalo",
    "Tom Holland", "Brie Larson", "Simu Liu", "John Boyega", "Idris Elba",
    # Classic Hollywood
    "Marlon Brando", "James Dean", "Humphrey Bogart", "Audrey Hepburn", "Marilyn Monroe",
    "Gregory Peck", "Katharine Hepburn", "Ingrid Bergman", "Cary Grant", "Gene Kelly",
    "Elizabeth Taylor", "Paul Newman", "Robert Redford", "Dustin Hoffman", "Jack Nicholson",
    "Harrison Ford", "Sigourney Weaver", "Jodie Foster", "Anthony Hopkins", "Gary Oldman",
    # British Actors
    "Daniel Craig", "Benedict Cumberbatch", "Tom Hiddleston", "Eddie Redmayne", "Jude Law",
    "Emily Blunt", "Keira Knightley", "Emma Watson", "Tilda Swinton", "Helen Mirren",
    "Judi Dench", "Ian McKellen", "Patrick Stewart", "Ralph Fiennes", "Colin Firth",
    # International Stars
    "Penélope Cruz", "Javier Bardem", "Antonio Banderas", "Gael García Bernal", "Diego Luna",
    "Lupita Nyong'o", "Chiwetel Ejiofor", "Dev Patel", "Priyanka Chopra", "Deepika Padukone",
    "Tony Leung", "Gong Li", "Zhang Ziyi", "Jet Li", "Jackie Chan",
    "Song Kang-ho", "Bae Doona", "Park So-dam", "Choi Min-sik", "Lee Byung-hun",
    "Ken Watanabe", "Rinko Kikuchi", "Tadanobu Asano", "Toshiro Mifune", "Takeshi Kitano",
    "Mads Mikkelsen", "Noomi Rapace", "Alicia Vikander", "Alexander Skarsgård", "Rebecca Ferguson",
    # Rising Stars
    "Anya Taylor-Joy", "Sydney Sweeney", "Austin Butler", "Barry Keoghan", "Paul Mescal",
    "Jenna Ortega", "Xochitl Gomez", "Dominique Thorne", "Kathryn Newton", "Maitreyi Ramakrishnan",
    # Comedy Stars
    "Steve Carell", "Will Ferrell", "Adam Sandler", "Seth Rogen", "Jonah Hill",
    "Melissa McCarthy", "Tiffany Haddish", "Awkwafina", "Ken Jeong", "Kevin Hart",
    # Character Actors
    "Willem Dafoe", "John Turturro", "Steve Buscemi", "J.K. Simmons", "Walton Goggins",
    "Michael Shannon", "Ben Mendelsohn", "John Hawkes", "Sam Rockwell", "Richard Jenkins",
    "Frances McDormand", "Allison Janney", "Octavia Spencer", "Laurie Metcalf", "Margo Martindale",
]

def generate_actors() -> list:
    """Generate a random cast of 2-6 actors."""
    num_actors = random.randint(2, 6)
    return random.sample(ACTORS, min(num_actors, len(ACTORS)))

def main():
    print("=" * 60)
    print("POPULATE ACTORS FOR EXISTING MOVIES")
    print("=" * 60)

    # Check how many movies need actors
    result = execute_query("SELECT COUNT(*) as count FROM rag_movies WHERE actors IS NULL OR actors = '{}'")
    movies_without_actors = result[0]['count'] if result else 0

    total_result = execute_query("SELECT COUNT(*) as count FROM rag_movies")
    total_movies = total_result[0]['count'] if total_result else 0

    print(f"\nTotal movies: {total_movies:,}")
    print(f"Movies without actors: {movies_without_actors:,}")

    if movies_without_actors == 0:
        print("\nAll movies already have actors assigned!")
        return

    print(f"\nPopulating actors for {movies_without_actors:,} movies...")

    batch_size = 1000
    updated = 0
    start_time = time.time()

    with get_cursor() as cursor:
        # Get IDs of movies without actors
        cursor.execute("SELECT id FROM rag_movies WHERE actors IS NULL OR actors = '{}' ORDER BY id")
        movie_ids = [row['id'] for row in cursor.fetchall()]

        for i in range(0, len(movie_ids), batch_size):
            batch_ids = movie_ids[i:i + batch_size]

            for movie_id in batch_ids:
                actors = generate_actors()
                cursor.execute(
                    "UPDATE rag_movies SET actors = %s WHERE id = %s",
                    (actors, movie_id)
                )

            updated += len(batch_ids)
            elapsed = time.time() - start_time
            rate = updated / elapsed if elapsed > 0 else 0
            remaining = (len(movie_ids) - updated) / rate if rate > 0 else 0
            print(f"  Updated {updated:,}/{movies_without_actors:,} movies ({rate:.0f}/sec, ~{remaining:.0f}s remaining)")

    total_time = time.time() - start_time

    print()
    print("=" * 60)
    print("COMPLETE")
    print("=" * 60)
    print(f"Updated {updated:,} movies in {total_time:.1f}s")
    print(f"Average rate: {updated/total_time:.0f} movies/sec")

if __name__ == "__main__":
    main()
