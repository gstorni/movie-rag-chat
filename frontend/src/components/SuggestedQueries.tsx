import React from 'react';
import { Sparkles } from 'lucide-react';

interface SuggestedQueriesProps {
  onSelect: (query: string) => void;
}

const suggestions = [
  'What are the best sci-fi movies about AI?',
  'Find movies directed by Christopher Nolan',
  'Movies about space exploration',
  'What horror movies are in the database?',
  'Recommend a thought-provoking drama',
  'How many movies are from the 90s?',
];

export function SuggestedQueries({ onSelect }: SuggestedQueriesProps) {
  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 text-gray-400 text-sm">
        <Sparkles className="w-4 h-4" />
        <span>Try asking:</span>
      </div>
      <div className="flex flex-wrap gap-2">
        {suggestions.map((query) => (
          <button
            key={query}
            onClick={() => onSelect(query)}
            className="px-3 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 text-sm rounded-lg border border-gray-700 hover:border-gray-600 transition-colors"
          >
            {query}
          </button>
        ))}
      </div>
    </div>
  );
}
