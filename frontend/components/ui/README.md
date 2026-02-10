# UI Components Library

可复用的UI组件库，用于今日精选事件版块和其他页面。

## 📦 组件列表

### 1. MetricPill - 互动数据胶囊

用于展示社交媒体互动数据（点赞、转发、回复、收藏）。

**Props:**
- `icon`: string - 图标（emoji）
- `value`: number | string - 数值
- `label?`: string - 标签文字（可选）
- `variant?`: 'like' | 'retweet' | 'reply' | 'bookmark' - 样式变体
- `size?`: 'sm' | 'md' | 'lg' - 尺寸
- `className?`: string - 自定义类名

**示例:**
```tsx
import { MetricPill } from '@/components/ui';

// 基础用法
<MetricPill icon="👍" value={1234} variant="like" />

// 带标签
<MetricPill icon="🔁" value={345} variant="retweet" label="转发" />

// 不同尺寸
<MetricPill icon="💬" value={89} variant="reply" size="sm" />
<MetricPill icon="🔖" value={234} variant="bookmark" size="lg" />
```

---

### 2. TopicTag - 话题标签胶囊

用于展示话题标签，支持点击交互。

**Props:**
- `topic`: string - 话题名称
- `variant?`: 'blue' | 'purple' | 'green' | 'orange' | 'rose' | 'indigo' - 颜色变体
- `size?`: 'sm' | 'md' | 'lg' - 尺寸
- `onClick?`: (topic: string) => void - 点击回调
- `className?`: string - 自定义类名

**示例:**
```tsx
import { TopicTag, TopicTagList } from '@/components/ui';

// 单个标签
<TopicTag topic="AI" variant="blue" />

// 可点击标签
<TopicTag
  topic="GPT"
  variant="purple"
  onClick={(topic) => console.log(topic)}
/>

// 标签列表（自动循环颜色）
<TopicTagList
  topics={['AI', 'GPT', 'OpenAI', '机器学习']}
  maxTags={10}
  onTagClick={(topic) => handleTopicClick(topic)}
/>
```

---

### 3. StatCard - 统计卡片

用于展示统计数据，支持动画效果。

**Props:**
- `icon`: string - 图标（emoji）
- `value`: number | string - 数值
- `label`: string - 标签文字
- `variant?`: 'blue' | 'purple' | 'pink' | 'green' | 'orange' | 'indigo' - 颜色变体
- `animated?`: boolean - 是否启用动画
- `className?`: string - 自定义类名

**示例:**
```tsx
import { StatCard, StatCardGrid } from '@/components/ui';

// 单个卡片
<StatCard
  icon="📊"
  value={1234}
  label="监控推文"
  variant="blue"
  animated
/>

// 卡片网格
<StatCardGrid
  stats={[
    { icon: '📊', value: 1234, label: '监控推文', variant: 'blue' },
    { icon: '⭐', value: 10, label: '精选内容', variant: 'purple' },
    { icon: '🔥', value: 5, label: '关键信息', variant: 'pink' },
  ]}
  columns={3}
/>
```

---

### 4. LoadingSkeleton - 骨架屏加载

用于显示加载占位符，提升感知性能。

**Props:**
- `variant?`: 'text' | 'card' | 'stat' | 'pill' | 'avatar' - 样式变体
- `width?`: string - 宽度
- `height?`: string - 高度
- `className?`: string - 自定义类名

**示例:**
```tsx
import {
  LoadingSkeleton,
  TweetCardSkeleton,
  EventCardSkeleton,
  PageLoadingSkeleton
} from '@/components/ui';

// 基础骨架屏
<LoadingSkeleton variant="text" />
<LoadingSkeleton variant="card" />

// 推文卡片骨架屏
<TweetCardSkeleton />

// 事件卡片骨架屏
<EventCardSkeleton />

// 完整页面骨架屏
<PageLoadingSkeleton />
```

---

### 5. FilterBar - 筛选栏

用于提供多个筛选选项。

**Props:**
- `filters`: Array - 筛选器配置数组
- `onReset?`: () => void - 重置回调
- `className?`: string - 自定义类名

**示例:**
```tsx
import { FilterBar } from '@/components/ui';

const [selectedTopic, setSelectedTopic] = useState('all');
const [selectedSort, setSelectedSort] = useState('time');

<FilterBar
  filters={[
    {
      label: '话题',
      options: [
        { label: '全部', value: 'all' },
        { label: 'AI', value: 'ai' },
        { label: 'GPT', value: 'gpt' },
      ],
      value: selectedTopic,
      onChange: setSelectedTopic,
    },
    {
      label: '排序',
      options: [
        { label: '时间', value: 'time' },
        { label: '热度', value: 'hot' },
      ],
      value: selectedSort,
      onChange: setSelectedSort,
    },
  ]}
  onReset={() => {
    setSelectedTopic('all');
    setSelectedSort('time');
  }}
/>
```

---

### 6. SortButton - 排序按钮

用于排序功能。

**Props:**
- `label`: string - 按钮文字
- `active`: boolean - 是否激活
- `direction?`: 'asc' | 'desc' - 排序方向
- `onClick`: () => void - 点击回调
- `className?`: string - 自定义类名

**示例:**
```tsx
import { SortButton } from '@/components/ui';

const [sortBy, setSortBy] = useState('time');
const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');

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
```

---

### 7. ScrollToTopButton - 返回顶部按钮

当页面滚动超过阈值时显示，点击平滑滚动到顶部。

**Props:**
- `threshold?`: number - 显示阈值（默认300px）
- `className?`: string - 自定义类名

**示例:**
```tsx
import { ScrollToTopButton } from '@/components/ui';

// 基础用法
<ScrollToTopButton />

// 自定义阈值
<ScrollToTopButton threshold={500} />
```

---

### 8. EmptyState - 空状态

用于显示无数据或空列表的状态。

**Props:**
- `icon?`: string - 图标（emoji）
- `title`: string - 标题
- `description?`: string - 描述
- `action?`: { label: string; onClick: () => void } - 操作按钮
- `className?`: string - 自定义类名

**示例:**
```tsx
import { EmptyState } from '@/components/ui';

// 基础用法
<EmptyState
  icon="📭"
  title="暂无数据"
  description="今天还没有收集到相关内容"
/>

// 带操作按钮
<EmptyState
  icon="🔍"
  title="未找到结果"
  description="尝试调整筛选条件"
  action={{
    label: '重置筛选',
    onClick: () => resetFilters(),
  }}
/>
```

---

## 🎨 设计系统

### 颜色变体

**MetricPill:**
- `like`: 红色系（点赞）
- `retweet`: 绿色系（转发）
- `reply`: 蓝色系（回复）
- `bookmark`: 橙色系（收藏）

**TopicTag:**
- `blue`: 蓝色渐变
- `purple`: 紫色渐变
- `green`: 绿色渐变
- `orange`: 橙色渐变
- `rose`: 玫瑰色渐变
- `indigo`: 靛蓝色渐变

**StatCard:**
- `blue`: 蓝色渐变
- `purple`: 紫色渐变
- `pink`: 粉色渐变
- `green`: 绿色渐变
- `orange`: 橙色渐变
- `indigo`: 靛蓝色渐变

### 尺寸规范

**sm (小):**
- padding: px-2 py-1
- font-size: text-xs

**md (中):**
- padding: px-3 py-1.5
- font-size: text-xs / text-sm

**lg (大):**
- padding: px-4 py-2
- font-size: text-sm / text-base

---

## 🚀 使用示例

### 完整页面示例

```tsx
import {
  StatCardGrid,
  TopicTagList,
  MetricPill,
  FilterBar,
  SortButton,
  ScrollToTopButton,
  PageLoadingSkeleton,
  EmptyState,
} from '@/components/ui';

export function EventsPage() {
  const [loading, setLoading] = useState(true);
  const [events, setEvents] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState('all');

  if (loading) {
    return <PageLoadingSkeleton />;
  }

  if (events.length === 0) {
    return (
      <EmptyState
        icon="📭"
        title="暂无事件"
        description="今天还没有收集到相关内容"
      />
    );
  }

  return (
    <div className="space-y-6">
      {/* 统计面板 */}
      <StatCardGrid
        stats={[
          { icon: '📊', value: 1234, label: '监控推文', variant: 'blue' },
          { icon: '⭐', value: 10, label: '精选事件', variant: 'purple' },
          { icon: '🔥', value: 5, label: '关键信息', variant: 'pink' },
        ]}
      />

      {/* 筛选栏 */}
      <FilterBar
        filters={[
          {
            label: '话题',
            options: [
              { label: '全部', value: 'all' },
              { label: 'AI', value: 'ai' },
            ],
            value: selectedTopic,
            onChange: setSelectedTopic,
          },
        ]}
      />

      {/* 事件列表 */}
      <div className="space-y-5">
        {events.map((event) => (
          <div key={event.id} className="bg-white rounded-xl p-4">
            <h3>{event.title}</h3>

            {/* 话题标签 */}
            <TopicTagList topics={event.topics} maxTags={5} />

            {/* 互动数据 */}
            <div className="flex gap-2 mt-3">
              <MetricPill icon="👍" value={event.likes} variant="like" />
              <MetricPill icon="🔁" value={event.retweets} variant="retweet" />
              <MetricPill icon="💬" value={event.replies} variant="reply" />
              <MetricPill icon="🔖" value={event.bookmarks} variant="bookmark" />
            </div>
          </div>
        ))}
      </div>

      {/* 返回顶部按钮 */}
      <ScrollToTopButton />
    </div>
  );
}
```

---

## 📝 注意事项

1. **性能优化**: 所有组件都使用了 `React.memo` 进行优化
2. **响应式设计**: 所有组件都支持移动端适配
3. **可访问性**: 按钮组件包含 `aria-label` 属性
4. **类型安全**: 所有组件都提供了完整的 TypeScript 类型定义

---

## 🔧 自定义样式

所有组件都支持通过 `className` prop 添加自定义样式：

```tsx
<MetricPill
  icon="👍"
  value={1234}
  variant="like"
  className="my-custom-class"
/>
```

---

## 📦 导入方式

```tsx
// 导入单个组件
import { MetricPill } from '@/components/ui';

// 导入多个组件
import {
  MetricPill,
  TopicTag,
  StatCard
} from '@/components/ui';

// 导入类型
import type {
  MetricPillProps,
  TopicTagProps
} from '@/components/ui';
```
