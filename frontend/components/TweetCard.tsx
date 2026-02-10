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
      <div className="group bg-white rounded-2xl shadow-lg p-6 hover:shadow-2xl transition-all duration-300 border-2 border-gray-100 hover:border-blue-200">
        <div className="flex items-start gap-4">
          <div className="flex-1">
            {/* Author info with avatar */}
            <div className="flex items-center gap-3 mb-4 pb-3 border-b border-gray-100">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-lg shadow-md">
                {(tweet.tweet.account.display_name || tweet.tweet.account.username).charAt(0).toUpperCase()}
              </div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-gray-900 text-lg">
                    {tweet.tweet.account.display_name || tweet.tweet.account.username}
                  </span>
                  <span className="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs font-semibold rounded">
                    认证
                  </span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <span>@{tweet.tweet.account.username}</span>
                  <span>·</span>
                  <span>{formatDate(tweet.tweet.created_at)}</span>
                </div>
              </div>
              {/* Importance badge */}
              <div className="flex flex-col items-center bg-gradient-to-br from-orange-400 to-red-500 text-white rounded-xl px-3 py-2 shadow-md">
                <span className="text-xs font-semibold">重要度</span>
                <span className="text-lg font-bold">{tweet.importance_score.toFixed(1)}</span>
              </div>
            </div>

            {/* Original tweet text */}
            <div className="mb-4 p-4 bg-gradient-to-br from-gray-50 to-blue-50 rounded-xl">
              <p className="text-gray-800 leading-relaxed text-base">
                {tweet.tweet.text}
              </p>
            </div>

            {/* Screenshot */}
            {tweet.screenshot_url && (
              <div className="mb-4 rounded-xl overflow-hidden border-2 border-gray-200 shadow-md hover:shadow-lg transition-shadow">
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
              <div className="mb-4 p-5 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border-l-4 border-blue-500 shadow-sm">
                <div className="flex items-center gap-2 mb-2">
                  <div className="bg-blue-500 rounded-lg p-1.5">
                    <span className="text-lg">🤖</span>
                  </div>
                  <h4 className="font-bold text-base text-blue-900">
                    AI 智能摘要
                  </h4>
                </div>
                <p className="text-base text-blue-800 leading-relaxed">
                  {tweet.summary}
                </p>
              </div>
            )}

            {/* Translation */}
            {tweet.translation && (
              <div className="mb-4 p-5 bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl border-l-4 border-purple-500 shadow-sm">
                <div className="flex items-center gap-2 mb-2">
                  <div className="bg-purple-500 rounded-lg p-1.5">
                    <span className="text-lg">🇨🇳</span>
                  </div>
                  <h4 className="font-bold text-base text-purple-900">
                    中文翻译
                  </h4>
                </div>
                <p className="text-base text-purple-800 leading-relaxed">
                  {tweet.translation}
                </p>
              </div>
            )}

            {/* Topics */}
            {tweet.topics && tweet.topics.length > 0 && (
              <div className="mb-4 flex flex-wrap gap-2">
                {tweet.topics.map((topic, index) => {
                  const colors = [
                    'from-blue-500 to-cyan-500',
                    'from-purple-500 to-pink-500',
                    'from-green-500 to-emerald-500',
                    'from-orange-500 to-red-500',
                  ];
                  const colorClass = colors[index % colors.length];

                  return (
                    <span
                      key={index}
                      className={`px-4 py-2 bg-gradient-to-r ${colorClass} text-white text-sm font-bold rounded-full shadow-md hover:shadow-lg hover:scale-105 transition-all`}
                    >
                      #{topic}
                    </span>
                  );
                })}
              </div>
            )}

            {/* Engagement metrics with visual cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
              <div className="bg-gradient-to-br from-red-50 to-pink-50 rounded-xl p-4 border border-red-100 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-2xl">👍</span>
                  <span className="text-xs text-gray-600 font-semibold">点赞</span>
                </div>
                <div className="text-xl font-bold text-red-600">
                  {formatNumber(tweet.tweet.like_count)}
                </div>
              </div>

              <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-4 border border-green-100 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-2xl">🔄</span>
                  <span className="text-xs text-gray-600 font-semibold">转发</span>
                </div>
                <div className="text-xl font-bold text-green-600">
                  {formatNumber(tweet.tweet.retweet_count)}
                </div>
              </div>

              <div className="bg-gradient-to-br from-blue-50 to-cyan-50 rounded-xl p-4 border border-blue-100 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-2xl">💬</span>
                  <span className="text-xs text-gray-600 font-semibold">回复</span>
                </div>
                <div className="text-xl font-bold text-blue-600">
                  {formatNumber(tweet.tweet.reply_count)}
                </div>
              </div>

              <div className="bg-gradient-to-br from-orange-50 to-amber-50 rounded-xl p-4 border border-orange-100 shadow-sm hover:shadow-md transition-shadow">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-2xl">🔖</span>
                  <span className="text-xs text-gray-600 font-semibold">收藏</span>
                </div>
                <div className="text-xl font-bold text-orange-600">
                  {formatNumber(tweet.tweet.bookmark_count)}
                </div>
              </div>
            </div>

            {/* Link to original */}
            <a
              href={tweet.tweet.tweet_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold shadow-md hover:shadow-lg hover:scale-105 transition-all duration-300"
            >
              <span>🔗</span>
              <span>查看原推文</span>
              <svg
                className="w-5 h-5"
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
