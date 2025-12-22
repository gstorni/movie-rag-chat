import React from 'react';
import { User, Bot, Database, Search, BarChart3 } from 'lucide-react';

interface ChatMessageProps {
  role: 'user' | 'assistant';
  content: string;
  sources?: {
    vector_matches: number;
    sql_matches: number;
    used_statistics: boolean;
  };
  intent?: string;
}

export function ChatMessage({ role, content, sources, intent }: ChatMessageProps) {
  const isUser = role === 'user';

  return (
    <div className={`flex gap-4 ${isUser ? 'flex-row-reverse' : ''}`}>
      {/* Avatar */}
      <div
        className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
          isUser ? 'bg-indigo-600' : 'bg-emerald-600'
        }`}
      >
        {isUser ? (
          <User className="w-5 h-5 text-white" />
        ) : (
          <Bot className="w-5 h-5 text-white" />
        )}
      </div>

      {/* Message content */}
      <div className={`flex-1 max-w-[80%] ${isUser ? 'text-right' : ''}`}>
        <div
          className={`inline-block px-4 py-3 rounded-2xl ${
            isUser
              ? 'bg-indigo-600 text-white rounded-tr-md'
              : 'bg-gray-700 text-gray-100 rounded-tl-md'
          }`}
        >
          <p className="whitespace-pre-wrap text-sm leading-relaxed">{content}</p>
        </div>

        {/* Source indicators for assistant messages */}
        {!isUser && sources && (
          <div className="flex flex-wrap gap-2 mt-2">
            {sources.vector_matches > 0 && (
              <span className="inline-flex items-center gap-1 px-2 py-1 bg-purple-900/50 text-purple-300 text-xs rounded-full">
                <Search className="w-3 h-3" />
                {sources.vector_matches} semantic
              </span>
            )}
            {sources.sql_matches > 0 && (
              <span className="inline-flex items-center gap-1 px-2 py-1 bg-blue-900/50 text-blue-300 text-xs rounded-full">
                <Database className="w-3 h-3" />
                {sources.sql_matches} structured
              </span>
            )}
            {sources.used_statistics && (
              <span className="inline-flex items-center gap-1 px-2 py-1 bg-amber-900/50 text-amber-300 text-xs rounded-full">
                <BarChart3 className="w-3 h-3" />
                stats
              </span>
            )}
            {intent && (
              <span className="inline-flex items-center gap-1 px-2 py-1 bg-gray-800 text-gray-400 text-xs rounded-full">
                {intent}
              </span>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
