import React from 'react';
import { DailySummaryDetail } from '@/lib/api';
import { EventBasedSummary } from './EventBasedSummary';
import { TweetCard } from './TweetCard';

interface SummaryViewProps {
  summary: DailySummaryDetail;
}

export function SummaryView({ summary }: SummaryViewProps) {
  // 限制更多资讯最多显示10条
  const limitedOtherNews = summary.other_news?.slice(0, 10) || [];

  return (
    <div className="max-w-5xl mx-auto">
      {/* Event-Based Summary Section */}
      {summary.highlights_summary && (
        <EventBasedSummary
          summary={summary.highlights_summary}
          tweetCount={summary.tweet_count}
          topTweetsCount={summary.top_tweets_count}
          topics={summary.topics}
        />
      )}

      {/* More AI News Section (Compact Display) - 限制10条 */}
      {limitedOtherNews.length > 0 && (
        <section className="mt-8">
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
                  精选 {limitedOtherNews.length} 条值得关注的 AI 相关动态
                </p>
              </div>
              <div className="bg-gradient-to-br from-blue-100 to-indigo-100 rounded-xl px-6 py-3">
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600">
                    {limitedOtherNews.length}
                  </div>
                  <div className="text-xs text-blue-700 font-semibold">精选资讯</div>
                </div>
              </div>
            </div>
          </div>
          <div className="grid gap-4">
            {limitedOtherNews.map((tweet) => (
              <TweetCard key={tweet.id} tweet={tweet} variant="compact" />
            ))}
          </div>
        </section>
      )}

      {/* Empty state */}
      {!summary.highlights_summary && limitedOtherNews.length === 0 && (
        <div className="text-center py-20 bg-white rounded-2xl shadow-lg border-2 border-gray-100">
          <div className="text-6xl mb-4">📭</div>
          <p className="text-gray-500 text-xl font-medium">暂无 AI 资讯</p>
          <p className="text-gray-400 text-sm mt-2">今天还没有收集到相关内容</p>
        </div>
      )}
    </div>
  );
}
