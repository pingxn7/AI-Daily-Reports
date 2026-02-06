import React from 'react';

interface HighlightsSummaryProps {
  summary: string;
  tweetCount: number;
  topTweetsCount: number;
  topics: string[] | null;
}

export function HighlightsSummary({
  summary,
  tweetCount,
  topTweetsCount,
  topics,
}: HighlightsSummaryProps) {
  return (
    <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-6 mb-8 border border-blue-100 shadow-sm">
      <div className="flex items-center gap-2 mb-4">
        <span className="text-2xl">📌</span>
        <h2 className="text-xl font-bold text-gray-900">今日关键亮点</h2>
      </div>

      {/* AI-generated summary */}
      <div className="prose prose-sm max-w-none mb-4">
        <div className="text-gray-700 leading-relaxed whitespace-pre-line">
          {summary}
        </div>
      </div>

      {/* Statistics */}
      <div className="flex flex-wrap items-center gap-4 pt-4 border-t border-blue-200">
        <div className="flex items-center gap-2 text-sm">
          <span className="font-semibold text-blue-700">共收集:</span>
          <span className="text-gray-700">{tweetCount} 条AI相关推文</span>
        </div>
        <div className="flex items-center gap-2 text-sm">
          <span className="font-semibold text-purple-700">精选:</span>
          <span className="text-gray-700">{topTweetsCount} 条</span>
        </div>
        {topics && topics.length > 0 && (
          <div className="flex items-center gap-2 text-sm">
            <span className="font-semibold text-gray-700">热门话题:</span>
            <div className="flex flex-wrap gap-1">
              {topics.slice(0, 5).map((topic, index) => (
                <span
                  key={index}
                  className="px-2 py-0.5 bg-white text-gray-700 text-xs rounded border border-gray-300"
                >
                  {topic}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
