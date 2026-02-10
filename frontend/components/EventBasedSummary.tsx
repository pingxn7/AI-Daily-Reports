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
    <div className="space-y-8">
      {/* Statistics Dashboard */}
      <FadeIn>
        <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <span className="text-4xl">📊</span>
              <div className="text-right">
                <div className="text-3xl font-bold">
                  <CountUp end={tweetCount} duration={2000} />
                </div>
                <div className="text-blue-100 text-sm">监控推文</div>
              </div>
            </div>
            <div className="mt-4 h-1 bg-blue-400 rounded-full overflow-hidden">
              <div className="h-1 bg-white rounded-full animate-slide-in" style={{ width: '75%' }}></div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <span className="text-4xl">⭐</span>
              <div className="text-right">
                <div className="text-3xl font-bold">
                  <CountUp end={topTweetsCount} duration={2000} />
                </div>
                <div className="text-purple-100 text-sm">精选事件</div>
              </div>
            </div>
            <div className="mt-4 h-1 bg-purple-400 rounded-full overflow-hidden">
              <div className="h-1 bg-white rounded-full animate-slide-in" style={{ width: '67%', animationDelay: '0.2s' }}></div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-pink-500 to-pink-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-shadow">
            <div className="flex items-center justify-between mb-2">
              <span className="text-4xl">🔥</span>
              <div className="text-right">
                <div className="text-3xl font-bold">
                  <CountUp end={parsed.keyHighlights.length} duration={2000} />
                </div>
                <div className="text-pink-100 text-sm">关键信息</div>
              </div>
            </div>
            <div className="mt-4 h-1 bg-pink-400 rounded-full overflow-hidden">
              <div className="h-1 bg-white rounded-full animate-slide-in" style={{ width: '80%', animationDelay: '0.4s' }}></div>
            </div>
          </div>
        </section>
      </FadeIn>

      {/* Key Highlights Section */}
      {parsed.keyHighlights.length > 0 && (
        <FadeIn delay={200}>
          <section className="bg-white rounded-2xl p-8 border-2 border-gray-100 shadow-lg">
          <div className="flex items-center gap-3 mb-6 pb-4 border-b-2 border-orange-200">
            <div className="bg-gradient-to-br from-orange-400 to-red-500 rounded-xl p-3 shadow-md">
              <span className="text-3xl">🔥</span>
            </div>
            <h2 className="text-3xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
              今日关键信息
            </h2>
          </div>
          <div className="grid gap-4">
            {parsed.keyHighlights.map((item, index) => (
              <div
                key={index}
                className="group relative bg-gradient-to-r from-gray-50 to-blue-50 rounded-xl p-5 border-l-4 border-blue-500 hover:border-purple-500 hover:shadow-md transition-all duration-300"
              >
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0">
                    <span className={`inline-block px-4 py-2 bg-gradient-to-r ${getTagColor(item.tag)} text-white rounded-lg text-sm font-bold shadow-md group-hover:scale-110 transition-transform`}>
                      {item.tag}
                    </span>
                  </div>
                  <div className="flex-1">
                    <p className="text-gray-800 text-lg leading-relaxed font-medium">{item.text}</p>
                  </div>
                  <div className="flex-shrink-0 text-2xl opacity-0 group-hover:opacity-100 transition-opacity">
                    ✨
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>
        </FadeIn>
      )}

      {/* Events Section */}
      {parsed.events.length > 0 && (
        <FadeIn delay={400}>
          <section>
            <div className="flex items-center gap-3 mb-8">
            <div className="bg-gradient-to-br from-blue-400 to-indigo-500 rounded-xl p-3 shadow-md">
              <span className="text-3xl">📰</span>
            </div>
            <h2 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              今日精选事件
            </h2>
          </div>

          <div className="space-y-6">
            {parsed.events.map((event, eventIndex) => (
              <div
                key={eventIndex}
                className="bg-white rounded-2xl overflow-hidden border-2 border-gray-100 shadow-lg hover:shadow-2xl transition-all duration-300 hover:scale-[1.01]"
              >
                {/* Event Header with gradient background */}
                <div className="bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 p-6">
                  <div className="flex items-start gap-4">
                    <div className="flex-shrink-0 bg-white rounded-full w-12 h-12 flex items-center justify-center text-2xl font-bold text-blue-600 shadow-lg">
                      {eventIndex + 1}
                    </div>
                    <div className="flex-1">
                      <h3 className="text-2xl font-bold text-white mb-2 drop-shadow-md">
                        {event.title}
                      </h3>
                      {event.summary && (
                        <p className="text-white/90 leading-relaxed text-base">
                          {event.summary}
                        </p>
                      )}
                    </div>
                  </div>
                </div>

                {/* Tweets */}
                {event.tweets.length > 0 && (
                  <div className="p-6">
                    <div className="flex items-center gap-2 mb-5">
                      <div className="h-1 w-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full"></div>
                      <h4 className="text-lg font-bold text-gray-700">
                        关键信息 ({event.tweets.length})
                      </h4>
                    </div>
                    <div className="space-y-4">
                      {event.tweets.map((tweet, tweetIndex) => (
                        <div
                          key={tweetIndex}
                          className="group relative bg-gradient-to-br from-gray-50 to-blue-50 rounded-xl p-5 border-l-4 border-blue-400 hover:border-purple-500 hover:shadow-md transition-all duration-300"
                        >
                          {/* Tweet number badge */}
                          <div className="absolute -left-3 top-5 bg-gradient-to-br from-blue-500 to-purple-600 text-white rounded-full w-6 h-6 flex items-center justify-center text-xs font-bold shadow-md">
                            {tweetIndex + 1}
                          </div>

                          {/* Author with avatar placeholder */}
                          <div className="flex items-center gap-3 mb-3">
                            <div className="w-10 h-10 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white font-bold shadow-md">
                              {tweet.author.charAt(1).toUpperCase()}
                            </div>
                            <div className="text-blue-700 font-bold text-base">
                              {tweet.author}
                            </div>
                          </div>

                          {/* Summary */}
                          <div className="text-gray-800 leading-relaxed mb-4 text-base pl-13">
                            {tweet.summary}
                          </div>

                          {/* Metrics with visual bars */}
                          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4 pl-13">
                            <div className="bg-white rounded-lg p-3 shadow-sm">
                              <div className="flex items-center gap-2 mb-1">
                                <span className="text-lg">👍</span>
                                <span className="text-xs text-gray-500">点赞</span>
                              </div>
                              <div className="text-lg font-bold text-blue-600">
                                {formatNumber(tweet.metrics.likes)}
                              </div>
                            </div>
                            <div className="bg-white rounded-lg p-3 shadow-sm">
                              <div className="flex items-center gap-2 mb-1">
                                <span className="text-lg">🔁</span>
                                <span className="text-xs text-gray-500">转发</span>
                              </div>
                              <div className="text-lg font-bold text-green-600">
                                {formatNumber(tweet.metrics.retweets)}
                              </div>
                            </div>
                            <div className="bg-white rounded-lg p-3 shadow-sm">
                              <div className="flex items-center gap-2 mb-1">
                                <span className="text-lg">💬</span>
                                <span className="text-xs text-gray-500">回复</span>
                              </div>
                              <div className="text-lg font-bold text-purple-600">
                                {formatNumber(tweet.metrics.replies)}
                              </div>
                            </div>
                            <div className="bg-white rounded-lg p-3 shadow-sm">
                              <div className="flex items-center gap-2 mb-1">
                                <span className="text-lg">🔖</span>
                                <span className="text-xs text-gray-500">收藏</span>
                              </div>
                              <div className="text-lg font-bold text-orange-600">
                                {formatNumber(tweet.metrics.bookmarks)}
                              </div>
                            </div>
                          </div>

                          {/* Link */}
                          <div className="pl-13">
                            <a
                              href={tweet.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg text-sm font-semibold shadow-md hover:shadow-lg hover:scale-105 transition-all duration-300"
                            >
                              <span>🔗</span>
                              <span>查看原文</span>
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
                                  d="M9 5l7 7-7 7"
                                />
                              </svg>
                            </a>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
        </FadeIn>
      )}

      {/* Topics Section */}
      {topics && topics.length > 0 && (
        <FadeIn delay={600}>
          <section className="bg-white rounded-2xl p-8 border-2 border-gray-100 shadow-lg">
            <div className="flex items-center gap-3 mb-6 pb-4 border-b-2 border-purple-200">
              <div className="bg-gradient-to-br from-purple-400 to-pink-500 rounded-xl p-3 shadow-md">
                <span className="text-3xl">🏷️</span>
              </div>
              <h3 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                热门话题
              </h3>
            </div>
            <div className="flex flex-wrap gap-3">
              {topics.slice(0, 15).map((topic, index) => {
                const colors = [
                  'from-blue-500 to-cyan-500',
                  'from-purple-500 to-pink-500',
                  'from-green-500 to-emerald-500',
                  'from-orange-500 to-red-500',
                  'from-indigo-500 to-purple-500',
                ];
                const colorClass = colors[index % colors.length];

                return (
                  <span
                    key={index}
                    className={`group relative px-5 py-3 bg-gradient-to-r ${colorClass} text-white rounded-full text-sm font-bold shadow-md hover:shadow-xl hover:scale-110 transition-all duration-300 cursor-pointer`}
                  >
                    <span className="relative z-10">#{topic}</span>
                    <div className="absolute inset-0 bg-white opacity-0 group-hover:opacity-20 rounded-full transition-opacity"></div>
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
          <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-xl p-6 border border-blue-100 shadow-sm">
            <div className="flex items-center gap-2 mb-4">
              <span className="text-2xl">📌</span>
              <h2 className="text-xl font-bold text-gray-900">今日关键亮点</h2>
            </div>
            <div className="prose prose-sm max-w-none">
              <div className="text-gray-700 leading-relaxed whitespace-pre-line">
                {summary}
              </div>
            </div>
          </div>
        </FadeIn>
      )}
    </div>
  );
}
