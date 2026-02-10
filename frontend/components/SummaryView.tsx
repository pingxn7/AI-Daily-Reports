import React from 'react';
import { DailySummaryDetail } from '@/lib/api';
import { HighlightsSummary } from './HighlightsSummary';
import { TweetCard } from './TweetCard';

interface SummaryViewProps {
  summary: DailySummaryDetail;
}

export function SummaryView({ summary }: SummaryViewProps) {
  return (
    <div className="max-w-5xl mx-auto">
      {/* Highlights Summary Section */}
      {summary.highlights_summary && (
        <HighlightsSummary
          summary={summary.highlights_summary}
          tweetCount={summary.tweet_count}
          topTweetsCount={summary.top_tweets_count}
          topics={summary.topics}
        />
      )}

      {/* Top 10 Curated Highlights Section */}
      {summary.highlights && summary.highlights.length > 0 && (
        <section className="mb-8">
          <div className="bg-gradient-to-br from-orange-50 to-red-50 rounded-xl p-5 mb-5 border border-orange-200 shadow-md">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-orange-500 to-red-600 rounded-xl p-3 shadow-sm">
                <span className="text-3xl">🔥</span>
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold text-gray-900">
                  今日精选事件
                </h2>
                <p className="text-gray-700 text-sm font-medium">
                  精心挑选的 {summary.highlights.length} 条最重要的 AI 资讯
                </p>
              </div>
              <div className="bg-white rounded-lg px-4 py-2 shadow-sm border border-orange-300">
                <div className="text-center">
                  <div className="text-2xl font-bold text-orange-600">
                    {summary.highlights.length}
                  </div>
                  <div className="text-xs text-orange-700 font-semibold">精选内容</div>
                </div>
              </div>
            </div>
          </div>
          <div className="space-y-4">
            {summary.highlights.map((tweet, index) => (
              <div key={tweet.id} className="relative">
                {/* Tweet number badge */}
                <div className="absolute -left-3 top-5 z-10 bg-gradient-to-br from-orange-500 to-red-600 text-white rounded-full w-9 h-9 flex items-center justify-center text-base font-bold shadow-md border-2 border-white">
                  {index + 1}
                </div>
                <TweetCard tweet={tweet} variant="full" />
              </div>
            ))}
          </div>
        </section>
      )}

      {/* More AI News Section (Compact Display) */}
      {summary.other_news && summary.other_news.length > 0 && (
        <section>
          <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-5 mb-5 border border-blue-200 shadow-md">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-blue-400 to-indigo-500 rounded-xl p-3 shadow-sm">
                <span className="text-3xl">📰</span>
              </div>
              <div className="flex-1">
                <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  更多 AI 资讯
                </h2>
                <p className="text-gray-600 text-sm">
                  其他值得关注的 {summary.other_news.length} 条 AI 相关动态
                </p>
              </div>
              <div className="bg-white rounded-lg px-4 py-2 shadow-sm border border-blue-300">
                <div className="text-center">
                  <div className="text-2xl font-bold text-blue-600">
                    {summary.other_news.length}
                  </div>
                  <div className="text-xs text-blue-700 font-semibold">更多资讯</div>
                </div>
              </div>
            </div>
          </div>
          <div className="grid gap-3">
            {summary.other_news.map((tweet) => (
              <TweetCard key={tweet.id} tweet={tweet} variant="compact" />
            ))}
          </div>
        </section>
      )}

      {/* Empty state */}
      {(!summary.highlights || summary.highlights.length === 0) &&
        (!summary.other_news || summary.other_news.length === 0) && (
          <div className="text-center py-16 bg-gradient-to-br from-gray-50 to-blue-50 rounded-xl shadow-sm border border-gray-200">
            <div className="text-5xl mb-3">📭</div>
            <p className="text-gray-500 text-lg font-medium">暂无 AI 资讯</p>
            <p className="text-gray-400 text-sm mt-1">今天还没有收集到相关内容</p>
          </div>
        )}
    </div>
  );
}
