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
      <div className="group bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-200 border border-gray-200 hover:border-blue-300 overflow-hidden">
        {/* Header Section - 账号信息 */}
        <div className="bg-gradient-to-r from-blue-50 to-purple-50 px-4 py-3 border-b border-gray-200">
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-sm shadow-sm">
              {(tweet.tweet.account.display_name || tweet.tweet.account.username).charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-gray-900 text-sm truncate">
                  {tweet.tweet.account.display_name || tweet.tweet.account.username}
                </span>
                <span className="px-1.5 py-0.5 bg-blue-500 text-white text-xs font-semibold rounded flex-shrink-0">
                  ✓
                </span>
              </div>
              <div className="flex items-center gap-1.5 text-xs text-gray-600">
                <span className="truncate">@{tweet.tweet.account.username}</span>
                <span>•</span>
                <span className="flex-shrink-0">{formatDate(tweet.tweet.created_at)}</span>
              </div>
            </div>
            {/* Importance badge */}
            <div className="flex flex-col items-center bg-gradient-to-br from-orange-500 to-red-600 text-white rounded-lg px-2.5 py-1 shadow-sm flex-shrink-0">
              <span className="text-xs font-semibold leading-tight">重要度</span>
              <span className="text-base font-bold leading-tight">{tweet.importance_score.toFixed(1)}</span>
            </div>
          </div>
        </div>

        {/* Content Section */}
        <div className="p-4 space-y-3">
          {/* AI Summary - 摘要 */}
          {tweet.summary && (
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-3 border border-blue-200">
              <div className="flex items-center gap-1.5 mb-1.5">
                <span className="text-sm">💡</span>
                <h4 className="font-bold text-xs text-blue-900 uppercase tracking-wide">
                  核心摘要
                </h4>
              </div>
              <p className="text-sm text-gray-800 leading-relaxed">
                {tweet.summary}
              </p>
            </div>
          )}

          {/* Original tweet text - 原文 */}
          <div className="bg-gray-50 rounded-lg p-3 border border-gray-200">
            <div className="flex items-center gap-1.5 mb-1.5">
              <span className="text-sm">📝</span>
              <h4 className="font-bold text-xs text-gray-700 uppercase tracking-wide">
                原文内容
              </h4>
            </div>
            <p className="text-sm text-gray-700 leading-relaxed">
              {tweet.tweet.text}
            </p>
          </div>

          {/* Translation - 翻译 */}
          {tweet.translation && (
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg p-3 border border-purple-200">
              <div className="flex items-center gap-1.5 mb-1.5">
                <span className="text-sm">🇨🇳</span>
                <h4 className="font-bold text-xs text-purple-900 uppercase tracking-wide">
                  中文翻译
                </h4>
              </div>
              <p className="text-sm text-gray-800 leading-relaxed">
                {tweet.translation}
              </p>
            </div>
          )}

          {/* Screenshot */}
          {tweet.screenshot_url && (
            <div className="rounded-lg overflow-hidden border border-gray-200 shadow-sm">
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

          {/* Topics - 话题标签 (Colorful Pills) */}
          {tweet.topics && tweet.topics.length > 0 && (
            <div className="flex flex-wrap gap-1.5">
              {tweet.topics.map((topic, index) => {
                const colors = [
                  'from-blue-500 to-cyan-500',
                  'from-purple-500 to-pink-500',
                  'from-green-500 to-emerald-500',
                  'from-orange-500 to-amber-500',
                  'from-rose-500 to-red-500',
                  'from-indigo-500 to-violet-500',
                ];
                const colorClass = colors[index % colors.length];

                return (
                  <span
                    key={index}
                    className={`inline-flex items-center px-2.5 py-1 bg-gradient-to-r ${colorClass} text-white text-xs font-bold rounded-full shadow-sm`}
                  >
                    #{topic}
                  </span>
                );
              })}
            </div>
          )}

          {/* Engagement Metrics - Colorful Pill Style */}
          <div className="flex flex-wrap gap-2">
            <div className="flex items-center gap-1.5 bg-gradient-to-r from-red-50 to-pink-50 border border-red-200 rounded-full px-3 py-1.5 shadow-sm">
              <span className="text-base">👍</span>
              <span className="text-xs font-bold text-red-600">
                {formatNumber(tweet.tweet.like_count)}
              </span>
            </div>

            <div className="flex items-center gap-1.5 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-full px-3 py-1.5 shadow-sm">
              <span className="text-base">🔄</span>
              <span className="text-xs font-bold text-green-600">
                {formatNumber(tweet.tweet.retweet_count)}
              </span>
            </div>

            <div className="flex items-center gap-1.5 bg-gradient-to-r from-blue-50 to-cyan-50 border border-blue-200 rounded-full px-3 py-1.5 shadow-sm">
              <span className="text-base">💬</span>
              <span className="text-xs font-bold text-blue-600">
                {formatNumber(tweet.tweet.reply_count)}
              </span>
            </div>

            <div className="flex items-center gap-1.5 bg-gradient-to-r from-orange-50 to-amber-50 border border-orange-200 rounded-full px-3 py-1.5 shadow-sm">
              <span className="text-base">🔖</span>
              <span className="text-xs font-bold text-orange-600">
                {formatNumber(tweet.tweet.bookmark_count)}
              </span>
            </div>
          </div>

          {/* Link to original */}
          <div>
            <a
              href={tweet.tweet.tweet_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-1.5 px-3 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg font-semibold text-xs shadow-sm hover:shadow-md hover:scale-105 transition-all duration-200"
            >
              <span className="text-sm">🔗</span>
              <span>查看原推文</span>
              <svg
                className="w-3 h-3"
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
    <div className="group bg-white rounded-xl shadow-sm p-4 hover:shadow-md transition-all duration-200 border border-gray-200 hover:border-blue-300">
      <div className="flex items-start gap-3">
        {/* Avatar */}
        <div className="flex-shrink-0 w-9 h-9 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-sm shadow-sm group-hover:scale-105 transition-transform">
          {(tweet.tweet.account.display_name || tweet.tweet.account.username).charAt(0).toUpperCase()}
        </div>

        <div className="flex-1 min-w-0">
          {/* Author info */}
          <div className="flex items-center gap-1.5 text-xs mb-2">
            <span className="font-bold text-gray-900 truncate text-sm">
              {tweet.tweet.account.display_name || tweet.tweet.account.username}
            </span>
            <span className="text-gray-500 truncate">
              @{tweet.tweet.account.username}
            </span>
            <span className="text-gray-400">·</span>
            <span className="text-gray-500 flex-shrink-0">
              {formatDate(tweet.tweet.created_at)}
            </span>
          </div>

          {/* Summary */}
          <p className="text-sm text-gray-700 mb-2 line-clamp-2 leading-relaxed">
            {tweet.summary || tweet.tweet.text}
          </p>

          {/* Topics (compact) - Colorful Pills */}
          {tweet.topics && tweet.topics.length > 0 && (
            <div className="mb-2 flex flex-wrap gap-1.5">
              {tweet.topics.slice(0, 3).map((topic, index) => {
                const colors = [
                  'from-blue-500 to-cyan-500',
                  'from-purple-500 to-pink-500',
                  'from-green-500 to-emerald-500',
                  'from-orange-500 to-amber-500',
                ];
                const colorClass = colors[index % colors.length];

                return (
                  <span
                    key={index}
                    className={`inline-flex items-center px-2 py-0.5 bg-gradient-to-r ${colorClass} text-white text-xs font-bold rounded-full shadow-sm`}
                  >
                    #{topic}
                  </span>
                );
              })}
            </div>
          )}

          {/* Engagement metrics - Colorful Pills */}
          <div className="flex flex-wrap items-center gap-1.5 mb-2">
            <div className="flex items-center gap-1 bg-gradient-to-r from-red-50 to-pink-50 border border-red-200 px-2 py-1 rounded-full">
              <span className="text-sm">👍</span>
              <span className="text-xs font-bold text-red-600">
                {formatNumber(tweet.tweet.like_count)}
              </span>
            </div>
            <div className="flex items-center gap-1 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 px-2 py-1 rounded-full">
              <span className="text-sm">🔄</span>
              <span className="text-xs font-bold text-green-600">
                {formatNumber(tweet.tweet.retweet_count)}
              </span>
            </div>
            <div className="flex items-center gap-1 bg-gradient-to-r from-blue-50 to-cyan-50 border border-blue-200 px-2 py-1 rounded-full">
              <span className="text-sm">💬</span>
              <span className="text-xs font-bold text-blue-600">
                {formatNumber(tweet.tweet.reply_count)}
              </span>
            </div>
            {tweet.tweet.bookmark_count > 0 && (
              <div className="flex items-center gap-1 bg-gradient-to-r from-orange-50 to-amber-50 border border-orange-200 px-2 py-1 rounded-full">
                <span className="text-sm">🔖</span>
                <span className="text-xs font-bold text-orange-600">
                  {formatNumber(tweet.tweet.bookmark_count)}
                </span>
              </div>
            )}
          </div>

          {/* Link to original */}
          <a
            href={tweet.tweet.tweet_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg text-xs font-semibold shadow-sm hover:shadow-md hover:scale-105 transition-all duration-200"
          >
            <span className="text-sm">🔗</span>
            <span>查看原推</span>
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 5l7 7-7 7"
              />
            </svg>
          </a>
        </div>
      </div>
    </div>
  );
}
