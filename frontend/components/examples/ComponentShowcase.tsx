import React, { useState } from 'react';
import {
  MetricPill,
  TopicTag,
  TopicTagList,
  StatCard,
  StatCardGrid,
  LoadingSkeleton,
  TweetCardSkeleton,
  EventCardSkeleton,
  PageLoadingSkeleton,
  FilterBar,
  SortButton,
  ScrollToTopButton,
  EmptyState,
} from '../ui';

/**
 * ComponentShowcase - 组件展示页面
 *
 * 展示所有UI组件的使用方法和效果
 */
export function ComponentShowcase() {
  const [selectedTopic, setSelectedTopic] = useState('all');
  const [sortBy, setSortBy] = useState('time');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');
  const [showLoading, setShowLoading] = useState(false);

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-12">
      <header className="text-center mb-12">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
          UI组件库展示
        </h1>
        <p className="text-gray-600">
          可复用的UI组件，统一的设计语言，完整的TypeScript类型定义
        </p>
      </header>

      {/* MetricPill 组件 */}
      <section className="bg-white rounded-xl p-6 shadow-md">
        <h2 className="text-2xl font-bold mb-4 text-gray-900">
          MetricPill - 互动数据胶囊
        </h2>
        <p className="text-gray-600 mb-6">
          用于展示社交媒体互动数据，支持4种颜色变体和3种尺寸
        </p>

        <div className="space-y-4">
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-2">标准尺寸</h3>
            <div className="flex flex-wrap gap-3">
              <MetricPill icon="👍" value={1234} variant="like" />
              <MetricPill icon="🔁" value={345} variant="retweet" />
              <MetricPill icon="💬" value={89} variant="reply" />
              <MetricPill icon="🔖" value={234} variant="bookmark" />
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-2">带标签</h3>
            <div className="flex flex-wrap gap-3">
              <MetricPill icon="👍" value={1234} variant="like" label="点赞" />
              <MetricPill icon="🔁" value={345} variant="retweet" label="转发" />
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-2">不同尺寸</h3>
            <div className="flex flex-wrap items-center gap-3">
              <MetricPill icon="👍" value={1234} variant="like" size="sm" />
              <MetricPill icon="👍" value={1234} variant="like" size="md" />
              <MetricPill icon="👍" value={1234} variant="like" size="lg" />
            </div>
          </div>
        </div>

        <div className="mt-6 bg-gray-50 rounded-lg p-4">
          <pre className="text-xs text-gray-700 overflow-x-auto">
{`<MetricPill icon="👍" value={1234} variant="like" />
<MetricPill icon="🔁" value={345} variant="retweet" label="转发" />
<MetricPill icon="💬" value={89} variant="reply" size="sm" />`}
          </pre>
        </div>
      </section>

      {/* TopicTag 组件 */}
      <section className="bg-white rounded-xl p-6 shadow-md">
        <h2 className="text-2xl font-bold mb-4 text-gray-900">
          TopicTag - 话题标签胶囊
        </h2>
        <p className="text-gray-600 mb-6">
          用于展示话题标签，支持6种渐变色和点击交互
        </p>

        <div className="space-y-4">
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-2">单个标签</h3>
            <div className="flex flex-wrap gap-2">
              <TopicTag topic="AI" variant="blue" />
              <TopicTag topic="GPT" variant="purple" />
              <TopicTag topic="OpenAI" variant="green" />
              <TopicTag topic="机器学习" variant="orange" />
              <TopicTag topic="深度学习" variant="rose" />
              <TopicTag topic="神经网络" variant="indigo" />
            </div>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-2">标签列表（自动循环颜色）</h3>
            <TopicTagList
              topics={['AI', 'GPT', 'OpenAI', '机器学习', '深度学习', '神经网络', 'Transformer', 'LLM']}
              onTagClick={(topic) => alert(`点击了: ${topic}`)}
            />
          </div>
        </div>

        <div className="mt-6 bg-gray-50 rounded-lg p-4">
          <pre className="text-xs text-gray-700 overflow-x-auto">
{`<TopicTag topic="AI" variant="blue" />
<TopicTagList
  topics={['AI', 'GPT', 'OpenAI']}
  onTagClick={(topic) => console.log(topic)}
/>`}
          </pre>
        </div>
      </section>

      {/* StatCard 组件 */}
      <section className="bg-white rounded-xl p-6 shadow-md">
        <h2 className="text-2xl font-bold mb-4 text-gray-900">
          StatCard - 统计卡片
        </h2>
        <p className="text-gray-600 mb-6">
          用于展示统计数据，支持6种颜色和动画效果
        </p>

        <StatCardGrid
          stats={[
            { icon: '📊', value: 1234, label: '监控推文', variant: 'blue', animated: true },
            { icon: '⭐', value: 10, label: '精选事件', variant: 'purple', animated: true },
            { icon: '🔥', value: 5, label: '关键信息', variant: 'pink', animated: true },
          ]}
        />

        <div className="mt-6 bg-gray-50 rounded-lg p-4">
          <pre className="text-xs text-gray-700 overflow-x-auto">
{`<StatCardGrid
  stats={[
    { icon: '📊', value: 1234, label: '监控推文', variant: 'blue' },
    { icon: '⭐', value: 10, label: '精选事件', variant: 'purple' },
  ]}
/>`}
          </pre>
        </div>
      </section>

      {/* LoadingSkeleton 组件 */}
      <section className="bg-white rounded-xl p-6 shadow-md">
        <h2 className="text-2xl font-bold mb-4 text-gray-900">
          LoadingSkeleton - 骨架屏加载
        </h2>
        <p className="text-gray-600 mb-6">
          用于显示加载占位符，提升感知性能
        </p>

        <div className="flex items-center gap-4 mb-6">
          <button
            onClick={() => setShowLoading(!showLoading)}
            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
          >
            {showLoading ? '隐藏骨架屏' : '显示骨架屏'}
          </button>
        </div>

        {showLoading ? (
          <div className="space-y-4">
            <TweetCardSkeleton />
            <EventCardSkeleton />
          </div>
        ) : (
          <div className="space-y-4">
            <div className="bg-gray-50 rounded-lg p-4">
              <p className="text-gray-600">点击按钮查看骨架屏效果</p>
            </div>
          </div>
        )}

        <div className="mt-6 bg-gray-50 rounded-lg p-4">
          <pre className="text-xs text-gray-700 overflow-x-auto">
{`<TweetCardSkeleton />
<EventCardSkeleton />
<PageLoadingSkeleton />`}
          </pre>
        </div>
      </section>

      {/* FilterBar 组件 */}
      <section className="bg-white rounded-xl p-6 shadow-md">
        <h2 className="text-2xl font-bold mb-4 text-gray-900">
          FilterBar - 筛选栏
        </h2>
        <p className="text-gray-600 mb-6">
          用于提供多个筛选选项
        </p>

        <FilterBar
          filters={[
            {
              label: '话题',
              options: [
                { label: '全部', value: 'all' },
                { label: 'AI', value: 'ai' },
                { label: 'GPT', value: 'gpt' },
                { label: 'OpenAI', value: 'openai' },
              ],
              value: selectedTopic,
              onChange: setSelectedTopic,
            },
          ]}
          onReset={() => setSelectedTopic('all')}
        />

        <div className="mt-4 text-sm text-gray-600">
          当前选择: <span className="font-semibold">{selectedTopic}</span>
        </div>

        <div className="mt-6 bg-gray-50 rounded-lg p-4">
          <pre className="text-xs text-gray-700 overflow-x-auto">
{`<FilterBar
  filters={[
    {
      label: '话题',
      options: [{ label: '全部', value: 'all' }],
      value: selectedTopic,
      onChange: setSelectedTopic,
    },
  ]}
/>`}
          </pre>
        </div>
      </section>

      {/* SortButton 组件 */}
      <section className="bg-white rounded-xl p-6 shadow-md">
        <h2 className="text-2xl font-bold mb-4 text-gray-900">
          SortButton - 排序按钮
        </h2>
        <p className="text-gray-600 mb-6">
          用于排序功能，支持升序/降序切换
        </p>

        <div className="flex gap-2">
          <SortButton
            label="时间"
            active={sortBy === 'time'}
            direction={sortDirection}
            onClick={() => {
              if (sortBy === 'time') {
                setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
              } else {
                setSortBy('time');
              }
            }}
          />
          <SortButton
            label="热度"
            active={sortBy === 'hot'}
            direction={sortDirection}
            onClick={() => {
              if (sortBy === 'hot') {
                setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
              } else {
                setSortBy('hot');
              }
            }}
          />
        </div>

        <div className="mt-4 text-sm text-gray-600">
          当前排序: <span className="font-semibold">{sortBy}</span> ({sortDirection === 'asc' ? '升序' : '降序'})
        </div>

        <div className="mt-6 bg-gray-50 rounded-lg p-4">
          <pre className="text-xs text-gray-700 overflow-x-auto">
{`<SortButton
  label="时间"
  active={sortBy === 'time'}
  direction={sortDirection}
  onClick={() => handleSort('time')}
/>`}
          </pre>
        </div>
      </section>

      {/* EmptyState 组件 */}
      <section className="bg-white rounded-xl p-6 shadow-md">
        <h2 className="text-2xl font-bold mb-4 text-gray-900">
          EmptyState - 空状态
        </h2>
        <p className="text-gray-600 mb-6">
          用于显示无数据或空列表的状态
        </p>

        <div className="space-y-4">
          <EmptyState
            icon="📭"
            title="暂无数据"
            description="今天还没有收集到相关内容"
          />

          <EmptyState
            icon="🔍"
            title="未找到结果"
            description="尝试调整筛选条件"
            action={{
              label: '重置筛选',
              onClick: () => alert('重置筛选'),
            }}
          />
        </div>

        <div className="mt-6 bg-gray-50 rounded-lg p-4">
          <pre className="text-xs text-gray-700 overflow-x-auto">
{`<EmptyState
  icon="📭"
  title="暂无数据"
  description="今天还没有收集到相关内容"
  action={{
    label: '重置筛选',
    onClick: () => handleReset(),
  }}
/>`}
          </pre>
        </div>
      </section>

      {/* ScrollToTopButton 组件 */}
      <ScrollToTopButton />

      <footer className="text-center py-8 text-gray-500 text-sm">
        <p>UI组件库 v1.0.0</p>
        <p className="mt-2">查看完整文档: frontend/components/ui/README.md</p>
      </footer>
    </div>
  );
}
