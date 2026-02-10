import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface HighlightsSummaryProps {
  summary: string;
  tweetCount: number;
  topTweetsCount: number;
  topics: string[] | null;
}

export function HighlightsSummary({
  summary,
  tweetCount,
  topTweetsCount,
  topics,
}: HighlightsSummaryProps) {
  return (
    <div className="space-y-6 mb-8">
      {/* Statistics Dashboard */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-shadow">
          <div className="flex items-center justify-between mb-2">
            <span className="text-4xl">📊</span>
            <div className="text-right">
              <div className="text-3xl font-bold">{tweetCount}</div>
              <div className="text-blue-100 text-sm">监控推文</div>
            </div>
          </div>
          <div className="mt-4 h-1 bg-blue-400 rounded-full">
            <div className="h-1 bg-white rounded-full w-3/4"></div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-shadow">
          <div className="flex items-center justify-between mb-2">
            <span className="text-4xl">⭐</span>
            <div className="text-right">
              <div className="text-3xl font-bold">{topTweetsCount}</div>
              <div className="text-purple-100 text-sm">精选内容</div>
            </div>
          </div>
          <div className="mt-4 h-1 bg-purple-400 rounded-full">
            <div className="h-1 bg-white rounded-full w-2/3"></div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-pink-500 to-pink-600 rounded-2xl p-6 text-white shadow-lg hover:shadow-xl transition-shadow">
          <div className="flex items-center justify-between mb-2">
            <span className="text-4xl">🏷️</span>
            <div className="text-right">
              <div className="text-3xl font-bold">{topics?.length || 0}</div>
              <div className="text-pink-100 text-sm">热门话题</div>
            </div>
          </div>
          <div className="mt-4 h-1 bg-pink-400 rounded-full">
            <div className="h-1 bg-white rounded-full w-4/5"></div>
          </div>
        </div>
      </div>

      {/* AI-generated summary with Markdown rendering */}
      <div className="bg-white rounded-2xl p-8 border-2 border-gray-100 shadow-lg">
        <div className="flex items-center gap-3 mb-6 pb-4 border-b-2 border-blue-200">
          <div className="bg-gradient-to-br from-blue-400 to-indigo-500 rounded-xl p-3 shadow-md">
            <span className="text-3xl">📌</span>
          </div>
          <h2 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            今日关键亮点
          </h2>
        </div>

        <div className="prose prose-lg max-w-none markdown-content">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              h1: ({ node, ...props }) => (
                <h1 className="text-3xl font-bold text-gray-900 mt-8 mb-4 flex items-center gap-2" {...props} />
              ),
              h2: ({ node, ...props }) => (
                <h2 className="text-2xl font-bold text-gray-800 mt-6 mb-3 flex items-center gap-2" {...props} />
              ),
              h3: ({ node, ...props }) => (
                <h3 className="text-xl font-bold text-gray-800 mt-5 mb-2" {...props} />
              ),
              h4: ({ node, ...props }) => (
                <h4 className="text-lg font-semibold text-gray-700 mt-4 mb-2" {...props} />
              ),
              p: ({ node, ...props }) => (
                <p className="text-gray-700 leading-relaxed mb-4" {...props} />
              ),
              ul: ({ node, ...props }) => (
                <ul className="space-y-2 mb-4 ml-4" {...props} />
              ),
              ol: ({ node, ...props }) => (
                <ol className="space-y-2 mb-4 ml-4" {...props} />
              ),
              li: ({ node, ...props }) => (
                <li className="text-gray-700 leading-relaxed" {...props} />
              ),
              hr: ({ node, ...props }) => (
                <hr className="my-6 border-t-2 border-gray-200" {...props} />
              ),
              blockquote: ({ node, ...props }) => (
                <blockquote className="border-l-4 border-blue-500 pl-4 py-2 my-4 bg-blue-50 rounded-r-lg" {...props} />
              ),
              a: ({ node, ...props }) => (
                <a className="text-blue-600 hover:text-blue-700 underline" target="_blank" rel="noopener noreferrer" {...props} />
              ),
              strong: ({ node, ...props }) => (
                <strong className="font-bold text-gray-900" {...props} />
              ),
              em: ({ node, ...props }) => (
                <em className="italic text-gray-800" {...props} />
              ),
              code: ({ node, inline, ...props }: any) =>
                inline ? (
                  <code className="bg-gray-100 text-red-600 px-1.5 py-0.5 rounded text-sm font-mono" {...props} />
                ) : (
                  <code className="block bg-gray-900 text-gray-100 p-4 rounded-lg overflow-x-auto text-sm font-mono" {...props} />
                ),
            }}
          >
            {summary}
          </ReactMarkdown>
        </div>
      </div>

      {/* Topics Section */}
      {topics && topics.length > 0 && (
        <div className="bg-white rounded-2xl p-8 border-2 border-gray-100 shadow-lg">
          <div className="flex items-center gap-3 mb-6 pb-4 border-b-2 border-purple-200">
            <div className="bg-gradient-to-br from-purple-400 to-pink-500 rounded-xl p-3 shadow-md">
              <span className="text-3xl">🏷️</span>
            </div>
            <h3 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              热门话题
            </h3>
          </div>
          <div className="flex flex-wrap gap-3">
            {topics.slice(0, 10).map((topic, index) => {
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
        </div>
      )}
    </div>
  );
}
