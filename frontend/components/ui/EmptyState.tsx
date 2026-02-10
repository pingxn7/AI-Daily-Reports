import React from 'react';

export interface EmptyStateProps {
  icon?: string;
  title: string;
  description?: string;
  action?: {
    label: string;
    onClick: () => void;
  };
  className?: string;
}

/**
 * EmptyState - 空状态组件
 *
 * 用于显示无数据或空列表的状态
 *
 * @example
 * ```tsx
 * <EmptyState
 *   icon="📭"
 *   title="暂无数据"
 *   description="今天还没有收集到相关内容"
 * />
 * ```
 */
export const EmptyState = React.memo<EmptyStateProps>(({
  icon = '📭',
  title,
  description,
  action,
  className = '',
}) => {
  return (
    <div
      className={`
        text-center py-16
        bg-gradient-to-br from-gray-50 to-blue-50
        rounded-xl shadow-sm border border-gray-200
        ${className}
      `}
    >
      <div className="text-5xl mb-3">{icon}</div>
      <p className="text-gray-500 text-lg font-medium">{title}</p>
      {description && (
        <p className="text-gray-400 text-sm mt-1">{description}</p>
      )}
      {action && (
        <button
          onClick={action.onClick}
          className="
            mt-4 px-6 py-2
            bg-gradient-to-r from-blue-500 to-purple-600
            text-white rounded-lg font-semibold text-sm
            shadow-md hover:shadow-lg hover:scale-105
            transition-all duration-200
          "
        >
          {action.label}
        </button>
      )}
    </div>
  );
});

EmptyState.displayName = 'EmptyState';
