"""
Chat service for processing user queries and generating responses.
Orchestrates between vector search, SQL search, and LLM generation.
"""

from openai import OpenAI
from typing import List, Dict, Any
import json
import sys
sys.path.append('..')
from config import config
from services.vector_search_service import hybrid_search
from services.sql_search_service import (
    get_movies_by_year,
    get_movies_by_director,
    get_movies_by_genre,
    get_movies_by_actor,
    get_top_rated_movies,
    get_statistics,
    search_movies_keyword
)

# Initialize OpenAI client
client = OpenAI(api_key=config.OPENAI_API_KEY)


def analyze_query_intent(query: str) -> tuple[Dict[str, Any], Dict[str, int]]:
    """
    Use LLM to analyze the user's query intent.
    Determines whether to use vector search, SQL search, or both.

    Args:
        query: User's natural language query

    Returns:
        Tuple of (intent dict, token usage dict)
    """
    system_prompt = """You are a query analyzer for a movie database. Analyze the user's query and return a JSON object with:
    - "intent": one of ["semantic_search", "structured_query", "hybrid"]
    - "filters": object with any extracted filters like {"year": 1994, "director": "name", "genre": "action", "actor": "name", "min_rating": 8.0, "title": "movie name"}
    - "keywords": array of important keywords for search
    - "needs_statistics": boolean if they're asking for stats/counts

    Examples:
    - "movies about space travel" -> {"intent": "semantic_search", "filters": {}, "keywords": ["space", "travel"]}
    - "tell me about Schindler's List" -> {"intent": "hybrid", "filters": {"title": "Schindler's List"}, "keywords": ["Schindler's List"]}
    - "what is the plot of The Godfather" -> {"intent": "hybrid", "filters": {"title": "The Godfather"}, "keywords": ["Godfather", "plot"]}
    - "Nolan movies" -> {"intent": "structured_query", "filters": {"director": "Nolan"}, "keywords": ["Nolan"]}
    - "movies with Tom Hanks" -> {"intent": "structured_query", "filters": {"actor": "Tom Hanks"}, "keywords": ["Tom Hanks"]}
    - "Leonardo DiCaprio sci-fi movies" -> {"intent": "hybrid", "filters": {"actor": "Leonardo DiCaprio", "genre": "sci-fi"}, "keywords": ["DiCaprio", "sci-fi"]}
    - "best sci-fi movies from the 90s" -> {"intent": "hybrid", "filters": {"genre": "sci-fi", "year_range": [1990, 1999]}, "keywords": ["sci-fi", "90s"]}
    - "how many movies are in the database" -> {"intent": "hybrid", "filters": {}, "keywords": [], "needs_statistics": true}

    IMPORTANT: Always use "hybrid", "semantic_search", or "structured_query" - NEVER use "general_question".

    Return ONLY valid JSON, no markdown or explanation."""

    response = client.chat.completions.create(
        model=config.CHAT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ],
        temperature=0
    )

    token_usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens
    }

    try:
        return json.loads(response.choices[0].message.content), token_usage
    except json.JSONDecodeError:
        # Fallback to hybrid search if parsing fails
        return {"intent": "hybrid", "filters": {}, "keywords": query.split()}, token_usage


def gather_context(query: str, intent_analysis: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gather relevant context based on query intent.

    Args:
        query: Original user query
        intent_analysis: Result from analyze_query_intent

    Returns:
        Dict with all gathered context
    """
    context = {
        "vector_results": {"movies": [], "reviews": []},
        "sql_results": [],
        "statistics": None
    }

    intent = intent_analysis.get("intent", "hybrid")
    filters = intent_analysis.get("filters", {})

    # Always do vector search for semantic and hybrid intents
    if intent in ["semantic_search", "hybrid"]:
        context["vector_results"] = hybrid_search(query, vector_limit=5)

    # Do structured queries based on filters
    if intent in ["structured_query", "hybrid"]:
        if "title" in filters:
            # Search by title
            title_results = search_movies_keyword(filters["title"])
            context["sql_results"].extend(title_results)
        if "director" in filters:
            context["sql_results"].extend(get_movies_by_director(filters["director"]))
        if "year" in filters:
            context["sql_results"].extend(get_movies_by_year(filters["year"]))
        if "genre" in filters:
            context["sql_results"].extend(get_movies_by_genre(filters["genre"]))
        if "actor" in filters:
            context["sql_results"].extend(get_movies_by_actor(filters["actor"]))
        if "min_rating" in filters:
            context["sql_results"].extend(get_top_rated_movies(10))

        # Keyword search as fallback
        keywords = intent_analysis.get("keywords", [])
        for keyword in keywords[:3]:  # Limit to first 3 keywords
            keyword_results = search_movies_keyword(keyword)
            context["sql_results"].extend(keyword_results)

    # Get statistics if needed
    if intent_analysis.get("needs_statistics"):
        context["statistics"] = get_statistics()

    # Deduplicate SQL results by movie ID
    seen_ids = set()
    unique_results = []
    for movie in context["sql_results"]:
        if movie["id"] not in seen_ids:
            seen_ids.add(movie["id"])
            unique_results.append(movie)
    context["sql_results"] = unique_results[:10]  # Limit to 10

    return context


def format_context_for_llm(context: Dict[str, Any]) -> str:
    """
    Format gathered context into a string for the LLM prompt.

    Args:
        context: Context dictionary from gather_context

    Returns:
        Formatted string for LLM context
    """
    parts = []

    # Vector search results (semantic matches)
    if context["vector_results"]["movies"]:
        parts.append("=== SEMANTICALLY SIMILAR MOVIES ===")
        for movie in context["vector_results"]["movies"]:
            similarity = movie.get('similarity', 0) * 100
            actors = movie.get('actors', [])
            actors_str = ", ".join(actors[:3]) if actors else "Unknown cast"
            parts.append(f"- {movie['title']} ({movie['year']}) by {movie['director']}")
            parts.append(f"  Genre: {movie['genre']} | Rating: {movie['rating']}/10 | Similarity: {similarity:.1f}%")
            parts.append(f"  Cast: {actors_str}")
            parts.append(f"  Plot: {movie['plot'][:200]}...")

    if context["vector_results"]["reviews"]:
        parts.append("\n=== RELEVANT REVIEWS ===")
        for review in context["vector_results"]["reviews"][:3]:
            parts.append(f"- Review for '{review['movie_title']}' by {review['reviewer_name']}:")
            parts.append(f"  \"{review['review_text'][:150]}...\" (Rating: {review['rating']}/10)")

    # SQL search results (structured matches)
    if context["sql_results"]:
        parts.append("\n=== MATCHING MOVIES FROM DATABASE ===")
        for movie in context["sql_results"]:
            actors = movie.get('actors', [])
            actors_str = ", ".join(actors[:3]) if actors else "Unknown cast"
            parts.append(f"- {movie['title']} ({movie['year']}) by {movie['director']}")
            parts.append(f"  Cast: {actors_str}")
            parts.append(f"  Genre: {movie['genre']} | Rating: {movie['rating']}/10 | Runtime: {movie['runtime_minutes']} min")

    # Statistics
    if context["statistics"]:
        stats = context["statistics"]
        parts.append("\n=== DATABASE STATISTICS ===")
        parts.append(f"Total movies: {stats.get('total_movies', 'N/A')}")
        parts.append(f"Average rating: {stats.get('avg_rating', 'N/A'):.1f}/10")
        parts.append(f"Year range: {stats.get('earliest_year', 'N/A')} - {stats.get('latest_year', 'N/A')}")
        parts.append(f"Unique directors: {stats.get('unique_directors', 'N/A')}")

    return "\n".join(parts) if parts else "No relevant information found in the database."


def generate_response(query: str, context_str: str, conversation_history: List[Dict[str, str]] = None) -> tuple[str, Dict[str, int]]:
    """
    Generate a response using the LLM with gathered context.

    Args:
        query: User's question
        context_str: Formatted context string
        conversation_history: Previous messages for context

    Returns:
        Tuple of (response string, token usage dict)
    """
    system_prompt = """You are a movie database assistant. You can ONLY discuss movies that are provided in the context below.

CRITICAL RULES:
1. NEVER use your general knowledge about movies
2. ONLY discuss movies that appear in the provided context
3. If the context shows "No relevant information found in the database", respond: "I don't have information about that in my database."
4. DO NOT make up information or use external knowledge
5. If the context contains movie results, use them to answer the question

When answering:
- Only cite movies from the context
- Include details like year, director, rating, actors, and plot when available
- Be conversational but stick strictly to database information
- Present the movies in a helpful, organized way
- DO NOT add closing remarks like "let me know", "feel free to ask", or "if you have questions"
- End your response naturally after providing the information"""

    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history[-6:])  # Keep last 6 messages

    # Add context and query
    user_message = f"""Context from database:
{context_str}

User question: {query}"""

    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=config.CHAT_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=1000
    )

    token_usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens
    }

    return response.choices[0].message.content, token_usage


def process_chat_message(query: str, conversation_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
    """
    Main entry point for processing a chat message.
    Orchestrates intent analysis, context gathering, and response generation.

    Args:
        query: User's message
        conversation_history: Previous conversation messages

    Returns:
        Dict with response and metadata
    """
    # Step 1: Analyze query intent
    intent_analysis, intent_tokens = analyze_query_intent(query)

    # Step 2: Gather relevant context
    context = gather_context(query, intent_analysis)

    # Step 3: Format context for LLM
    context_str = format_context_for_llm(context)

    # Step 4: Generate response
    response, response_tokens = generate_response(query, context_str, conversation_history)

    # Aggregate token usage
    total_tokens = {
        "intent_analysis": intent_tokens,
        "response_generation": response_tokens,
        "total": {
            "prompt_tokens": intent_tokens["prompt_tokens"] + response_tokens["prompt_tokens"],
            "completion_tokens": intent_tokens["completion_tokens"] + response_tokens["completion_tokens"],
            "total_tokens": intent_tokens["total_tokens"] + response_tokens["total_tokens"]
        }
    }

    return {
        "response": response,
        "intent": intent_analysis.get("intent"),
        "sources": {
            "vector_matches": len(context["vector_results"]["movies"]) + len(context["vector_results"]["reviews"]),
            "sql_matches": len(context["sql_results"]),
            "used_statistics": context["statistics"] is not None
        },
        "token_usage": total_tokens
    }
