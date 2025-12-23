/**
 * Chat service for communicating with the RAG backend.
 */

export interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export interface TokenUsage {
  prompt_tokens: number;
  completion_tokens: number;
  total_tokens: number;
}

export interface ChatResponse {
  response: string;
  intent: string;
  sources: {
    vector_matches: number;
    sql_matches: number;
    used_statistics: boolean;
    redis_cache_hit?: boolean;
  };
  token_usage?: {
    intent_analysis: TokenUsage;
    response_generation: TokenUsage;
    total: TokenUsage;
  };
}

export type SearchPhase = 'idle' | 'analyzing' | 'vector_search' | 'sql_search' | 'generating' | 'complete';

export interface PhaseCallback {
  (phase: SearchPhase): void;
}

const API_BASE = '/api';

/**
 * Simulate phase progression with realistic timing.
 * In a real implementation, the backend would send these updates via SSE/WebSocket.
 */
async function simulatePhases(onPhaseChange: PhaseCallback): Promise<void> {
  const phases: { phase: SearchPhase; delay: number }[] = [
    { phase: 'analyzing', delay: 300 },
    { phase: 'vector_search', delay: 600 },
    { phase: 'sql_search', delay: 500 },
    { phase: 'generating', delay: 0 }, // Stays here until response arrives
  ];

  for (const { phase, delay } of phases) {
    onPhaseChange(phase);
    if (delay > 0) {
      await new Promise(resolve => setTimeout(resolve, delay));
    }
  }
}

/**
 * Send a chat message with phase callbacks for visualization.
 */
export async function sendMessageWithPhases(
  message: string,
  conversationHistory: Message[],
  onPhaseChange: PhaseCallback
): Promise<ChatResponse> {
  // Start phase simulation in parallel with API call
  const phasePromise = simulatePhases(onPhaseChange);

  const response = await fetch(`${API_BASE}/chat/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      conversation_history: conversationHistory,
    }),
  });

  // Wait for minimum phase progression
  await phasePromise;

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Chat request failed: ${error}`);
  }

  const result = await response.json();

  // Signal completion
  onPhaseChange('complete');

  return result;
}

/**
 * Send a chat message and get a response from the RAG system.
 */
export async function sendMessage(
  message: string,
  conversationHistory: Message[]
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE}/chat/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      conversation_history: conversationHistory,
    }),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Chat request failed: ${error}`);
  }

  return response.json();
}

/**
 * Get database statistics.
 */
export async function getStats(): Promise<{
  total_movies: number;
  avg_rating: number;
  earliest_year: number;
  latest_year: number;
  unique_directors: number;
}> {
  const response = await fetch(`${API_BASE}/movies/stats`);
  if (!response.ok) {
    throw new Error('Failed to fetch stats');
  }
  return response.json();
}

/**
 * Health check for the API.
 */
export async function healthCheck(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE}/chat/health`);
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * Detailed statistics interface
 */
export interface DetailedStats {
  movies: {
    total_movies: number;
    avg_rating: number;
    min_rating: number;
    max_rating: number;
    rating_stddev: number;
    earliest_year: number;
    latest_year: number;
    unique_directors: number;
    unique_genres: number;
    avg_runtime: number;
    min_runtime: number;
    max_runtime: number;
    total_runtime_minutes: number;
  };
  reviews: {
    total_reviews: number;
    avg_review_rating: number;
    unique_reviewers: number;
    movies_with_reviews: number;
  };
  vector_db: {
    movies_with_embeddings: number;
    total_movies: number;
    embedding_coverage_percent: number;
  };
  review_vector_db: {
    reviews_with_embeddings: number;
    total_reviews: number;
    embedding_coverage_percent: number;
  };
  vector_config: {
    embedding_dimensions: number;
    embedding_model: string;
    distance_metric: string;
    index_type: string;
  };
  genre_distribution: Array<{ genre: string; count: number }>;
  decade_distribution: Array<{ decade: number; count: number; avg_rating: number }>;
  rating_distribution: Array<{ rating_bucket: string; count: number }>;
  top_directors: Array<{ director: string; movie_count: number; avg_rating: number }>;
  runtime_distribution: Array<{ runtime_category: string; count: number }>;
  storage: {
    movies_table_size: string;
    reviews_table_size: string;
    total_size: string;
  };
  indexes: Array<{ indexname: string; size: string }>;
  redis_cache?: {
    available: boolean;
    status: string;
    host?: string;
    cache_stats?: {
      hits: number;
      misses: number;
      total_requests: number;
      hit_rate_percent: number;
    };
    cached_items?: {
      search_results: number;
      stats_cached: boolean;
    };
    memory?: {
      used_memory: string;
      used_memory_peak: string;
      connected_clients: number;
    };
    server?: {
      version: string;
      uptime_days: number;
    };
  };
}

/**
 * Get detailed database and vector statistics.
 */
export async function getDetailedStats(): Promise<DetailedStats> {
  const response = await fetch(`${API_BASE}/movies/stats/detailed`);
  if (!response.ok) {
    throw new Error('Failed to fetch detailed stats');
  }
  return response.json();
}
