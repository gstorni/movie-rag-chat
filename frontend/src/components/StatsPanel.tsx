import React from 'react';
import { Film, Star, Calendar, Users } from 'lucide-react';

interface StatsPanelProps {
  stats: {
    total_movies: number;
    avg_rating: number;
    earliest_year: number;
    latest_year: number;
    unique_directors: number;
  } | null;
}

export function StatsPanel({ stats }: StatsPanelProps) {
  if (!stats) return null;

  const items = [
    { icon: Film, label: 'Movies', value: stats.total_movies },
    { icon: Star, label: 'Avg Rating', value: stats.avg_rating?.toFixed(1) },
    { icon: Calendar, label: 'Years', value: `${stats.earliest_year}-${stats.latest_year}` },
    { icon: Users, label: 'Directors', value: stats.unique_directors },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {items.map(({ icon: Icon, label, value }) => (
        <div
          key={label}
          className="bg-gray-800/50 rounded-xl p-3 border border-gray-700/50"
        >
          <div className="flex items-center gap-2 text-gray-400 mb-1">
            <Icon className="w-4 h-4" />
            <span className="text-xs">{label}</span>
          </div>
          <p className="text-lg font-semibold text-white">{value}</p>
        </div>
      ))}
    </div>
  );
}
