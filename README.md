# Movie RAG Experiment

A Hybrid RAG (Retrieval-Augmented Generation) system that combines:
- **Vector Search** (pgvector) for semantic similarity
- **PostgreSQL** for structured queries
- **OpenAI GPT-4o-mini** for intelligent responses

## Architecture

```
User Query → Intent Analysis (GPT) → Hybrid Search
                                    ├── Vector Search (semantic)
                                    └── SQL Search (structured)
                                    ↓
                              Combined Context → GPT Response
```

## Project Structure

```
rag-experiment/
├── backend/                    # Python FastAPI backend
│   ├── config.py              # Configuration management
│   ├── main.py                # FastAPI app entry point
│   ├── migrations/            # SQL migrations
│   │   ├── 001_create_schema.sql
│   │   └── 002_insert_mock_data.sql
│   ├── routes/                # API routes
│   │   ├── chat_routes.py     # Chat endpoints
│   │   └── movies_routes.py   # Movies CRUD
│   ├── services/              # Business logic
│   │   ├── chat_service.py    # Chat orchestration
│   │   ├── embedding_service.py
│   │   ├── sql_search_service.py
│   │   └── vector_search_service.py
│   ├── scripts/               # Setup scripts
│   │   ├── setup_database.py
│   │   └── generate_embeddings.py
│   └── utils/                 # Utilities
│       └── database.py        # DB connection helpers
│
└── frontend/                  # React frontend
    ├── src/
    │   ├── App.tsx           # Main chat interface
    │   ├── components/       # UI components
    │   └── services/         # API client
    └── package.json
```

## Setup Instructions

### 1. Database Setup

You'll need PostgreSQL with the pgvector extension installed.

```bash
# Enable pgvector extension
psql -U postgres -d postgres -c 'CREATE EXTENSION IF NOT EXISTS vector;'

# Run migrations
psql -U postgres -d postgres < backend/migrations/001_create_schema.sql
psql -U postgres -d postgres < backend/migrations/002_insert_mock_data.sql
```

### 2. Backend Setup

```bash
cd rag-experiment/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate embeddings (requires OpenAI API key)
python scripts/setup_database.py
python scripts/generate_embeddings.py

# Start the server
python main.py
```

The API will be available at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd rag-experiment/frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

The frontend will be available at `http://localhost:3003`

## API Endpoints

### Chat
- `POST /api/chat/` - Send a message and get AI response
- `GET /api/chat/health` - Health check

### Movies
- `GET /api/movies/` - List movies with optional filters
- `GET /api/movies/top` - Top rated movies
- `GET /api/movies/search/semantic?query=...` - Semantic search
- `GET /api/movies/search/reviews?query=...` - Search reviews
- `GET /api/movies/stats` - Database statistics
- `GET /api/movies/{id}` - Get movie with reviews

## How It Works

1. **Intent Analysis**: GPT analyzes the query to determine search strategy
   - `semantic_search`: Use vector similarity (e.g., "movies about existential crisis")
   - `structured_query`: Use SQL filters (e.g., "movies by Nolan")
   - `hybrid`: Combine both approaches
   - `general_question`: Stats or general info

2. **Context Gathering**: Based on intent, the system:
   - Generates embedding for semantic search via pgvector
   - Executes SQL queries for structured filters
   - Retrieves database statistics if needed

3. **Response Generation**: GPT synthesizes the gathered context into a natural response

## Example Queries

- "What are the best sci-fi movies about AI?"
- "Find movies directed by Christopher Nolan"
- "Movies about space exploration and loneliness"
- "What horror movies deal with family trauma?"
- "How many movies are in the database?"
- "Compare The Matrix and Inception"

## Tech Stack

- **Backend**: Python 3.11+, FastAPI, psycopg2, OpenAI
- **Database**: PostgreSQL 15 with pgvector extension
- **Frontend**: React 18, TypeScript, Tailwind CSS, Vite
- **AI**: OpenAI text-embedding-3-small (embeddings), GPT-4o-mini (chat)
