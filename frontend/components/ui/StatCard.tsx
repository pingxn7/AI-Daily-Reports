import React from 'react';

export interface StatCardProps {
  icon: string;
  value: number | string;
  label: string;
  variant?: 'blue' | 'purple' | 'pink' | 'green' | 'orange' | 'indigo';
  animated?: boolean;
  className?: string;
}

const variantStyles = {
  blue: 'from-blue-500 to-blue-600',
  purple: 'from-purple-500 to-purple-600',
  pink: 'from-pink-500 to-pink-600',
  green: 'from-green-500 to-green-600',
  orange: 'from-orange-500 to-orange-600',
  indigo: 'from-indigo-500 to-indigo-600',
};

const labelColors = {
  blue: 'text-blue-100',
  purple: 'text-purple-100',
  pink: 'text-pink-100',
  green: 'text-green-100',
  orange: 'text-orange-100',
  indigo: 'text-indigo-100',
};

/**
 * StatCard - 统计卡片组件
 *
 * 用于展示统计数据，支持动画效果
 *
 * @example
 * ```tsx
 * <StatCard icon="📊" value={1234} label="监控推文" variant="blue" />
 * <StatCard icon="⭐" value="10" label="精选内容" variant="purple" animated />
 * ```
 */
export const StatCard = React.memo<StatCardProps>(({
  icon,
  value,
  label,
  variant = 'blue',
  animated = false,
  className = '',
}) => {
  const gradientClass = variantStyles[variant];
  const labelColor = labelColors[variant];

  const formattedValue = typeof value === 'number'
    ? value.toLocaleString()
    : value;

  return (
    <div
      className={`
        bg-gradient-to-br ${gradientClass}
        rounded-xl p-4 text-white shadow-md
        hover:shadow-lg transition-all duration-200
        ${animated ? 'hover:scale-105' : ''}
        ${className}
      `}
    >
      <div className="flex items-center justify-between">
        <span className="text-3xl">{icon}</span>
        <div className="text-right">
          <div className="text-2xl font-bold">
            {formattedValue}
          </div>
          <div className={`${labelColor} text-xs font-medium`}>
            {label}
          </div>
        </div>
      </div>
    </div>
  );
});

StatCard.displayName = 'StatCard';

/**
 * StatCardGrid - 统计卡片网格组件
 *
 * 自动布局多个统计卡片
 *
 * @example
 * ```tsx
 * <StatCardGrid stats={[
 *   { icon: '📊', value: 1234, label: '监控推文', variant: 'blue' },
 *   { icon: '⭐', value: 10, label: '精选内容', variant: 'purple' },
 * ]} />
 * ```
 */
export interface StatCardGridProps {
  stats: Array<Omit<StatCardProps, 'className'>>;
  columns?: 1 | 2 | 3 | 4;
  className?: string;
}

export const StatCardGrid = React.memo<StatCardGridProps>(({
  stats,
  columns = 3,
  className = '',
}) => {
  const gridCols = {
    1: 'grid-cols-1',
    2: 'grid-cols-1 md:grid-cols-2',
    3: 'grid-cols-1 md:grid-cols-3',
    4: 'grid-cols-1 md:grid-cols-2 lg:grid-cols-4',
  };

  return (
    <div className={`grid ${gridCols[columns]} gap-3 ${className}`}>
      {stats.map((stat, index) => (
        <StatCard key={index} {...stat} />
      ))}
    </div>
  );
});

StatCardGrid.displayName = 'StatCardGrid';
