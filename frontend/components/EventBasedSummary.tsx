import React from 'react';
import { CountUp } from './CountUp';
import { FadeIn } from './FadeIn';

interface KeyHighlight {
  tag: string;
  text: string;
}

interface TweetInfo {
  author: string;
  summary: string;
  metrics: {
    likes: number;
    retweets: number;
    replies: number;
    bookmarks: number;
  };
  url: string;
}

interface Event {
  title: string;
  summary: string;
  tweets: TweetInfo[];
}

interface ParsedReport {
  keyHighlights: KeyHighlight[];
  events: Event[];
}

interface EventBasedSummaryProps {
  summary: string;
  tweetCount: number;
  topTweetsCount: number;
  topics: string[] | null;
}

function parseEventBasedReport(markdownText: string): ParsedReport {
  const result: ParsedReport = {
    keyHighlights: [],
    events: [],
  };

  // Parse key highlights
  const highlightsMatch = markdownText.match(/##\s*🔥\s*今日关键信息([\s\S]*?)(?=##|$)/);
  if (highlightsMatch) {
    const highlightsText = highlightsMatch[1];
    const lines = highlightsText.split('\n');
    for (const line of lines) {
      const match = line.match(/^-\s*【(.+?)】\s*(.+)$/);
      if (match) {
        result.keyHighlights.push({
          tag: match[1],
          text: match[2],
        });
      }
    }
  }

  // Parse events section
  const eventsMatch = markdownText.match(/##\s*📰\s*今日精选事件([\s\S]*)$/);
  if (!eventsMatch) {
    return result;
  }

  const eventsText = eventsMatch[1];
  const blocks = eventsText.split(/###\s+/);

  let i = 0;
  while (i < blocks.length) {
    const block = blocks[i].trim();
    if (!block) {
      i++;
      continue;
    }

    // Check if this is a title/summary block
    if (!block.startsWith('关键信息')) {
      const lines = block.split('\n');
      const title = lines[0].trim();
      let summary = lines.slice(1).join('\n').trim();

      // Remove any "####" markers from summary
      summary = summary.replace(/####[\s\S]*$/, '').trim();

      const tweets: TweetInfo[] = [];

      // Look for the next block which should be "关键信息"
      if (i + 1 < blocks.length) {
        const nextBlock = blocks[i + 1].trim();
        if (nextBlock.startsWith('关键信息')) {
          // Parse tweets from this block
          const tweetPattern = /-\s*\*\*(@\w+)\s*\(([^)]+)\)\*\*\s*-\s*([^\n]+)\n\s*👍\s*([\d,]+)\s*\|\s*🔁\s*([\d,]+)\s*\|\s*💬\s*([\d,]+)\s*\|\s*🔖\s*([\d,]+)\s*\n\s*\[查看原文\]\(([^)]+)\)/g;

          let tweetMatch;
          while ((tweetMatch = tweetPattern.exec(nextBlock)) !== null) {
            tweets.push({
              author: `${tweetMatch[1]} (${tweetMatch[2]})`,
              summary: tweetMatch[3].trim(),
              metrics: {
                likes: parseInt(tweetMatch[4].replace(/,/g, '')),
                retweets: parseInt(tweetMatch[5].replace(/,/g, '')),
                replies: parseInt(tweetMatch[6].replace(/,/g, '')),
                bookmarks: parseInt(tweetMatch[7].replace(/,/g, '')),
              },
              url: tweetMatch[8],
            });
          }

          i++; // Skip the next block since we processed it
        }
      }

      result.events.push({
        title,
        summary,
        tweets,
      });
    }

    i++;
  }

  return result;
}

function formatNumber(num: number): string {
  return num.toLocaleString();
}

export function EventBasedSummary({
  summary,
  tweetCount,
  topTweetsCount,
  topics,
}: EventBasedSummaryProps) {
  const parsed = parseEventBasedReport(summary);

  // Tag color mapping
  const getTagColor = (tag: string) => {
    const colorMap: { [key: string]: string } = {
      '模型': 'from-purple-500 to-pink-500',
      '产品': 'from-blue-500 to-cyan-500',
      '市场': 'from-green-500 to-emerald-500',
      '应用': 'from-orange-500 to-amber-500',
      '融资': 'from-red-500 to-rose-500',
      '研究': 'from-indigo-500 to-violet-500',
    };
    return colorMap[tag] || 'from-gray-500 to-slate-500';
  };

  return (
    <div className="space-y-6">
      {/* Statistics Dashboard - Compact */}
      <FadeIn>
        <section className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-4 text-white shadow-md hover:shadow-lg transition-all duration-200">
            <div className="flex items-center justify-between">
              <span className="text-3xl">📊</span>
              <div className="text-right">
                <div className="text-2xl font-bold">
                  <CountUp end={tweetCount} duration={2000} />
                </div>
                <div className="text-blue-100 text-xs font-medium">监控推文</div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-4 text-white shadow-md hover:shadow-lg transition-all duration-200">
            <div className="flex items-center justify-between">
              <span className="text-3xl">⭐</span>
              <div className="text-right">
                <div className="text-2xl font-bold">
                  <CountUp end={topTweetsCount} duration={2000} />
                </div>
                <div className="text-purple-100 text-xs font-medium">精选事件</div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl p-4 text-white shadow-md hover:shadow-lg transition-all duration-200">
            <div className="flex items-center justify-between">
              <span className="text-3xl">🔥</span>
              <div className="text-right">
                <div className="text-2xl font-bold">
                  <CountUp end={parsed.keyHighlights.length} duration={2000} />
                </div>
                <div className="text-pink-100 text-xs font-medium">关键信息</div>
              </div>
            </div>
          </div>
        </section>
      </FadeIn>

      {/* Key Highlights Section */}
      {parsed.keyHighlights.length > 0 && (
        <FadeIn delay={200}>
          <section>
            <div className="flex items-center gap-3 mb-6">
              <div className="bg-gradient-to-br from-orange-400 to-red-500 rounded-xl p-3 shadow-md">
                <span className="text-3xl">🔥</span>
              </div>
              <h2 className="text-3xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
                今日关键信息
              </h2>
            </div>
            <div className="grid gap-3">
              {parsed.keyHighlights.map((item, index) => {
                // Alternate background colors
                const bgColors = [
                  'from-blue-50 to-cyan-50',
                  'from-purple-50 to-pink-50',
                  'from-green-50 to-emerald-50',
                  'from-orange-50 to-amber-50',
                  'from-rose-50 to-red-50',
                  'from-indigo-50 to-violet-50',
                ];
                const bgColor = bgColors[index % bgColors.length];

                return (
                  <div
                    key={index}
                    className={`group bg-gradient-to-r ${bgColor} rounded-xl p-4 border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200`}
                  >
                    <div className="flex items-start gap-3">
                      <div className="flex-shrink-0">
                        <span className={`inline-block px-3 py-1.5 bg-gradient-to-r ${getTagColor(item.tag)} text-white rounded-full text-xs font-bold shadow-sm`}>
                          {item.tag}
                        </span>
                      </div>
                      <div className="flex-1">
                        <p className="text-gray-800 text-sm leading-relaxed font-medium">{item.text}</p>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </section>
        </FadeIn>
      )}

      {/* Events Section */}
      {parsed.events.length > 0 && (
        <FadeIn delay={400}>
          <section>
            <div className="flex items-center gap-3 mb-6">
              <div className="bg-gradient-to-br from-blue-400 to-indigo-500 rounded-xl p-3 shadow-md">
                <span className="text-3xl">📰</span>
              </div>
              <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                今日精选事件
              </h2>
            </div>

            <div className="space-y-5">
              {parsed.events.map((event, eventIndex) => {
                // Alternate background colors for each event
                const bgColors = [
                  'from-blue-50 to-cyan-50',
                  'from-purple-50 to-pink-50',
                  'from-green-50 to-emerald-50',
                  'from-orange-50 to-amber-50',
                  'from-indigo-50 to-violet-50',
                ];
                const bgColor = bgColors[eventIndex % bgColors.length];

                const headerColors = [
                  'from-blue-500 to-cyan-600',
                  'from-purple-500 to-pink-600',
                  'from-green-500 to-emerald-600',
                  'from-orange-500 to-amber-600',
                  'from-indigo-500 to-violet-600',
                ];
                const headerColor = headerColors[eventIndex % headerColors.length];

                return (
                  <div
                    key={eventIndex}
                    className={`bg-gradient-to-br ${bgColor} rounded-2xl overflow-hidden border border-gray-200 shadow-md hover:shadow-xl transition-all duration-300`}
                  >
                    {/* Event Header - Compact */}
                    <div className={`bg-gradient-to-r ${headerColor} px-5 py-4`}>
                      <div className="flex items-center gap-3">
                        <div className="flex-shrink-0 bg-white rounded-full w-10 h-10 flex items-center justify-center text-lg font-bold text-gray-800 shadow-md">
                          {eventIndex + 1}
                        </div>
                        <div className="flex-1 min-w-0">
                          <h3 className="text-xl font-bold text-white mb-1 drop-shadow-sm">
                            {event.title}
                          </h3>
                          {event.summary && (
                            <p className="text-white/90 text-sm leading-snug line-clamp-2">
                              {event.summary}
                            </p>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Tweets - Modular Cards */}
                    {event.tweets.length > 0 && (
                      <div className="p-4 space-y-3">
                        {event.tweets.map((tweet, tweetIndex) => (
                          <div
                            key={tweetIndex}
                            className="bg-white rounded-xl p-4 border border-gray-200 shadow-sm hover:shadow-md transition-all duration-200"
                          >
                            {/* Author Section */}
                            <div className="flex items-center gap-2 mb-3">
                              <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold text-sm shadow-sm">
                                {tweet.author.charAt(1).toUpperCase()}
                              </div>
                              <div className="flex-1 min-w-0">
                                <div className="text-gray-900 font-semibold text-sm truncate">
                                  {tweet.author}
                                </div>
                              </div>
                              <div className="flex-shrink-0 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold shadow-sm">
                                {tweetIndex + 1}
                              </div>
                            </div>

                            {/* Summary */}
                            <div className="text-gray-700 text-sm leading-relaxed mb-3">
                              {tweet.summary}
                            </div>

                            {/* Metrics - Colorful Pill Blocks */}
                            <div className="flex flex-wrap gap-2 mb-3">
                              <div className="flex items-center gap-1.5 bg-gradient-to-r from-red-50 to-pink-50 border border-red-200 rounded-full px-3 py-1.5 shadow-sm">
                                <span className="text-base">👍</span>
                                <span className="text-xs font-bold text-red-600">
                                  {formatNumber(tweet.metrics.likes)}
                                </span>
                              </div>
                              <div className="flex items-center gap-1.5 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-full px-3 py-1.5 shadow-sm">
                                <span className="text-base">🔁</span>
                                <span className="text-xs font-bold text-green-600">
                                  {formatNumber(tweet.metrics.retweets)}
                                </span>
                              </div>
                              <div className="flex items-center gap-1.5 bg-gradient-to-r from-blue-50 to-cyan-50 border border-blue-200 rounded-full px-3 py-1.5 shadow-sm">
                                <span className="text-base">💬</span>
                                <span className="text-xs font-bold text-blue-600">
                                  {formatNumber(tweet.metrics.replies)}
                                </span>
                              </div>
                              <div className="flex items-center gap-1.5 bg-gradient-to-r from-orange-50 to-amber-50 border border-orange-200 rounded-full px-3 py-1.5 shadow-sm">
                                <span className="text-base">🔖</span>
                                <span className="text-xs font-bold text-orange-600">
                                  {formatNumber(tweet.metrics.bookmarks)}
                                </span>
                              </div>
                            </div>

                            {/* Link */}
                            <a
                              href={tweet.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg text-xs font-semibold shadow-sm hover:shadow-md hover:scale-105 transition-all duration-200"
                            >
                              <span className="text-sm">🔗</span>
                              <span>查看原文</span>
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
                                  d="M9 5l7 7-7 7"
                                />
                              </svg>
                            </a>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </section>
        </FadeIn>
      )}

      {/* Topics Section */}
      {topics && topics.length > 0 && (
        <FadeIn delay={600}>
          <section className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6 border border-purple-200 shadow-md">
            <div className="flex items-center gap-3 mb-4">
              <div className="bg-gradient-to-br from-purple-400 to-pink-500 rounded-xl p-2.5 shadow-sm">
                <span className="text-2xl">🏷️</span>
              </div>
              <h3 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                热门话题
              </h3>
            </div>
            <div className="flex flex-wrap gap-2">
              {topics.slice(0, 15).map((topic, index) => {
                const colors = [
                  'from-blue-500 to-cyan-500',
                  'from-purple-500 to-pink-500',
                  'from-green-500 to-emerald-500',
                  'from-orange-500 to-red-500',
                  'from-indigo-500 to-violet-500',
                  'from-rose-500 to-pink-500',
                ];
                const colorClass = colors[index % colors.length];

                return (
                  <span
                    key={index}
                    className={`inline-flex items-center px-3 py-1.5 bg-gradient-to-r ${colorClass} text-white rounded-full text-xs font-bold shadow-sm hover:shadow-md hover:scale-105 transition-all duration-200 cursor-pointer`}
                  >
                    #{topic}
                  </span>
                );
              })}
            </div>
          </section>
        </FadeIn>
      )}

      {/* Fallback for plain text if parsing fails */}
      {parsed.keyHighlights.length === 0 && parsed.events.length === 0 && (
        <FadeIn>
          <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-5 border border-blue-200 shadow-sm">
            <div className="flex items-center gap-2 mb-3">
              <span className="text-xl">📌</span>
              <h2 className="text-lg font-bold text-gray-900">今日关键亮点</h2>
            </div>
            <div className="prose prose-sm max-w-none">
              <div className="text-gray-700 text-sm leading-relaxed whitespace-pre-line">
                {summary}
              </div>
            </div>
          </div>
        </FadeIn>
      )}
    </div>
  );
}
