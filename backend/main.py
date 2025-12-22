"""
Main FastAPI application entry point.
Configures routes, CORS, and starts the server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config import config
from routes import chat_router, movies_router

# Create FastAPI app
app = FastAPI(
    title="Movie RAG API",
    description="Hybrid RAG system combining vector search with PostgreSQL for movie queries",
    version="1.0.0"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(chat_router, prefix="/api")
app.include_router(movies_router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Movie RAG API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat/",
            "movies": "/api/movies/",
            "semantic_search": "/api/movies/search/semantic",
            "stats": "/api/movies/stats"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    print(f"Starting Movie RAG API on http://{config.API_HOST}:{config.API_PORT}")
    uvicorn.run(
        "main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        reload=True
    )
