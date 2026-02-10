import React from 'react';

export interface MetricPillProps {
  icon: string;
  value: number | string;
  label?: string;
  variant?: 'like' | 'retweet' | 'reply' | 'bookmark';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const variantStyles = {
  like: {
    bg: 'from-red-50 to-pink-50',
    border: 'border-red-200',
    text: 'text-red-600',
  },
  retweet: {
    bg: 'from-green-50 to-emerald-50',
    border: 'border-green-200',
    text: 'text-green-600',
  },
  reply: {
    bg: 'from-blue-50 to-cyan-50',
    border: 'border-blue-200',
    text: 'text-blue-600',
  },
  bookmark: {
    bg: 'from-orange-50 to-amber-50',
    border: 'border-orange-200',
    text: 'text-orange-600',
  },
};

const sizeStyles = {
  sm: {
    container: 'px-2 py-1',
    icon: 'text-sm',
    text: 'text-xs',
  },
  md: {
    container: 'px-3 py-1.5',
    icon: 'text-base',
    text: 'text-xs',
  },
  lg: {
    container: 'px-4 py-2',
    icon: 'text-lg',
    text: 'text-sm',
  },
};

/**
 * MetricPill - 互动数据胶囊组件
 *
 * 用于展示社交媒体互动数据（点赞、转发、回复、收藏）
 *
 * @example
 * ```tsx
 * <MetricPill icon="👍" value={1234} variant="like" />
 * <MetricPill icon="🔁" value={345} variant="retweet" label="转发" />
 * ```
 */
export const MetricPill = React.memo<MetricPillProps>(({
  icon,
  value,
  label,
  variant = 'like',
  size = 'md',
  className = '',
}) => {
  const styles = variantStyles[variant];
  const sizes = sizeStyles[size];

  const formattedValue = typeof value === 'number'
    ? value.toLocaleString()
    : value;

  return (
    <div
      className={`
        inline-flex items-center gap-1.5
        bg-gradient-to-r ${styles.bg}
        border ${styles.border}
        rounded-full ${sizes.container}
        shadow-sm hover:shadow-md
        transition-all duration-200
        ${className}
      `}
    >
      <span className={sizes.icon}>{icon}</span>
      <span className={`${sizes.text} font-bold ${styles.text}`}>
        {formattedValue}
      </span>
      {label && (
        <span className={`${sizes.text} ${styles.text} opacity-75`}>
          {label}
        </span>
      )}
    </div>
  );
});

MetricPill.displayName = 'MetricPill';
