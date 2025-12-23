import React, { useState, useEffect, useRef } from 'react';
import { Film, AlertCircle, RefreshCw, BarChart3, Database, Users, Calendar, Star, Tag, MessageSquare, ChevronDown, ChevronUp, Cpu, Zap, Search, Brain, FileText, ArrowRight, Github, User } from 'lucide-react';
import { ChatMessage } from './components/ChatMessage';
import { ChatInput } from './components/ChatInput';
import { TypingIndicator } from './components/TypingIndicator';
import { SuggestedQueries } from './components/SuggestedQueries';
import { SearchVisualization } from './components/SearchVisualization';
import { AnalyticsPage } from './components/AnalyticsPage';
import { sendMessageWithPhases, getStats, healthCheck, Message, ChatResponse, SearchPhase } from './services/chatService';

interface ChatEntry {
  role: 'user' | 'assistant';
  content: string;
  sources?: ChatResponse['sources'];
  intent?: string;
}

function App() {
  const [messages, setMessages] = useState<ChatEntry[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [stats, setStats] = useState<{
    total_movies: number;
    avg_rating: number;
    earliest_year: number;
    latest_year: number;
    unique_directors: number;
    unique_genres: number;
    unique_reviewers: number;
    unique_actors: number;
  } | null>(null);
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [searchPhase, setSearchPhase] = useState<SearchPhase>('idle');
  const [lastResponse, setLastResponse] = useState<ChatResponse | null>(null);
  const [showAnalytics, setShowAnalytics] = useState(false);
  const [showHowItWorks, setShowHowItWorks] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Check API health and load stats on mount
  useEffect(() => {
    const init = async () => {
      const isHealthy = await healthCheck();
      setApiStatus(isHealthy ? 'online' : 'offline');

      if (isHealthy) {
        try {
          const statsData = await getStats();
          setStats(statsData);
        } catch (e) {
          console.error('Failed to load stats:', e);
        }
      }
    };
    init();
  }, []);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Keep visualization visible - no auto-hide

  const handleSend = async (content: string) => {
    if (apiStatus === 'offline') {
      setError('API is offline. Please start the backend server.');
      return;
    }

    setError(null);
    setSearchPhase('idle');
    // Don't clear lastResponse - keep showing previous results until new ones arrive

    // Build conversation history BEFORE adding new message
    const history: Message[] = messages.map((m) => ({
      role: m.role,
      content: m.content,
    }));

    // Add user message
    const userMessage: ChatEntry = { role: 'user', content };
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Send to API with phase callbacks (history includes all previous messages)
      const response = await sendMessageWithPhases(content, history, (phase) => {
        setSearchPhase(phase);
      });

      setLastResponse(response);

      // Add assistant message
      const assistantMessage: ChatEntry = {
        role: 'assistant',
        content: response.response,
        sources: response.sources,
        intent: response.intent,
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to send message');
      setSearchPhase('idle');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRetryConnection = async () => {
    setApiStatus('checking');
    const isHealthy = await healthCheck();
    setApiStatus(isHealthy ? 'online' : 'offline');

    if (isHealthy) {
      try {
        const statsData = await getStats();
        setStats(statsData);
      } catch (e) {
        console.error('Failed to load stats:', e);
      }
    }
  };

  const handleClearChat = () => {
    setMessages([]);
    setError(null);
    setSearchPhase('idle');
    setLastResponse(null);
  };

  // Show analytics page
  if (showAnalytics) {
    return <AnalyticsPage onBack={() => setShowAnalytics(false)} />;
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header - Responsive */}
      <header className="fixed top-0 left-0 right-0 bg-gray-900/95 backdrop-blur border-b border-gray-800 z-10">
        <div className="max-w-4xl mx-auto px-2 sm:px-4 py-2 sm:py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 sm:gap-3">
              <div className="w-8 h-8 sm:w-10 sm:h-10 bg-indigo-600 rounded-lg sm:rounded-xl flex items-center justify-center">
                <Film className="w-4 h-4 sm:w-6 sm:h-6" />
              </div>
              <div>
                <h1 className="text-sm sm:text-xl font-bold">Movie RAG Chat</h1>
                <p className="text-[10px] sm:text-xs text-gray-400 hidden sm:block">
                  Hybrid search with pgvector + PostgreSQL
                </p>
              </div>
            </div>

            <div className="flex items-center gap-1 sm:gap-3">
              {/* GitHub Link */}
              <a
                href="https://github.com/gstorni/movie-rag-chat"
                target="_blank"
                rel="noopener noreferrer"
                className="p-1.5 sm:p-2 text-gray-400 hover:text-white hover:bg-gray-700/50 rounded-lg transition-colors"
                title="View on GitHub"
              >
                <Github className="w-4 h-4 sm:w-5 sm:h-5" />
              </a>

              {/* Analytics Button */}
              <button
                onClick={() => setShowAnalytics(true)}
                className="p-1.5 sm:p-2 text-gray-400 hover:text-purple-400 hover:bg-purple-500/10 rounded-lg transition-colors"
                title="View Analytics"
              >
                <BarChart3 className="w-4 h-4 sm:w-5 sm:h-5" />
              </button>

              {/* API Status */}
              <div className="flex items-center gap-1 sm:gap-2">
                <div
                  className={`w-2 h-2 rounded-full ${
                    apiStatus === 'online'
                      ? 'bg-green-500'
                      : apiStatus === 'offline'
                      ? 'bg-red-500'
                      : 'bg-yellow-500 animate-pulse'
                  }`}
                />
                <span className="text-[10px] sm:text-xs text-gray-400 hidden sm:inline">
                  {apiStatus === 'checking' ? 'Connecting...' : apiStatus}
                </span>
              </div>

              {apiStatus === 'offline' && (
                <button
                  onClick={handleRetryConnection}
                  className="p-1.5 sm:p-2 text-gray-400 hover:text-white transition-colors"
                  title="Retry connection"
                >
                  <RefreshCw className="w-3.5 h-3.5 sm:w-4 sm:h-4" />
                </button>
              )}

              {messages.length > 0 && (
                <button
                  onClick={handleClearChat}
                  className="px-2 py-1 sm:px-3 sm:py-1.5 text-xs sm:text-sm text-gray-400 hover:text-white border border-gray-700 hover:border-gray-600 rounded-lg transition-colors"
                >
                  Clear
                </button>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Stats Info Bar - always visible, responsive (header: 48px mobile, 73px desktop) */}
      {stats && (
        <div className="fixed top-[48px] sm:top-[73px] left-0 right-0 z-10 bg-gray-800/80 backdrop-blur border-b border-gray-700/50">
          <div className="max-w-4xl mx-auto px-2 sm:px-4 py-2">
            <div className="flex flex-wrap items-center justify-center gap-x-3 gap-y-1 sm:gap-4 text-[10px] sm:text-xs">
              <div className="flex items-center gap-1 text-gray-400">
                <Database className="w-3 h-3 sm:w-3.5 sm:h-3.5 text-blue-400" />
                <span className="text-blue-400 font-medium">{stats.total_movies?.toLocaleString()}</span>
                <span className="hidden sm:inline">movies</span>
              </div>
              <div className="flex items-center gap-1 text-gray-400">
                <Calendar className="w-3 h-3 sm:w-3.5 sm:h-3.5 text-green-400" />
                <span className="text-green-400 font-medium">{stats.earliest_year}—{stats.latest_year}</span>
              </div>
              <div className="flex items-center gap-1 text-gray-400">
                <Tag className="w-3 h-3 sm:w-3.5 sm:h-3.5 text-orange-400" />
                <span className="text-orange-400 font-medium">{stats.unique_genres}</span>
                <span className="hidden sm:inline">genres</span>
              </div>
              <div className="flex items-center gap-1 text-gray-400">
                <Users className="w-3 h-3 sm:w-3.5 sm:h-3.5 text-purple-400" />
                <span className="text-purple-400 font-medium">{stats.unique_directors}</span>
                <span className="hidden sm:inline">directors</span>
              </div>
              <div className="flex items-center gap-1 text-gray-400">
                <User className="w-3 h-3 sm:w-3.5 sm:h-3.5 text-pink-400" />
                <span className="text-pink-400 font-medium">{stats.unique_actors}</span>
                <span className="hidden sm:inline">actors</span>
              </div>
              <div className="flex items-center gap-1 text-gray-400">
                <MessageSquare className="w-3 h-3 sm:w-3.5 sm:h-3.5 text-cyan-400" />
                <span className="text-cyan-400 font-medium">{stats.unique_reviewers}</span>
                <span className="hidden sm:inline">reviewers</span>
              </div>
              <div className="flex items-center gap-1 text-gray-400">
                <Star className="w-3 h-3 sm:w-3.5 sm:h-3.5 text-yellow-400" />
                <span className="text-yellow-400 font-medium">{stats.avg_rating?.toFixed(1)}</span>
                <span className="hidden sm:inline">avg</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Fixed Search Visualization - only visible when searching or has results */}
      {(isLoading || searchPhase !== 'idle' || lastResponse) && (
        <div className="fixed top-[84px] sm:top-[109px] left-0 right-0 z-10 bg-gray-900/95 backdrop-blur border-b border-gray-800">
          <div className="max-w-4xl mx-auto px-4 py-3">
            <SearchVisualization
              isSearching={isLoading}
              currentPhase={searchPhase}
              sources={lastResponse?.sources}
              intent={lastResponse?.intent}
              tokenUsage={lastResponse?.token_usage}
            />
          </div>
        </div>
      )}

      {/* Main content - dynamic padding based on whether visualization is shown */}
      <main className={`max-w-4xl mx-auto px-2 sm:px-4 pb-24 sm:pb-36 ${
        (isLoading || searchPhase !== 'idle' || lastResponse)
          ? 'pt-[320px] sm:pt-[396px]'
          : 'pt-[100px] sm:pt-[130px]'
      }`}>
        {/* Empty state */}
        {messages.length === 0 && (
          <div className="py-12">
            <div className="text-center mb-8">
              <div className="w-16 h-16 bg-gray-800 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <Film className="w-8 h-8 text-indigo-500" />
              </div>
              <h2 className="text-2xl font-bold mb-2">Ask me about movies!</h2>
              <p className="text-gray-400 max-w-md mx-auto">
                I can search through our movie database using semantic similarity and
                structured queries. Try asking about plots, directors, genres, or
                specific films.
              </p>
            </div>
            <SuggestedQueries onSelect={handleSend} />

            {/* How it Works Section */}
            <div className="mt-8 max-w-2xl mx-auto">
              <button
                onClick={() => setShowHowItWorks(!showHowItWorks)}
                className="w-full flex items-center justify-center gap-2 py-3 px-4 bg-gray-800/50 hover:bg-gray-800 border border-gray-700/50 hover:border-gray-600 rounded-xl transition-all text-gray-400 hover:text-gray-300"
              >
                <Brain className="w-4 h-4" />
                <span className="text-sm font-medium">How does this RAG system work?</span>
                {showHowItWorks ? (
                  <ChevronUp className="w-4 h-4" />
                ) : (
                  <ChevronDown className="w-4 h-4" />
                )}
              </button>

              {showHowItWorks && (
                <div className="mt-4 p-5 bg-gray-800/30 border border-gray-700/50 rounded-xl text-sm">
                  {/* Data Flow Section */}
                  <div className="mb-6">
                    <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
                      <FileText className="w-4 h-4 text-blue-400" />
                      Data Pipeline
                    </h3>
                    <div className="flex flex-col sm:flex-row items-start sm:items-center gap-2 sm:gap-3 text-gray-400 text-xs">
                      <div className="flex items-center gap-2 px-3 py-2 bg-blue-500/10 border border-blue-500/30 rounded-lg">
                        <Film className="w-3.5 h-3.5 text-blue-400" />
                        <span>Movies + Plots</span>
                      </div>
                      <ArrowRight className="w-4 h-4 text-gray-600 hidden sm:block" />
                      <div className="flex items-center gap-2 px-3 py-2 bg-purple-500/10 border border-purple-500/30 rounded-lg">
                        <Cpu className="w-3.5 h-3.5 text-purple-400" />
                        <span>OpenAI Embeddings</span>
                      </div>
                      <ArrowRight className="w-4 h-4 text-gray-600 hidden sm:block" />
                      <div className="flex items-center gap-2 px-3 py-2 bg-green-500/10 border border-green-500/30 rounded-lg">
                        <Database className="w-3.5 h-3.5 text-green-400" />
                        <span>PostgreSQL + pgvector</span>
                      </div>
                    </div>
                  </div>

                  {/* Search Pipeline */}
                  <div className="mb-6">
                    <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
                      <Search className="w-4 h-4 text-indigo-400" />
                      Search Pipeline
                    </h3>
                    <div className="bg-gray-900/50 rounded-lg p-4 font-mono text-xs text-gray-400 overflow-x-auto">
                      <div className="whitespace-pre">
{`User Query → Intent Analysis (GPT)
              ↓
        ┌─────┴─────┐
        ↓           ↓
   Vector Search  SQL Search
   (pgvector)    (PostgreSQL)
        ↓           ↓
        └─────┬─────┘
              ↓
      Context Assembly
              ↓
   Response Generation (GPT)`}
                      </div>
                    </div>
                  </div>

                  {/* Key Points */}
                  <div className="mb-6">
                    <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
                      <Zap className="w-4 h-4 text-yellow-400" />
                      Key Features
                    </h3>
                    <ul className="space-y-2 text-gray-400 text-xs">
                      <li className="flex items-start gap-2">
                        <span className="text-green-400 mt-0.5">•</span>
                        <span><strong className="text-gray-300">pgvector</strong> is a PostgreSQL extension that adds vector similarity search directly to the database</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-blue-400 mt-0.5">•</span>
                        <span><strong className="text-gray-300">Hybrid search:</strong> Combines semantic similarity (vectors) with structured queries (SQL)</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-purple-400 mt-0.5">•</span>
                        <span><strong className="text-gray-300">1536-dimension vectors</strong> from OpenAI's text-embedding-3-small model</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-orange-400 mt-0.5">•</span>
                        <span><strong className="text-gray-300">Single database:</strong> All data + vectors in PostgreSQL (not a separate vector DB)</span>
                      </li>
                    </ul>
                  </div>

                  {/* Database Schema */}
                  <div>
                    <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
                      <Database className="w-4 h-4 text-green-400" />
                      Database Schema
                    </h3>
                    <div className="bg-gray-900/50 rounded-lg p-4 font-mono text-xs overflow-x-auto">
                      <table className="w-full text-left">
                        <thead>
                          <tr className="text-gray-500 border-b border-gray-700">
                            <th className="pb-2 pr-4">Table</th>
                            <th className="pb-2 pr-4">Regular Columns</th>
                            <th className="pb-2">Vector Column</th>
                          </tr>
                        </thead>
                        <tbody className="text-gray-400">
                          <tr className="border-b border-gray-800">
                            <td className="py-2 pr-4 text-blue-400">rag_movies</td>
                            <td className="py-2 pr-4">id, title, plot, director, genre, year, rating, <span className="text-pink-400">actors[]</span></td>
                            <td className="py-2 text-purple-400">plot_embedding <span className="text-gray-600">(1536 floats)</span></td>
                          </tr>
                          <tr>
                            <td className="py-2 pr-4 text-blue-400">rag_reviews</td>
                            <td className="py-2 pr-4">id, review_text, reviewer_name, rating</td>
                            <td className="py-2 text-purple-400">review_embedding <span className="text-gray-600">(1536 floats)</span></td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                    <p className="mt-3 text-gray-500 text-xs">
                      Both vector and regular searches query the <strong className="text-gray-400">same tables</strong> in PostgreSQL.
                      Vector search uses the embedding columns with cosine similarity (<code className="text-green-400">&lt;=&gt;</code> operator),
                      while SQL search uses standard columns with regular SQL queries.
                    </p>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Messages */}
        <div className="space-y-6">
          {messages.map((message, index) => (
            <ChatMessage
              key={index}
              role={message.role}
              content={message.content}
              sources={message.sources}
              intent={message.intent}
            />
          ))}
          {isLoading && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>

        {/* Error message */}
        {error && (
          <div className="mt-4 p-4 bg-red-900/30 border border-red-800 rounded-xl flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-red-400 text-sm">{error}</p>
              {apiStatus === 'offline' && (
                <p className="text-red-500/70 text-xs mt-1">
                  Make sure the Python backend is running: cd backend && python main.py
                </p>
              )}
            </div>
          </div>
        )}
      </main>

      {/* Input area */}
      <footer className="fixed bottom-0 left-0 right-0 bg-gray-900/95 backdrop-blur border-t border-gray-800">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <ChatInput
            onSend={handleSend}
            disabled={isLoading || apiStatus === 'offline'}
            placeholder={
              apiStatus === 'offline'
                ? 'API offline - start the backend server'
                : 'Ask about movies...'
            }
          />
        </div>
      </footer>
    </div>
  );
}

export default App;
