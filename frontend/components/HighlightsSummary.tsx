import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface HighlightsSummaryProps {
  summary: string;
  tweetCount: number;
  topTweetsCount: number;
  topics: string[] | null;
}

// 分类标签图标映射
const categoryIcons: { [key: string]: string } = {
  '模型': '🤖',
  '产品': '📦',
  '市场': '📈',
  '应用': '⚡',
  '研究': '🔬',
  '融资': '💰',
  '政策': '📋',
  '人物': '👤',
  '公司': '🏢',
  '技术': '⚙️',
  '开源': '🌟',
  '数据': '📊',
};

// 处理文本中的分类标签，添加图标
const processTextWithIcons = (text: string) => {
  const regex = /【([^】]+)】/g;
  const parts = [];
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(text)) !== null) {
    // 添加标签前的文本
    if (match.index > lastIndex) {
      parts.push(text.substring(lastIndex, match.index));
    }

    const category = match[1];
    const icon = categoryIcons[category] || '📌';

    // 添加带图标的标签 - Colorful Pill Style
    parts.push(
      <span key={match.index} className="inline-flex items-center gap-1 px-2.5 py-0.5 bg-gradient-to-r from-blue-500 to-indigo-600 text-white rounded-full font-bold text-xs shadow-sm mx-0.5">
        <span className="text-sm">{icon}</span>
        <span>{category}</span>
      </span>
    );

    lastIndex = match.index + match[0].length;
  }

  // 添加剩余文本
  if (lastIndex < text.length) {
    parts.push(text.substring(lastIndex));
  }

  return parts.length > 0 ? parts : text;
};

export function HighlightsSummary({
  summary,
  tweetCount,
  topTweetsCount,
  topics,
}: HighlightsSummaryProps) {
  return (
    <div className="space-y-6 mb-8">
      {/* Statistics Dashboard - Compact */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-4 text-white shadow-md hover:shadow-lg transition-all duration-200">
          <div className="flex items-center justify-between">
            <span className="text-3xl">📊</span>
            <div className="text-right">
              <div className="text-2xl font-bold">{tweetCount}</div>
              <div className="text-blue-100 text-xs font-medium">监控推文</div>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-4 text-white shadow-md hover:shadow-lg transition-all duration-200">
          <div className="flex items-center justify-between">
            <span className="text-3xl">⭐</span>
            <div className="text-right">
              <div className="text-2xl font-bold">{topTweetsCount}</div>
              <div className="text-purple-100 text-xs font-medium">精选内容</div>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-pink-500 to-pink-600 rounded-xl p-4 text-white shadow-md hover:shadow-lg transition-all duration-200">
          <div className="flex items-center justify-between">
            <span className="text-3xl">🏷️</span>
            <div className="text-right">
              <div className="text-2xl font-bold">{topics?.length || 0}</div>
              <div className="text-pink-100 text-xs font-medium">热门话题</div>
            </div>
          </div>
        </div>
      </div>

      {/* AI-generated summary with Markdown rendering and category icons */}
      <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-6 border border-blue-200 shadow-md">
        <div className="flex items-center gap-3 mb-5">
          <div className="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-xl p-2.5 shadow-sm">
            <span className="text-2xl">📌</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-900">
            今日关键信息
          </h2>
        </div>

        <div className="prose prose-base max-w-none markdown-content">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              h1: ({ node, ...props }) => (
                <h1 className="text-2xl font-bold text-gray-900 mt-6 mb-3 flex items-center gap-2" {...props} />
              ),
              h2: ({ node, children, ...props }) => (
                <h2 className="text-xl font-bold text-gray-800 mt-5 mb-3 pb-2 border-b border-gray-300 flex items-center gap-2" {...props}>
                  {children}
                </h2>
              ),
              h3: ({ node, ...props }) => (
                <h3 className="text-lg font-bold text-gray-800 mt-4 mb-2" {...props} />
              ),
              h4: ({ node, ...props }) => (
                <h4 className="text-base font-semibold text-gray-700 mt-3 mb-2" {...props} />
              ),
              p: ({ node, children, ...props }) => {
                // 处理段落中的分类标签
                if (typeof children === 'string') {
                  return (
                    <p className="text-gray-700 leading-relaxed mb-2 text-sm" {...props}>
                      {processTextWithIcons(children)}
                    </p>
                  );
                }
                return (
                  <p className="text-gray-700 leading-relaxed mb-2 text-sm" {...props}>
                    {children}
                  </p>
                );
              },
              ul: ({ node, ...props }) => (
                <ul className="space-y-2 mb-4 ml-2" {...props} />
              ),
              ol: ({ node, ...props }) => (
                <ol className="space-y-2 mb-4 ml-2" {...props} />
              ),
              li: ({ node, children, ...props }) => {
                // 处理列表项中的分类标签
                const processedChildren = React.Children.map(children, (child) => {
                  if (typeof child === 'string') {
                    return processTextWithIcons(child);
                  }
                  return child;
                });

                return (
                  <li className="text-gray-700 leading-relaxed pl-2 text-sm relative before:content-['•'] before:absolute before:left-[-12px] before:text-blue-500 before:font-bold" {...props}>
                    {processedChildren}
                  </li>
                );
              },
              hr: ({ node, ...props }) => (
                <hr className="my-6 border-t border-gray-300" {...props} />
              ),
              blockquote: ({ node, ...props }) => (
                <blockquote className="border-l-4 border-blue-500 pl-3 py-2 my-3 bg-white/60 rounded-r-lg" {...props} />
              ),
              a: ({ node, ...props }) => (
                <a className="text-blue-600 hover:text-blue-700 underline font-medium" target="_blank" rel="noopener noreferrer" {...props} />
              ),
              strong: ({ node, ...props }) => (
                <strong className="font-bold text-gray-900" {...props} />
              ),
              em: ({ node, ...props }) => (
                <em className="italic text-gray-800" {...props} />
              ),
              code: ({ node, inline, ...props }: any) =>
                inline ? (
                  <code className="bg-white text-red-600 px-1.5 py-0.5 rounded text-xs font-mono border border-gray-200" {...props} />
                ) : (
                  <code className="block bg-gray-900 text-gray-100 p-3 rounded-lg overflow-x-auto text-xs font-mono my-3" {...props} />
                ),
            }}
          >
            {summary}
          </ReactMarkdown>
        </div>
      </div>

      {/* Topics Section */}
      {topics && topics.length > 0 && (
        <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-6 border border-purple-200 shadow-md">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-gradient-to-br from-purple-400 to-pink-500 rounded-xl p-2.5 shadow-sm">
              <span className="text-2xl">🏷️</span>
            </div>
            <h3 className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              热门话题
            </h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {topics.slice(0, 10).map((topic, index) => {
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
        </div>
      )}
    </div>
  );
}
