import React from 'react';
import { Bot } from 'lucide-react';

export function TypingIndicator() {
  return (
    <div className="flex gap-4">
      {/* Avatar */}
      <div className="flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center bg-emerald-600">
        <Bot className="w-5 h-5 text-white" />
      </div>

      {/* Typing animation */}
      <div className="flex items-center gap-1 px-4 py-3 bg-gray-700 rounded-2xl rounded-tl-md">
        <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot" />
        <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot" />
        <div className="w-2 h-2 bg-gray-400 rounded-full typing-dot" />
      </div>
    </div>
  );
}
