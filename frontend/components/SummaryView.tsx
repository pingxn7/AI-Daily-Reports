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
        <section className="mb-12">
          <div className="bg-white rounded-2xl p-6 mb-6 border-2 border-gray-100 shadow-lg">
            <div className="flex items-center gap-4">
              <div className="bg-gradient-to-br from-orange-400 to-red-500 rounded-xl p-4 shadow-md">
                <span className="text-4xl">🔥</span>
              </div>
              <div className="flex-1">
                <h2 className="text-3xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
                  今日精选推文
                </h2>
                <p className="text-gray-600 mt-1">
                  精心挑选的 {summary.highlights.length} 条最重要的 AI 资讯
                </p>
              </div>
              <div className="bg-gradient-to-br from-orange-100 to-red-100 rounded-xl px-6 py-3">
                <div className="text-center">
                  <div className="text-3xl font-bold text-orange-600">
                    {summary.highlights.length}
                  </div>
                  <div className="text-xs text-orange-700 font-semibold">精选内容</div>
                </div>
              </div>
            </div>
          </div>
          <div className="space-y-6">
            {summary.highlights.map((tweet, index) => (
              <div key={tweet.id} className="relative">
                {/* Tweet number badge */}
                <div className="absolute -left-4 top-6 z-10 bg-gradient-to-br from-orange-500 to-red-600 text-white rounded-full w-10 h-10 flex items-center justify-center text-lg font-bold shadow-lg">
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
          <div className="bg-white rounded-2xl p-6 mb-6 border-2 border-gray-100 shadow-lg">
            <div className="flex items-center gap-4">
              <div className="bg-gradient-to-br from-blue-400 to-indigo-500 rounded-xl p-4 shadow-md">
                <span className="text-4xl">📰</span>
              </div>
              <div className="flex-1">
                <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  更多 AI 资讯
                </h2>
                <p className="text-gray-600 mt-1">
                  其他值得关注的 {summary.other_news.length} 条 AI 相关动态
                </p>
              </div>
              <div className="bg-gradient-to-br from-blue-100 to-indigo-100 rounded-xl px-6 py-3">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">
                    {summary.other_news.length}
                  </div>
                  <div className="text-xs text-blue-700 font-semibold">更多资讯</div>
                </div>
              </div>
            </div>
          </div>
          <div className="grid gap-4">
            {summary.other_news.map((tweet) => (
              <TweetCard key={tweet.id} tweet={tweet} variant="compact" />
            ))}
          </div>
        </section>
      )}

      {/* Empty state */}
      {(!summary.highlights || summary.highlights.length === 0) &&
        (!summary.other_news || summary.other_news.length === 0) && (
          <div className="text-center py-20 bg-white rounded-2xl shadow-lg border-2 border-gray-100">
            <div className="text-6xl mb-4">📭</div>
            <p className="text-gray-500 text-xl font-medium">暂无 AI 资讯</p>
            <p className="text-gray-400 text-sm mt-2">今天还没有收集到相关内容</p>
          </div>
        )}
    </div>
  );
}
