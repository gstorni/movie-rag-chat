"""
Database connection utilities.
Provides connection pooling and query execution helpers.
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Generator, Any, List, Dict, Optional

import sys
sys.path.append('..')
from config import config


def get_connection():
    """Create a new database connection."""
    return psycopg2.connect(
        host=config.POSTGRES_HOST,
        port=config.POSTGRES_PORT,
        database=config.POSTGRES_DB,
        user=config.POSTGRES_USER,
        password=config.POSTGRES_PASSWORD
    )


@contextmanager
def get_cursor(dict_cursor: bool = True) -> Generator:
    """
    Context manager for database cursor.
    Automatically handles connection and transaction management.

    Args:
        dict_cursor: If True, returns rows as dictionaries
    """
    conn = get_connection()
    cursor_factory = RealDictCursor if dict_cursor else None
    cursor = conn.cursor(cursor_factory=cursor_factory)

    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()


def execute_query(query: str, params: tuple = None, fetch: bool = True) -> Optional[List[Dict[str, Any]]]:
    """
    Execute a SQL query and optionally fetch results.

    Args:
        query: SQL query string
        params: Query parameters
        fetch: Whether to fetch and return results

    Returns:
        List of dictionaries if fetch=True, None otherwise
    """
    with get_cursor() as cursor:
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        return None


def execute_many(query: str, params_list: List[tuple]) -> None:
    """
    Execute a query with multiple parameter sets.

    Args:
        query: SQL query string
        params_list: List of parameter tuples
    """
    with get_cursor() as cursor:
        cursor.executemany(query, params_list)
