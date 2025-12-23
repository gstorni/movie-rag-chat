import React, { useEffect, useState } from 'react';
import {
  Database,
  Cpu,
  HardDrive,
  Film,
  Star,
  Clock,
  Users,
  BarChart3,
  Layers,
  Zap,
  RefreshCw,
  ArrowLeft,
  TrendingUp,
  Hash,
  Server,
  Box,
  X
} from 'lucide-react';
import { getDetailedStats, DetailedStats } from '../services/chatService';

interface AnalyticsPageProps {
  onBack: () => void;
}

export function AnalyticsPage({ onBack }: AnalyticsPageProps) {
  const [stats, setStats] = useState<DetailedStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null);

  const loadStats = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getDetailedStats();
      setStats(data);
      setLastUpdated(new Date());
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load statistics');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStats();
  }, []);

  const formatNumber = (num: number) => num?.toLocaleString() ?? '—';
  const formatRuntime = (minutes: number) => {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4 text-indigo-500" />
          <p className="text-gray-400">Loading analytics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-400 mb-4">{error}</p>
          <button
            onClick={loadStats}
            className="px-4 py-2 bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!stats) return null;

  const maxGenreCount = Math.max(...(stats.genre_distribution?.map(g => g.count) || [1]));
  const maxDecadeCount = Math.max(...(stats.decade_distribution?.map(d => d.count) || [1]));

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="sticky top-0 bg-gray-900/95 backdrop-blur border-b border-gray-800 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={onBack}
                className="p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-purple-600 rounded-xl flex items-center justify-center">
                  <BarChart3 className="w-6 h-6" />
                </div>
                <div>
                  <h1 className="text-xl font-bold">Database Analytics</h1>
                  <p className="text-xs text-gray-400">
                    Comprehensive stats for nerds
                  </p>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              {lastUpdated && (
                <span className="text-xs text-gray-500">
                  Updated: {lastUpdated.toLocaleTimeString()}
                </span>
              )}
              <button
                onClick={loadStats}
                className="p-2 text-gray-400 hover:text-white hover:bg-gray-800 rounded-lg transition-colors"
                title="Refresh"
              >
                <RefreshCw className="w-4 h-4" />
              </button>
              <button
                onClick={onBack}
                className="p-2 text-gray-400 hover:text-red-400 hover:bg-red-500/10 rounded-lg transition-colors"
                title="Close"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        {/* Overview Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <StatCard
            icon={Film}
            label="Total Movies"
            value={formatNumber(stats.movies?.total_movies)}
            color="blue"
          />
          <StatCard
            icon={Star}
            label="Avg Rating"
            value={stats.movies?.avg_rating?.toFixed(2) ?? '—'}
            subValue={`σ = ${stats.movies?.rating_stddev ?? '—'}`}
            color="yellow"
          />
          <StatCard
            icon={Users}
            label="Directors"
            value={formatNumber(stats.movies?.unique_directors)}
            color="green"
          />
          <StatCard
            icon={Layers}
            label="Genres"
            value={formatNumber(stats.movies?.unique_genres)}
            color="purple"
          />
        </div>

        {/* PostgreSQL Database Section */}
        <Section title="PostgreSQL Database" icon={Database} color="green">
          <div className="grid md:grid-cols-3 gap-4 mb-6">
            <MetricCard
              label="Total Movies"
              value={formatNumber(stats.movies?.total_movies)}
              icon={Film}
            />
            <MetricCard
              label="Total Reviews"
              value={formatNumber(stats.reviews?.total_reviews)}
              icon={Star}
            />
            <MetricCard
              label="Unique Reviewers"
              value={formatNumber(stats.reviews?.unique_reviewers)}
              icon={Users}
            />
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Storage Info */}
            <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700/50">
              <div className="flex items-center gap-2 mb-4">
                <HardDrive className="w-5 h-5 text-green-400" />
                <h4 className="font-medium">Storage Usage</h4>
              </div>
              <div className="space-y-3">
                <StorageItem label="Movies Table" value={stats.storage?.movies_table_size} icon={Film} />
                <StorageItem label="Reviews Table" value={stats.storage?.reviews_table_size} icon={Star} />
                <div className="pt-3 border-t border-gray-700">
                  <StorageItem label="Total Size" value={stats.storage?.total_size} icon={Database} highlight />
                </div>
              </div>
            </div>

            {/* Database Indexes */}
            <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700/50">
              <div className="flex items-center gap-2 mb-4">
                <Box className="w-5 h-5 text-green-400" />
                <h4 className="font-medium">Indexes ({stats.indexes?.length || 0})</h4>
              </div>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {stats.indexes?.length > 0 ? (
                  stats.indexes.map((index) => (
                    <div key={index.indexname} className="flex justify-between items-center text-sm py-1">
                      <span className="text-gray-400 font-mono text-xs truncate flex-1 mr-2">
                        {index.indexname}
                      </span>
                      <span className="text-green-400 font-mono text-xs whitespace-nowrap">
                        {index.size}
                      </span>
                    </div>
                  ))
                ) : (
                  <p className="text-gray-500 text-sm">No index information available</p>
                )}
              </div>
            </div>
          </div>
        </Section>

        {/* Redis Cache Section */}
        {stats.redis_cache && stats.redis_cache.available && (
          <Section title="Redis Cache" icon={Zap} color="red">
            <div className="grid md:grid-cols-2 gap-6">
              {/* Cache Statistics */}
              <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700/50">
                <div className="flex items-center gap-2 mb-4">
                  <TrendingUp className="w-5 h-5 text-red-400" />
                  <h4 className="font-medium">Cache Performance</h4>
                  <span className={`ml-auto px-2 py-0.5 rounded text-xs ${
                    stats.redis_cache.status === 'connected'
                      ? 'bg-green-500/20 text-green-400'
                      : 'bg-red-500/20 text-red-400'
                  }`}>
                    {stats.redis_cache.status}
                  </span>
                </div>
                {stats.redis_cache.cache_stats ? (
                  <div className="space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-gray-400 text-sm">Hit Rate</span>
                      <span className="text-green-400 font-semibold">
                        {stats.redis_cache.cache_stats.hit_rate_percent.toFixed(2)}%
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-400 text-sm">Total Requests</span>
                      <span className="text-white font-mono">
                        {formatNumber(stats.redis_cache.cache_stats.total_requests)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-400 text-sm">Cache Hits</span>
                      <span className="text-green-400 font-mono">
                        {formatNumber(stats.redis_cache.cache_stats.hits)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-gray-400 text-sm">Cache Misses</span>
                      <span className="text-orange-400 font-mono">
                        {formatNumber(stats.redis_cache.cache_stats.misses)}
                      </span>
                    </div>
                  </div>
                ) : (
                  <p className="text-gray-500 text-sm">No cache statistics available</p>
                )}
              </div>

              {/* Memory & Server Info */}
              <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700/50">
                <div className="flex items-center gap-2 mb-4">
                  <Server className="w-5 h-5 text-red-400" />
                  <h4 className="font-medium">Redis Server</h4>
                </div>
                <div className="space-y-3">
                  {stats.redis_cache.host && (
                    <div className="flex justify-between items-center">
                      <span className="text-gray-400 text-sm">Host</span>
                      <span className="text-white font-mono text-sm">
                        {stats.redis_cache.host}
                      </span>
                    </div>
                  )}
                  {stats.redis_cache.server && (
                    <>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-400 text-sm">Version</span>
                        <span className="text-white font-mono text-sm">
                          {stats.redis_cache.server.version}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-400 text-sm">Uptime</span>
                        <span className="text-white font-mono text-sm">
                          {stats.redis_cache.server.uptime_days} days
                        </span>
                      </div>
                    </>
                  )}
                  {stats.redis_cache.memory && (
                    <>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-400 text-sm">Memory Used</span>
                        <span className="text-purple-400 font-mono text-sm">
                          {stats.redis_cache.memory.used_memory}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-400 text-sm">Peak Memory</span>
                        <span className="text-purple-300 font-mono text-sm">
                          {stats.redis_cache.memory.used_memory_peak}
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-400 text-sm">Clients</span>
                        <span className="text-cyan-400 font-mono text-sm">
                          {stats.redis_cache.memory.connected_clients}
                        </span>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
          </Section>
        )}

        {/* Vector Database Section */}
        <Section title="Vector Database (pgvector)" icon={Zap} color="blue">
          <div className="grid md:grid-cols-2 gap-6">
            {/* Movie Embeddings */}
            <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700/50">
              <div className="flex items-center gap-2 mb-4">
                <Film className="w-5 h-5 text-blue-400" />
                <h4 className="font-medium">Movie Embeddings</h4>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Coverage</span>
                  <span className="text-blue-400 font-mono">
                    {stats.vector_db?.movies_with_embeddings?.toLocaleString()} / {stats.vector_db?.total_movies?.toLocaleString()}
                  </span>
                </div>
                <div className="h-3 bg-gray-700 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-blue-600 to-blue-400 transition-all duration-500"
                    style={{ width: `${stats.vector_db?.embedding_coverage_percent ?? 0}%` }}
                  />
                </div>
                <div className="text-right text-sm font-mono text-blue-400">
                  {stats.vector_db?.embedding_coverage_percent?.toFixed(1)}%
                </div>
              </div>
            </div>

            {/* Review Embeddings */}
            <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700/50">
              <div className="flex items-center gap-2 mb-4">
                <Star className="w-5 h-5 text-green-400" />
                <h4 className="font-medium">Review Embeddings</h4>
              </div>
              <div className="space-y-3">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-400">Coverage</span>
                  <span className="text-green-400 font-mono">
                    {stats.review_vector_db?.reviews_with_embeddings?.toLocaleString()} / {stats.review_vector_db?.total_reviews?.toLocaleString()}
                  </span>
                </div>
                <div className="h-3 bg-gray-700 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-gradient-to-r from-green-600 to-green-400 transition-all duration-500"
                    style={{ width: `${stats.review_vector_db?.embedding_coverage_percent ?? 0}%` }}
                  />
                </div>
                <div className="text-right text-sm font-mono text-green-400">
                  {stats.review_vector_db?.embedding_coverage_percent?.toFixed(1)}%
                </div>
              </div>
            </div>

            {/* Vector Config */}
            {stats.vector_config && (
              <div className="md:col-span-2 bg-gray-800/30 rounded-xl p-5 border border-gray-700/30">
                <div className="flex items-center gap-2 mb-4">
                  <Cpu className="w-5 h-5 text-purple-400" />
                  <h4 className="font-medium">Vector Configuration</h4>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <ConfigItem label="Dimensions" value={stats.vector_config.embedding_dimensions} />
                  <ConfigItem label="Model" value={stats.vector_config.embedding_model} />
                  <ConfigItem label="Distance" value={stats.vector_config.distance_metric} />
                  <ConfigItem label="Index" value={stats.vector_config.index_type} />
                </div>
              </div>
            )}
          </div>
        </Section>

        {/* Movie Statistics */}
        <Section title="Movie Statistics" icon={Film} color="indigo">
          <div className="grid md:grid-cols-3 gap-4 mb-6">
            <MetricCard label="Year Range" value={`${stats.movies?.earliest_year} — ${stats.movies?.latest_year}`} icon={TrendingUp} />
            <MetricCard label="Rating Range" value={`${stats.movies?.min_rating} — ${stats.movies?.max_rating}`} icon={Star} />
            <MetricCard label="Avg Runtime" value={formatRuntime(stats.movies?.avg_runtime ?? 0)} icon={Clock} />
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            {/* Rating Distribution */}
            <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700/50">
              <h4 className="font-medium mb-4 flex items-center gap-2">
                <Star className="w-4 h-4 text-yellow-400" />
                Rating Distribution
              </h4>
              <div className="space-y-2">
                {stats.rating_distribution?.map((bucket) => (
                  <DistributionBar
                    key={bucket.rating_bucket}
                    label={bucket.rating_bucket}
                    count={bucket.count}
                    maxCount={Math.max(...stats.rating_distribution.map(r => r.count))}
                    color="yellow"
                  />
                ))}
              </div>
            </div>

            {/* Runtime Distribution */}
            <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700/50">
              <h4 className="font-medium mb-4 flex items-center gap-2">
                <Clock className="w-4 h-4 text-cyan-400" />
                Runtime Distribution
              </h4>
              <div className="space-y-2">
                {stats.runtime_distribution?.map((runtime) => (
                  <DistributionBar
                    key={runtime.runtime_category}
                    label={runtime.runtime_category}
                    count={runtime.count}
                    maxCount={Math.max(...stats.runtime_distribution.map(r => r.count))}
                    color="cyan"
                  />
                ))}
              </div>
            </div>
          </div>
        </Section>

        {/* Genre & Decade Analysis */}
        <Section title="Genre & Decade Analysis" icon={BarChart3} color="green">
          <div className="grid md:grid-cols-2 gap-6">
            {/* Genre Distribution */}
            <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700/50">
              <h4 className="font-medium mb-4 flex items-center gap-2">
                <Layers className="w-4 h-4 text-purple-400" />
                Top Genres
              </h4>
              <div className="space-y-2 max-h-80 overflow-y-auto pr-2">
                {stats.genre_distribution?.map((genre) => (
                  <DistributionBar
                    key={genre.genre}
                    label={genre.genre}
                    count={genre.count}
                    maxCount={maxGenreCount}
                    color="purple"
                  />
                ))}
              </div>
            </div>

            {/* Decade Distribution */}
            <div className="bg-gray-800/50 rounded-xl p-5 border border-gray-700/50">
              <h4 className="font-medium mb-4 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-emerald-400" />
                Movies by Decade
              </h4>
              <div className="space-y-2 max-h-80 overflow-y-auto pr-2">
                {stats.decade_distribution?.map((decade) => (
                  <DistributionBar
                    key={decade.decade}
                    label={`${decade.decade}s`}
                    count={decade.count}
                    maxCount={maxDecadeCount}
                    color="emerald"
                    subValue={`★ ${decade.avg_rating}`}
                  />
                ))}
              </div>
            </div>
          </div>
        </Section>

        {/* Top Directors */}
        <Section title="Top Directors" icon={Users} color="orange">
          <div className="grid md:grid-cols-2 lg:grid-cols-5 gap-4">
            {stats.top_directors?.map((director, index) => (
              <div
                key={director.director}
                className="bg-gray-800/50 rounded-xl p-4 border border-gray-700/50 hover:border-orange-500/30 transition-colors"
              >
                <div className="flex items-start gap-3">
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center text-sm font-bold ${
                    index === 0 ? 'bg-yellow-500/20 text-yellow-400' :
                    index === 1 ? 'bg-gray-400/20 text-gray-300' :
                    index === 2 ? 'bg-orange-600/20 text-orange-400' :
                    'bg-gray-700/50 text-gray-400'
                  }`}>
                    #{index + 1}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="font-medium truncate text-sm">{director.director}</p>
                    <p className="text-xs text-gray-400">{director.movie_count} movies</p>
                    <p className="text-xs text-yellow-400">★ {director.avg_rating}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Section>

        {/* Technical Footer */}
        <div className="mt-6 p-4 bg-gray-800/30 rounded-xl border border-gray-700/30">
          <div className="flex flex-wrap gap-4 text-xs text-gray-500">
            <span className="flex items-center gap-1">
              <Database className="w-3 h-3" /> PostgreSQL 15
            </span>
            <span className="flex items-center gap-1">
              <Zap className="w-3 h-3" /> pgvector extension
            </span>
            <span className="flex items-center gap-1">
              <Hash className="w-3 h-3" /> IVFFlat indexing
            </span>
            <span className="flex items-center gap-1">
              <Cpu className="w-3 h-3" /> text-embedding-3-small
            </span>
            <span className="flex items-center gap-1">
              <Clock className="w-3 h-3" /> Total Runtime: {formatRuntime(stats.movies?.total_runtime_minutes ?? 0)} ({Math.round((stats.movies?.total_runtime_minutes ?? 0) / 60 / 24)} days)
            </span>
          </div>
        </div>
      </main>
    </div>
  );
}

// Helper Components

function StatCard({ icon: Icon, label, value, subValue, color }: {
  icon: React.ElementType;
  label: string;
  value: string;
  subValue?: string;
  color: string;
}) {
  const colors: Record<string, string> = {
    blue: 'bg-blue-500/20 text-blue-400 border-blue-500/30',
    yellow: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30',
    green: 'bg-green-500/20 text-green-400 border-green-500/30',
    purple: 'bg-purple-500/20 text-purple-400 border-purple-500/30',
  };

  return (
    <div className={`rounded-xl p-4 border ${colors[color]}`}>
      <Icon className="w-5 h-5 mb-2" />
      <p className="text-2xl font-bold text-white">{value}</p>
      <p className="text-xs text-gray-400">{label}</p>
      {subValue && <p className="text-xs mt-1 opacity-70">{subValue}</p>}
    </div>
  );
}

function Section({ title, icon: Icon, color, children }: {
  title: string;
  icon: React.ElementType;
  color: string;
  children: React.ReactNode;
}) {
  const colors: Record<string, string> = {
    blue: 'text-blue-400',
    green: 'text-green-400',
    purple: 'text-purple-400',
    orange: 'text-orange-400',
    indigo: 'text-indigo-400',
    gray: 'text-gray-400',
  };

  return (
    <section className="mb-10">
      <h3 className={`text-lg font-semibold mb-4 flex items-center gap-2 ${colors[color]}`}>
        <Icon className="w-5 h-5" />
        {title}
      </h3>
      {children}
    </section>
  );
}

function MetricCard({ label, value, icon: Icon }: {
  label: string;
  value: string;
  icon: React.ElementType;
}) {
  return (
    <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700/50">
      <div className="flex items-center gap-2 text-gray-400 text-sm mb-1">
        <Icon className="w-4 h-4" />
        {label}
      </div>
      <p className="text-lg font-semibold">{value}</p>
    </div>
  );
}

function ConfigItem({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="text-center">
      <p className="text-xs text-gray-500 mb-1">{label}</p>
      <p className="text-sm font-mono text-purple-400">{value}</p>
    </div>
  );
}

function DistributionBar({ label, count, maxCount, color, subValue }: {
  label: string;
  count: number;
  maxCount: number;
  color: string;
  subValue?: string;
}) {
  const colors: Record<string, string> = {
    yellow: 'bg-yellow-500/60',
    cyan: 'bg-cyan-500/60',
    purple: 'bg-purple-500/60',
    emerald: 'bg-emerald-500/60',
  };

  const percentage = (count / maxCount) * 100;

  return (
    <div className="group">
      <div className="flex justify-between text-xs mb-1">
        <span className="text-gray-400 truncate flex-1">{label}</span>
        <span className="text-gray-500 ml-2 flex items-center gap-2">
          {subValue && <span className="text-yellow-400">{subValue}</span>}
          <span className="font-mono">{count.toLocaleString()}</span>
        </span>
      </div>
      <div className="h-2 bg-gray-700/50 rounded-full overflow-hidden">
        <div
          className={`h-full ${colors[color]} rounded-full transition-all duration-300 group-hover:opacity-80`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

function StorageItem({ label, value, icon: Icon, highlight }: {
  label: string;
  value: string;
  icon: React.ElementType;
  highlight?: boolean;
}) {
  return (
    <div className="flex items-center justify-between">
      <div className="flex items-center gap-2 text-gray-400">
        <Icon className="w-4 h-4" />
        <span className="text-sm">{label}</span>
      </div>
      <span className={`font-mono text-sm ${highlight ? 'text-blue-400 font-semibold' : 'text-gray-300'}`}>
        {value}
      </span>
    </div>
  );
}
