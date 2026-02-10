import React from 'react';

export interface LoadingSkeletonProps {
  variant?: 'text' | 'card' | 'stat' | 'pill' | 'avatar';
  width?: string;
  height?: string;
  className?: string;
}

/**
 * LoadingSkeleton - 骨架屏加载组件
 *
 * 用于显示加载占位符，提升感知性能
 *
 * @example
 * ```tsx
 * <LoadingSkeleton variant="text" />
 * <LoadingSkeleton variant="card" />
 * <LoadingSkeleton variant="stat" />
 * ```
 */
export const LoadingSkeleton = React.memo<LoadingSkeletonProps>(({
  variant = 'text',
  width,
  height,
  className = '',
}) => {
  const baseClass = 'animate-pulse bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 bg-[length:200%_100%]';

  const variantStyles = {
    text: 'h-4 rounded',
    card: 'h-48 rounded-xl',
    stat: 'h-24 rounded-xl',
    pill: 'h-8 rounded-full',
    avatar: 'w-10 h-10 rounded-full',
  };

  const style = {
    width: width || undefined,
    height: height || undefined,
  };

  return (
    <div
      className={`${baseClass} ${variantStyles[variant]} ${className}`}
      style={style}
    />
  );
});

LoadingSkeleton.displayName = 'LoadingSkeleton';

/**
 * TweetCardSkeleton - 推文卡片骨架屏
 */
export const TweetCardSkeleton = React.memo(() => {
  return (
    <div className="bg-white rounded-xl shadow-md p-4 border border-gray-200">
      {/* Header */}
      <div className="flex items-center gap-3 mb-3">
        <LoadingSkeleton variant="avatar" />
        <div className="flex-1 space-y-2">
          <LoadingSkeleton width="40%" />
          <LoadingSkeleton width="60%" />
        </div>
      </div>

      {/* Content */}
      <div className="space-y-2 mb-3">
        <LoadingSkeleton width="100%" />
        <LoadingSkeleton width="90%" />
        <LoadingSkeleton width="80%" />
      </div>

      {/* Metrics */}
      <div className="flex gap-2">
        <LoadingSkeleton variant="pill" width="80px" />
        <LoadingSkeleton variant="pill" width="80px" />
        <LoadingSkeleton variant="pill" width="80px" />
        <LoadingSkeleton variant="pill" width="80px" />
      </div>
    </div>
  );
});

TweetCardSkeleton.displayName = 'TweetCardSkeleton';

/**
 * EventCardSkeleton - 事件卡片骨架屏
 */
export const EventCardSkeleton = React.memo(() => {
  return (
    <div className="bg-gradient-to-br from-gray-50 to-gray-100 rounded-2xl overflow-hidden border border-gray-200 shadow-md">
      {/* Header */}
      <div className="bg-gray-300 px-5 py-4">
        <div className="flex items-center gap-3">
          <LoadingSkeleton variant="avatar" className="bg-gray-400" />
          <div className="flex-1 space-y-2">
            <LoadingSkeleton width="60%" className="bg-gray-400" />
            <LoadingSkeleton width="80%" className="bg-gray-400" />
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-4 space-y-3">
        <TweetCardSkeleton />
        <TweetCardSkeleton />
      </div>
    </div>
  );
});

EventCardSkeleton.displayName = 'EventCardSkeleton';

/**
 * StatCardSkeleton - 统计卡片骨架屏
 */
export const StatCardSkeleton = React.memo(() => {
  return (
    <div className="bg-gray-200 rounded-xl p-4 animate-pulse">
      <div className="flex items-center justify-between">
        <div className="w-12 h-12 bg-gray-300 rounded-full" />
        <div className="text-right space-y-2">
          <LoadingSkeleton width="60px" height="32px" className="bg-gray-300" />
          <LoadingSkeleton width="80px" className="bg-gray-300" />
        </div>
      </div>
    </div>
  );
});

StatCardSkeleton.displayName = 'StatCardSkeleton';

/**
 * PageLoadingSkeleton - 完整页面骨架屏
 */
export const PageLoadingSkeleton = React.memo(() => {
  return (
    <div className="space-y-6">
      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <StatCardSkeleton />
        <StatCardSkeleton />
        <StatCardSkeleton />
      </div>

      {/* Events */}
      <div className="space-y-5">
        <EventCardSkeleton />
        <EventCardSkeleton />
      </div>
    </div>
  );
});

PageLoadingSkeleton.displayName = 'PageLoadingSkeleton';
