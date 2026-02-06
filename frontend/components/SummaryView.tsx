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
          <div className="flex items-center gap-3 mb-6">
            <span className="text-3xl">🔥</span>
            <h2 className="text-2xl font-bold text-gray-900">
              今日精选 (Top {summary.highlights.length})
            </h2>
          </div>
          <div className="space-y-6">
            {summary.highlights.map((tweet) => (
              <TweetCard key={tweet.id} tweet={tweet} variant="full" />
            ))}
          </div>
        </section>
      )}

      {/* More AI News Section (Compact Display) */}
      {summary.other_news && summary.other_news.length > 0 && (
        <section>
          <div className="flex items-center gap-3 mb-6">
            <span className="text-3xl">📰</span>
            <h2 className="text-2xl font-bold text-gray-900">
              更多AI资讯 ({summary.other_news.length} 条)
            </h2>
          </div>
          <div className="space-y-3">
            {summary.other_news.map((tweet) => (
              <TweetCard key={tweet.id} tweet={tweet} variant="compact" />
            ))}
          </div>
        </section>
      )}

      {/* Empty state */}
      {(!summary.highlights || summary.highlights.length === 0) &&
        (!summary.other_news || summary.other_news.length === 0) && (
          <div className="text-center py-12">
            <p className="text-gray-500 text-lg">No AI news found for this day.</p>
          </div>
        )}
    </div>
  );
}
