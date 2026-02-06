import React from 'react';
import Image from 'next/image';
import { ProcessedTweet, formatNumber, formatDate } from '@/lib/api';

interface TweetCardProps {
  tweet: ProcessedTweet;
  variant: 'full' | 'compact';
}

export function TweetCard({ tweet, variant }: TweetCardProps) {
  if (variant === 'full') {
    return (
      <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
        <div className="flex items-start gap-4">
          <div className="flex-1">
            {/* Author info */}
            <div className="flex items-center gap-2 mb-3">
              <span className="font-bold text-gray-900">
                {tweet.tweet.text.split('@')[0] || 'User'}
              </span>
              <span className="text-gray-500">
                {formatDate(tweet.tweet.created_at)}
              </span>
            </div>

            {/* Original tweet text */}
            <p className="text-gray-800 mb-4 leading-relaxed">
              {tweet.tweet.text}
            </p>

            {/* Screenshot */}
            {tweet.screenshot_url && (
              <div className="mb-4 rounded-lg overflow-hidden border border-gray-200">
                <Image
                  src={tweet.screenshot_url}
                  alt="Tweet screenshot"
                  width={800}
                  height={600}
                  className="w-full h-auto"
                  unoptimized
                />
              </div>
            )}

            {/* AI Summary */}
            {tweet.summary && (
              <div className="mb-3 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                <h4 className="font-semibold text-sm text-blue-900 mb-1">
                  🤖 AI Summary
                </h4>
                <p className="text-sm text-blue-800 leading-relaxed">
                  {tweet.summary}
                </p>
              </div>
            )}

            {/* Translation */}
            {tweet.translation && (
              <div className="mb-3 p-4 bg-gray-50 rounded-lg border-l-4 border-gray-400">
                <h4 className="font-semibold text-sm text-gray-900 mb-1">
                  🇨🇳 中文翻译
                </h4>
                <p className="text-sm text-gray-700 leading-relaxed">
                  {tweet.translation}
                </p>
              </div>
            )}

            {/* Topics */}
            {tweet.topics && tweet.topics.length > 0 && (
              <div className="mb-4 flex flex-wrap gap-2">
                {tweet.topics.map((topic, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-purple-100 text-purple-700 text-xs font-medium rounded-full"
                  >
                    {topic}
                  </span>
                ))}
              </div>
            )}

            {/* Engagement metrics */}
            <div className="flex items-center gap-6 text-sm text-gray-600 mb-4">
              <span className="flex items-center gap-1">
                <span>👍</span>
                <span className="font-medium">{formatNumber(tweet.tweet.like_count)}</span>
              </span>
              <span className="flex items-center gap-1">
                <span>🔄</span>
                <span className="font-medium">{formatNumber(tweet.tweet.retweet_count)}</span>
              </span>
              <span className="flex items-center gap-1">
                <span>💬</span>
                <span className="font-medium">{formatNumber(tweet.tweet.reply_count)}</span>
              </span>
              {tweet.tweet.bookmark_count > 0 && (
                <span className="flex items-center gap-1">
                  <span>🔖</span>
                  <span className="font-medium">{formatNumber(tweet.tweet.bookmark_count)}</span>
                </span>
              )}
              <span className="ml-auto text-xs text-gray-500">
                Importance: {tweet.importance_score.toFixed(1)}/10
              </span>
            </div>

            {/* Link to original */}
            <a
              href={tweet.tweet.tweet_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 font-medium text-sm transition-colors"
            >
              View original tweet
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
                />
              </svg>
            </a>
          </div>
        </div>
      </div>
    );
  }

  // Compact variant - for non-curated tweets
  return (
    <div className="bg-white rounded-lg shadow-sm p-4 hover:bg-gray-50 transition-colors border border-gray-200">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          {/* Author info */}
          <div className="flex items-center gap-2 text-sm mb-2">
            <span className="font-semibold text-gray-900 truncate">
              {tweet.tweet.text.split('@')[0] || 'User'}
            </span>
            <span className="text-gray-400">·</span>
            <span className="text-gray-500 text-xs">
              {formatDate(tweet.tweet.created_at)}
            </span>
          </div>

          {/* Summary only, no screenshot, no translation */}
          <p className="text-sm text-gray-700 mb-3 line-clamp-2 leading-relaxed">
            {tweet.summary || tweet.tweet.text}
          </p>

          {/* Topics (compact) */}
          {tweet.topics && tweet.topics.length > 0 && (
            <div className="mb-2 flex flex-wrap gap-1">
              {tweet.topics.slice(0, 3).map((topic, index) => (
                <span
                  key={index}
                  className="px-2 py-0.5 bg-purple-50 text-purple-600 text-xs rounded"
                >
                  {topic}
                </span>
              ))}
            </div>
          )}

          {/* Engagement metrics */}
          <div className="flex items-center gap-4 text-xs text-gray-500">
            <span className="flex items-center gap-1">
              <span>👍</span>
              <span>{formatNumber(tweet.tweet.like_count)}</span>
            </span>
            <span className="flex items-center gap-1">
              <span>🔄</span>
              <span>{formatNumber(tweet.tweet.retweet_count)}</span>
            </span>
            <span className="flex items-center gap-1">
              <span>💬</span>
              <span>{formatNumber(tweet.tweet.reply_count)}</span>
            </span>
            {tweet.tweet.bookmark_count > 0 && (
              <span className="flex items-center gap-1">
                <span>🔖</span>
                <span>{formatNumber(tweet.tweet.bookmark_count)}</span>
              </span>
            )}
          </div>
        </div>

        {/* Link to original */}
        <a
          href={tweet.tweet.tweet_url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-blue-600 text-sm whitespace-nowrap hover:text-blue-700 flex items-center gap-1 flex-shrink-0 transition-colors"
        >
          查看原推
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"
            />
          </svg>
        </a>
      </div>
    </div>
  );
}
