import React from 'react';

export interface TopicTagProps {
  topic: string;
  variant?: 'blue' | 'purple' | 'green' | 'orange' | 'rose' | 'indigo';
  size?: 'sm' | 'md' | 'lg';
  onClick?: (topic: string) => void;
  className?: string;
}

const variantStyles = {
  blue: 'from-blue-500 to-cyan-500',
  purple: 'from-purple-500 to-pink-500',
  green: 'from-green-500 to-emerald-500',
  orange: 'from-orange-500 to-amber-500',
  rose: 'from-rose-500 to-red-500',
  indigo: 'from-indigo-500 to-violet-500',
};

const sizeStyles = {
  sm: {
    container: 'px-2 py-0.5',
    text: 'text-xs',
  },
  md: {
    container: 'px-2.5 py-1',
    text: 'text-xs',
  },
  lg: {
    container: 'px-3 py-1.5',
    text: 'text-sm',
  },
};

/**
 * TopicTag - 话题标签胶囊组件
 *
 * 用于展示话题标签，支持点击交互
 *
 * @example
 * ```tsx
 * <TopicTag topic="AI" variant="blue" />
 * <TopicTag topic="GPT" variant="purple" onClick={(topic) => console.log(topic)} />
 * ```
 */
export const TopicTag = React.memo<TopicTagProps>(({
  topic,
  variant = 'blue',
  size = 'md',
  onClick,
  className = '',
}) => {
  const gradientClass = variantStyles[variant];
  const sizes = sizeStyles[size];

  const handleClick = () => {
    if (onClick) {
      onClick(topic);
    }
  };

  return (
    <span
      onClick={handleClick}
      className={`
        inline-flex items-center
        ${sizes.container}
        bg-gradient-to-r ${gradientClass}
        text-white ${sizes.text} font-bold
        rounded-full shadow-sm
        hover:shadow-md hover:scale-105
        transition-all duration-200
        ${onClick ? 'cursor-pointer' : ''}
        ${className}
      `}
    >
      #{topic}
    </span>
  );
});

TopicTag.displayName = 'TopicTag';

/**
 * TopicTagList - 话题标签列表组件
 *
 * 自动循环使用不同颜色的话题标签
 *
 * @example
 * ```tsx
 * <TopicTagList topics={['AI', 'GPT', 'OpenAI']} />
 * ```
 */
export interface TopicTagListProps {
  topics: string[];
  size?: 'sm' | 'md' | 'lg';
  maxTags?: number;
  onTagClick?: (topic: string) => void;
  className?: string;
}

export const TopicTagList = React.memo<TopicTagListProps>(({
  topics,
  size = 'md',
  maxTags,
  onTagClick,
  className = '',
}) => {
  const variants: Array<keyof typeof variantStyles> = [
    'blue',
    'purple',
    'green',
    'orange',
    'rose',
    'indigo',
  ];

  const displayTopics = maxTags ? topics.slice(0, maxTags) : topics;

  return (
    <div className={`flex flex-wrap gap-1.5 ${className}`}>
      {displayTopics.map((topic, index) => (
        <TopicTag
          key={`${topic}-${index}`}
          topic={topic}
          variant={variants[index % variants.length]}
          size={size}
          onClick={onTagClick}
        />
      ))}
    </div>
  );
});

TopicTagList.displayName = 'TopicTagList';
