"""
Clean all movie data from the RAG database.
Removes all records from rag_movies and rag_reviews tables.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.database import get_cursor

def main():
    print("=" * 70)
    print("CLEAN RAG DATABASE")
    print("=" * 70)

    with get_cursor() as cursor:
        # Check counts before deletion
        cursor.execute("SELECT COUNT(*) as count FROM rag_movies")
        movies_count = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM rag_reviews")
        reviews_count = cursor.fetchone()['count']

        print(f"\nCurrent database state:")
        print(f"  Movies: {movies_count:,}")
        print(f"  Reviews: {reviews_count:,}")

        if movies_count == 0 and reviews_count == 0:
            print("\n✓ Database is already empty!")
            return

        print(f"\n⚠️  This will delete ALL {movies_count:,} movies and {reviews_count:,} reviews!")
        confirm = input("Type 'DELETE' to confirm: ")

        if confirm != 'DELETE':
            print("\n✗ Cancelled - no data deleted")
            return

        print("\nDeleting data...")

        # Delete reviews first (foreign key constraint)
        cursor.execute("DELETE FROM rag_reviews")
        print(f"  ✓ Deleted {reviews_count:,} reviews")

        # Delete movies (cascades to reviews, but already deleted above)
        cursor.execute("DELETE FROM rag_movies")
        print(f"  ✓ Deleted {movies_count:,} movies")

        # Reset sequences
        cursor.execute("ALTER SEQUENCE rag_movies_id_seq RESTART WITH 1")
        cursor.execute("ALTER SEQUENCE rag_reviews_id_seq RESTART WITH 1")
        print("  ✓ Reset ID sequences")

        # Vacuum to reclaim space
        cursor.execute("VACUUM ANALYZE rag_movies")
        cursor.execute("VACUUM ANALYZE rag_reviews")
        print("  ✓ Vacuumed tables")

    print("\n" + "=" * 70)
    print("DATABASE CLEANED SUCCESSFULLY")
    print("=" * 70)
    print("All movie data and vector embeddings have been removed.")

if __name__ == "__main__":
    main()
