"""
Embedding service for generating and managing vector embeddings.
Uses OpenAI's text-embedding-3-small model.
"""

from openai import OpenAI
from typing import List
import sys
sys.path.append('..')
from config import config


# Initialize OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)


def generate_embedding(text: str) -> List[float]:
    """
    Generate embedding vector for a single text.

    Args:
        text: The text to embed

    Returns:
        List of floats representing the embedding vector
    """
    response = client.embeddings.create(
        model=config.EMBEDDING_MODEL,
        input=text
    )
    return response.data[0].embedding


def generate_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for multiple texts in a single API call.

    Args:
        texts: List of texts to embed

    Returns:
        List of embedding vectors
    """
    response = client.embeddings.create(
        model=config.EMBEDDING_MODEL,
        input=texts
    )
    # Sort by index to maintain order
    sorted_data = sorted(response.data, key=lambda x: x.index)
    return [item.embedding for item in sorted_data]


def create_search_embedding(query: str) -> List[float]:
    """
    Create an embedding optimized for search queries.
    Wraps the query with context for better semantic matching.

    Args:
        query: The search query

    Returns:
        Embedding vector for the query
    """
    # Add search context to improve matching
    search_text = f"Search query: {query}"
    return generate_embedding(search_text)
