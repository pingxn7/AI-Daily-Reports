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
      <div className="group bg-white rounded-xl shadow-md hover:shadow-lg transition-all duration-300 border border-gray-200 hover:border-blue-300 overflow-hidden">
        {/* Header Section - 账号信息 */}
        <div className="bg-gradient-to-r from-gray-50 to-blue-50 px-4 py-3 border-b border-gray-200">
          <div className="flex items-center gap-2">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-base shadow-md">
              {(tweet.tweet.account.display_name || tweet.tweet.account.username).charAt(0).toUpperCase()}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-1.5">
                <span className="font-bold text-gray-900 text-base truncate">
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
            <div className="flex flex-col items-center bg-gradient-to-br from-orange-500 to-red-600 text-white rounded-lg px-3 py-1.5 shadow-md flex-shrink-0">
              <span className="text-xs font-semibold leading-tight">重要度</span>
              <span className="text-lg font-bold leading-tight">{tweet.importance_score.toFixed(1)}</span>
            </div>
          </div>
        </div>

        {/* Content Section */}
        <div className="p-4 space-y-3">
          {/* AI Summary - 摘要 */}
          {tweet.summary && (
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg p-3 border-l-4 border-blue-500">
              <div className="flex items-center gap-1.5 mb-1.5">
                <span className="text-base">💡</span>
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
              <span className="text-base">📝</span>
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
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg p-3 border-l-4 border-purple-500">
              <div className="flex items-center gap-1.5 mb-1.5">
                <span className="text-base">🇨🇳</span>
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

          {/* Topics - 话题标签 */}
          {tweet.topics && tweet.topics.length > 0 && (
            <div className="flex flex-wrap gap-1.5">
              {tweet.topics.map((topic, index) => {
                const colors = [
                  'bg-blue-100 text-blue-700 border-blue-300',
                  'bg-purple-100 text-purple-700 border-purple-300',
                  'bg-green-100 text-green-700 border-green-300',
                  'bg-orange-100 text-orange-700 border-orange-300',
                ];
                const colorClass = colors[index % colors.length];

                return (
                  <span
                    key={index}
                    className={`px-2 py-1 ${colorClass} text-xs font-semibold rounded border`}
                  >
                    #{topic}
                  </span>
                );
              })}
            </div>
          )}

          {/* Engagement Metrics - 互动数据 */}
          <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-lg p-3 border border-gray-200">
            <div className="flex items-center gap-1.5 mb-2">
              <span className="text-base">📊</span>
              <h4 className="font-bold text-xs text-gray-700 uppercase tracking-wide">
                互动数据
              </h4>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
              <div className="bg-white rounded-md p-2 border border-red-200 hover:border-red-400 transition-colors">
                <div className="flex items-center gap-1 mb-0.5">
                  <span className="text-lg">👍</span>
                  <span className="text-xs text-gray-600 font-semibold">点赞</span>
                </div>
                <div className="text-base font-bold text-red-600">
                  {formatNumber(tweet.tweet.like_count)}
                </div>
              </div>

              <div className="bg-white rounded-md p-2 border border-green-200 hover:border-green-400 transition-colors">
                <div className="flex items-center gap-1 mb-0.5">
                  <span className="text-lg">🔄</span>
                  <span className="text-xs text-gray-600 font-semibold">转发</span>
                </div>
                <div className="text-base font-bold text-green-600">
                  {formatNumber(tweet.tweet.retweet_count)}
                </div>
              </div>

              <div className="bg-white rounded-md p-2 border border-blue-200 hover:border-blue-400 transition-colors">
                <div className="flex items-center gap-1 mb-0.5">
                  <span className="text-lg">💬</span>
                  <span className="text-xs text-gray-600 font-semibold">回复</span>
                </div>
                <div className="text-base font-bold text-blue-600">
                  {formatNumber(tweet.tweet.reply_count)}
                </div>
              </div>

              <div className="bg-white rounded-md p-2 border border-orange-200 hover:border-orange-400 transition-colors">
                <div className="flex items-center gap-1 mb-0.5">
                  <span className="text-lg">🔖</span>
                  <span className="text-xs text-gray-600 font-semibold">收藏</span>
                </div>
                <div className="text-base font-bold text-orange-600">
                  {formatNumber(tweet.tweet.bookmark_count)}
                </div>
              </div>
            </div>
          </div>

          {/* Link to original */}
          <div className="pt-1">
            <a
              href={tweet.tweet.tweet_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg font-semibold text-sm shadow-md hover:shadow-lg hover:scale-105 transition-all duration-300"
            >
              <span>🔗</span>
              <span>查看原推文</span>
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
    <div className="group bg-white rounded-xl shadow-sm p-5 hover:shadow-lg transition-all duration-300 border border-gray-200 hover:border-blue-300">
      <div className="flex items-start gap-4">
        {/* Avatar */}
        <div className="flex-shrink-0 w-10 h-10 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold shadow-md group-hover:scale-110 transition-transform">
          {(tweet.tweet.account.display_name || tweet.tweet.account.username).charAt(0).toUpperCase()}
        </div>

        <div className="flex-1 min-w-0">
          {/* Author info */}
          <div className="flex items-center gap-2 text-sm mb-2">
            <span className="font-bold text-gray-900 truncate">
              {tweet.tweet.account.display_name || tweet.tweet.account.username}
            </span>
            <span className="text-gray-500 truncate text-xs">
              @{tweet.tweet.account.username}
            </span>
            <span className="text-gray-400">·</span>
            <span className="text-gray-500 text-xs">
              {formatDate(tweet.tweet.created_at)}
            </span>
          </div>

          {/* Summary */}
          <p className="text-sm text-gray-700 mb-3 line-clamp-2 leading-relaxed">
            {tweet.summary || tweet.tweet.text}
          </p>

          {/* Topics (compact) */}
          {tweet.topics && tweet.topics.length > 0 && (
            <div className="mb-3 flex flex-wrap gap-1.5">
              {tweet.topics.slice(0, 3).map((topic, index) => {
                const colors = [
                  'bg-blue-100 text-blue-700',
                  'bg-purple-100 text-purple-700',
                  'bg-green-100 text-green-700',
                ];
                const colorClass = colors[index % colors.length];

                return (
                  <span
                    key={index}
                    className={`px-2.5 py-1 ${colorClass} text-xs font-semibold rounded-full`}
                  >
                    #{topic}
                  </span>
                );
              })}
            </div>
          )}

          {/* Engagement metrics with mini cards */}
          <div className="flex items-center gap-3 mb-3">
            <div className="flex items-center gap-1.5 bg-red-50 px-2.5 py-1 rounded-lg">
              <span className="text-sm">👍</span>
              <span className="text-xs font-semibold text-red-600">
                {formatNumber(tweet.tweet.like_count)}
              </span>
            </div>
            <div className="flex items-center gap-1.5 bg-green-50 px-2.5 py-1 rounded-lg">
              <span className="text-sm">🔄</span>
              <span className="text-xs font-semibold text-green-600">
                {formatNumber(tweet.tweet.retweet_count)}
              </span>
            </div>
            <div className="flex items-center gap-1.5 bg-blue-50 px-2.5 py-1 rounded-lg">
              <span className="text-sm">💬</span>
              <span className="text-xs font-semibold text-blue-600">
                {formatNumber(tweet.tweet.reply_count)}
              </span>
            </div>
            {tweet.tweet.bookmark_count > 0 && (
              <div className="flex items-center gap-1.5 bg-orange-50 px-2.5 py-1 rounded-lg">
                <span className="text-sm">🔖</span>
                <span className="text-xs font-semibold text-orange-600">
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
            className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg text-xs font-semibold shadow-sm hover:shadow-md hover:scale-105 transition-all duration-300"
          >
            <span>🔗</span>
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
