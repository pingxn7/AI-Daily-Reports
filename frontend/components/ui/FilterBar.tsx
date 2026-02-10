import React, { useState } from 'react';

export interface FilterOption {
  label: string;
  value: string;
}

export interface FilterBarProps {
  filters: {
    label: string;
    options: FilterOption[];
    value: string;
    onChange: (value: string) => void;
  }[];
  onReset?: () => void;
  className?: string;
}

/**
 * FilterBar - 筛选栏组件
 *
 * 用于提供多个筛选选项
 *
 * @example
 * ```tsx
 * <FilterBar
 *   filters={[
 *     {
 *       label: '话题',
 *       options: [
 *         { label: '全部', value: 'all' },
 *         { label: 'AI', value: 'ai' },
 *       ],
 *       value: selectedTopic,
 *       onChange: setSelectedTopic,
 *     },
 *   ]}
 * />
 * ```
 */
export const FilterBar = React.memo<FilterBarProps>(({
  filters,
  onReset,
  className = '',
}) => {
  return (
    <div
      className={`
        bg-white rounded-xl p-4 border border-gray-200 shadow-sm
        ${className}
      `}
    >
      <div className="flex flex-wrap items-center gap-4">
        {filters.map((filter, index) => (
          <div key={index} className="flex items-center gap-2">
            <label className="text-sm font-semibold text-gray-700">
              {filter.label}:
            </label>
            <select
              value={filter.value}
              onChange={(e) => filter.onChange(e.target.value)}
              className="
                px-3 py-1.5 text-sm
                border border-gray-300 rounded-lg
                bg-white text-gray-700
                focus:outline-none focus:ring-2 focus:ring-blue-500
                hover:border-gray-400
                transition-colors
              "
            >
              {filter.options.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        ))}

        {onReset && (
          <button
            onClick={onReset}
            className="
              ml-auto px-4 py-1.5 text-sm
              text-gray-600 hover:text-gray-900
              border border-gray-300 rounded-lg
              hover:bg-gray-50
              transition-colors
            "
          >
            重置
          </button>
        )}
      </div>
    </div>
  );
});

FilterBar.displayName = 'FilterBar';

/**
 * SortButton - 排序按钮组件
 */
export interface SortButtonProps {
  label: string;
  active: boolean;
  direction?: 'asc' | 'desc';
  onClick: () => void;
  className?: string;
}

export const SortButton = React.memo<SortButtonProps>(({
  label,
  active,
  direction = 'desc',
  onClick,
  className = '',
}) => {
  return (
    <button
      onClick={onClick}
      className={`
        inline-flex items-center gap-1.5 px-3 py-1.5
        text-sm font-semibold rounded-lg
        transition-all duration-200
        ${
          active
            ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-md'
            : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
        }
        ${className}
      `}
    >
      <span>{label}</span>
      {active && (
        <svg
          className={`w-4 h-4 transition-transform ${
            direction === 'asc' ? 'rotate-180' : ''
          }`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M19 9l-7 7-7-7"
          />
        </svg>
      )}
    </button>
  );
});

SortButton.displayName = 'SortButton';
