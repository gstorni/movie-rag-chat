"""
Database setup script.
Creates schema and inserts mock data.
"""

import os
import sys
sys.path.append('..')
from utils.database import get_cursor


def run_migration(filepath: str):
    """Execute a SQL migration file."""
    print(f"Running migration: {filepath}")

    with open(filepath, 'r') as f:
        sql = f.read()

    with get_cursor(dict_cursor=False) as cursor:
        cursor.execute(sql)

    print(f"  ✓ Completed: {os.path.basename(filepath)}")


def main():
    """Run all migrations in order."""
    migrations_dir = os.path.join(os.path.dirname(__file__), '..', 'migrations')

    migrations = sorted([
        f for f in os.listdir(migrations_dir)
        if f.endswith('.sql')
    ])

    print("=" * 50)
    print("DATABASE SETUP")
    print("=" * 50)
    print(f"\nFound {len(migrations)} migrations to run\n")

    for migration in migrations:
        filepath = os.path.join(migrations_dir, migration)
        try:
            run_migration(filepath)
        except Exception as e:
            print(f"  ✗ Error in {migration}: {e}")
            # Continue with other migrations
            continue

    print("\n" + "=" * 50)
    print("DATABASE SETUP COMPLETE")
    print("=" * 50)


if __name__ == "__main__":
    main()
