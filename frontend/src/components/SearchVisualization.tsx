import React, { useEffect, useState } from 'react';
import { Database, Brain, Cpu, Search, Zap, CheckCircle2, Loader2, Coins } from 'lucide-react';
import { TokenUsage } from '../services/chatService';

interface SearchStep {
  id: string;
  label: string;
  description: string;
  icon: React.ElementType;
  status: 'pending' | 'active' | 'complete';
  result?: string;
  color: string;
}

interface SearchVisualizationProps {
  isSearching: boolean;
  currentPhase: 'idle' | 'analyzing' | 'vector_search' | 'sql_search' | 'generating' | 'complete';
  sources?: {
    vector_matches: number;
    sql_matches: number;
    used_statistics: boolean;
  };
  intent?: string;
  tokenUsage?: {
    intent_analysis: TokenUsage;
    response_generation: TokenUsage;
    total: TokenUsage;
  };
}

export function SearchVisualization({ isSearching, currentPhase, sources, intent, tokenUsage }: SearchVisualizationProps) {
  const [steps, setSteps] = useState<SearchStep[]>([
    {
      id: 'analyze',
      label: 'Intent Analysis',
      description: 'Understanding your query...',
      icon: Brain,
      status: 'pending',
      color: 'purple'
    },
    {
      id: 'vector',
      label: 'Vector Search',
      description: 'Searching semantically similar content...',
      icon: Zap,
      status: 'pending',
      color: 'blue'
    },
    {
      id: 'sql',
      label: 'SQL Query',
      description: 'Querying structured database...',
      icon: Database,
      status: 'pending',
      color: 'green'
    },
    {
      id: 'generate',
      label: 'AI Response',
      description: 'Generating intelligent response...',
      icon: Cpu,
      status: 'pending',
      color: 'orange'
    }
  ]);

  useEffect(() => {
    if (!isSearching && currentPhase === 'idle') {
      // Reset all steps
      setSteps(prev => prev.map(s => ({ ...s, status: 'pending', result: undefined })));
      return;
    }

    setSteps(prev => prev.map(step => {
      let newStatus: 'pending' | 'active' | 'complete' = step.status;
      let result = step.result;

      switch (step.id) {
        case 'analyze':
          if (currentPhase === 'analyzing') {
            newStatus = 'active';
          } else if (['vector_search', 'sql_search', 'generating', 'complete'].includes(currentPhase)) {
            newStatus = 'complete';
            result = intent ? `Intent: ${intent}` : 'Query analyzed';
          }
          break;
        case 'vector':
          if (currentPhase === 'vector_search') {
            newStatus = 'active';
          } else if (['sql_search', 'generating', 'complete'].includes(currentPhase)) {
            newStatus = 'complete';
            result = sources ? `${sources.vector_matches} semantic matches` : 'Completed';
          }
          break;
        case 'sql':
          if (currentPhase === 'sql_search') {
            newStatus = 'active';
          } else if (['generating', 'complete'].includes(currentPhase)) {
            newStatus = 'complete';
            result = sources ? `${sources.sql_matches} database matches` : 'Completed';
          }
          break;
        case 'generate':
          if (currentPhase === 'generating') {
            newStatus = 'active';
          } else if (currentPhase === 'complete') {
            newStatus = 'complete';
            result = 'Response generated';
          }
          break;
      }

      return { ...step, status: newStatus, result };
    }));
  }, [currentPhase, isSearching, sources, intent]);

  if (!isSearching && currentPhase === 'idle') {
    return null;
  }

  const getStatusIcon = (step: SearchStep) => {
    if (step.status === 'active') {
      return <Loader2 className="w-5 h-5 animate-spin" />;
    }
    if (step.status === 'complete') {
      return <CheckCircle2 className="w-5 h-5" />;
    }
    return <step.icon className="w-5 h-5" />;
  };

  const getColorClasses = (step: SearchStep) => {
    const colors: Record<string, { bg: string; border: string; text: string; glow: string }> = {
      purple: {
        bg: 'bg-purple-500/20',
        border: 'border-purple-500/50',
        text: 'text-purple-400',
        glow: 'shadow-purple-500/20'
      },
      blue: {
        bg: 'bg-blue-500/20',
        border: 'border-blue-500/50',
        text: 'text-blue-400',
        glow: 'shadow-blue-500/20'
      },
      green: {
        bg: 'bg-green-500/20',
        border: 'border-green-500/50',
        text: 'text-green-400',
        glow: 'shadow-green-500/20'
      },
      orange: {
        bg: 'bg-orange-500/20',
        border: 'border-orange-500/50',
        text: 'text-orange-400',
        glow: 'shadow-orange-500/20'
      }
    };
    return colors[step.color] || colors.blue;
  };

  return (
    <div className="mb-4 sm:mb-6 p-2 sm:p-4 bg-gray-800/50 rounded-lg sm:rounded-xl border border-gray-700/50">
      <div className="flex items-center gap-2 mb-2 sm:mb-4 text-gray-400 text-[10px] sm:text-sm">
        <Search className="w-3 h-3 sm:w-4 sm:h-4" />
        <span>Search Pipeline</span>
      </div>

      <div className="grid grid-cols-4 gap-1 sm:gap-3">
        {steps.map((step, index) => {
          const colors = getColorClasses(step);
          const isActive = step.status === 'active';
          const isComplete = step.status === 'complete';

          return (
            <div
              key={step.id}
              className={`relative p-1.5 sm:p-3 rounded-md sm:rounded-lg border transition-all duration-300 ${
                isActive
                  ? `${colors.bg} ${colors.border} shadow-lg ${colors.glow}`
                  : isComplete
                  ? `${colors.bg} ${colors.border} opacity-90`
                  : 'bg-gray-800/30 border-gray-700/30 opacity-50'
              }`}
            >
              {/* Connection line - hidden on mobile */}
              {index < steps.length - 1 && (
                <div
                  className={`absolute top-1/2 -right-1 sm:-right-3 w-1 sm:w-3 h-0.5 hidden sm:block ${
                    isComplete ? colors.bg : 'bg-gray-700'
                  }`}
                />
              )}

              <div className="flex flex-col items-center text-center">
                <div className={`mb-1 sm:mb-2 ${isActive || isComplete ? colors.text : 'text-gray-500'}`}>
                  <step.icon className={`w-3 h-3 sm:w-5 sm:h-5 ${step.status === 'active' ? 'animate-pulse' : ''}`} />
                </div>
                <div className={`text-[8px] sm:text-xs font-medium leading-tight ${isActive || isComplete ? 'text-white' : 'text-gray-500'}`}>
                  <span className="hidden sm:inline">{step.label}</span>
                  <span className="sm:hidden">{step.label.split(' ')[0]}</span>
                </div>
                {step.result && isComplete && (
                  <div className={`text-[7px] sm:text-xs mt-0.5 sm:mt-1 ${colors.text} hidden sm:block`}>
                    {step.result}
                  </div>
                )}
                {isActive && (
                  <div className="text-[7px] sm:text-xs mt-0.5 sm:mt-1 text-gray-400 hidden sm:block">
                    {step.description}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Data flow visualization - hidden on mobile for compact view */}
      {currentPhase === 'complete' && sources && (
        <div className="mt-2 sm:mt-4 pt-2 sm:pt-4 border-t border-gray-700/50 hidden sm:block">
          <div className="flex justify-center gap-3 sm:gap-6 flex-wrap">
            {sources.vector_matches > 0 && (
              <div className="flex items-center gap-2 px-2 sm:px-3 py-1.5 sm:py-2 bg-blue-500/10 rounded-lg border border-blue-500/30">
                <div className="w-6 h-6 sm:w-8 sm:h-8 bg-blue-500/20 rounded-full flex items-center justify-center">
                  <Zap className="w-3 h-3 sm:w-4 sm:h-4 text-blue-400" />
                </div>
                <div>
                  <div className="text-xs sm:text-sm font-medium text-blue-400">pgvector</div>
                  <div className="text-[10px] sm:text-xs text-gray-500">{sources.vector_matches} matches</div>
                </div>
              </div>
            )}

            {sources.sql_matches > 0 && (
              <div className="flex items-center gap-2 px-2 sm:px-3 py-1.5 sm:py-2 bg-green-500/10 rounded-lg border border-green-500/30">
                <div className="w-6 h-6 sm:w-8 sm:h-8 bg-green-500/20 rounded-full flex items-center justify-center">
                  <Database className="w-3 h-3 sm:w-4 sm:h-4 text-green-400" />
                </div>
                <div>
                  <div className="text-xs sm:text-sm font-medium text-green-400">PostgreSQL</div>
                  <div className="text-[10px] sm:text-xs text-gray-500">{sources.sql_matches} results</div>
                </div>
              </div>
            )}

            {sources.used_statistics && (
              <div className="flex items-center gap-2 px-2 sm:px-3 py-1.5 sm:py-2 bg-amber-500/10 rounded-lg border border-amber-500/30">
                <div className="w-6 h-6 sm:w-8 sm:h-8 bg-amber-500/20 rounded-full flex items-center justify-center">
                  <Database className="w-3 h-3 sm:w-4 sm:h-4 text-amber-400" />
                </div>
                <div>
                  <div className="text-xs sm:text-sm font-medium text-amber-400">Stats</div>
                  <div className="text-[10px] sm:text-xs text-gray-500">Aggregated</div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Token Usage Display - hidden on mobile */}
      {currentPhase === 'complete' && tokenUsage && (
        <div className="mt-2 sm:mt-4 pt-2 sm:pt-4 border-t border-gray-700/50 hidden sm:block">
          <div className="flex items-center justify-center gap-2 mb-2 sm:mb-3">
            <Coins className="w-3 h-3 sm:w-4 sm:h-4 text-indigo-400" />
            <span className="text-[10px] sm:text-xs text-gray-400 font-medium">Token Usage</span>
          </div>
          <div className="flex justify-center gap-2 sm:gap-4 flex-wrap">
            {/* Intent Analysis Tokens */}
            <div className="px-2 sm:px-3 py-1.5 sm:py-2 bg-purple-500/10 rounded-lg border border-purple-500/30">
              <div className="text-[10px] sm:text-xs text-purple-400 font-medium mb-0.5 sm:mb-1">Intent</div>
              <div className="flex gap-2 sm:gap-3 text-[10px] sm:text-xs">
                <span className="text-gray-400">
                  <span className="text-purple-300 font-mono">{tokenUsage.intent_analysis.prompt_tokens}</span>
                </span>
                <span className="text-gray-400">
                  <span className="text-purple-300 font-mono">{tokenUsage.intent_analysis.completion_tokens}</span>
                </span>
              </div>
            </div>

            {/* Response Generation Tokens */}
            <div className="px-2 sm:px-3 py-1.5 sm:py-2 bg-orange-500/10 rounded-lg border border-orange-500/30">
              <div className="text-[10px] sm:text-xs text-orange-400 font-medium mb-0.5 sm:mb-1">Response</div>
              <div className="flex gap-2 sm:gap-3 text-[10px] sm:text-xs">
                <span className="text-gray-400">
                  <span className="text-orange-300 font-mono">{tokenUsage.response_generation.prompt_tokens}</span>
                </span>
                <span className="text-gray-400">
                  <span className="text-orange-300 font-mono">{tokenUsage.response_generation.completion_tokens}</span>
                </span>
              </div>
            </div>

            {/* Total */}
            <div className="px-2 sm:px-3 py-1.5 sm:py-2 bg-indigo-500/10 rounded-lg border border-indigo-500/30">
              <div className="text-[10px] sm:text-xs text-indigo-400 font-medium mb-0.5 sm:mb-1">Total</div>
              <div className="flex items-center gap-1 sm:gap-2">
                <span className="text-indigo-300 font-mono font-bold text-xs sm:text-sm">{tokenUsage.total.total_tokens.toLocaleString()}</span>
              </div>
              <div className="text-[9px] sm:text-xs text-gray-500">
                ~${((tokenUsage.total.prompt_tokens * 0.00015 + tokenUsage.total.completion_tokens * 0.0006) / 1000).toFixed(5)}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
