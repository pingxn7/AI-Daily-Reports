'use client';

import React from 'react';

interface ProgressBarProps {
  value: number;
  max: number;
  label?: string;
  color?: 'blue' | 'purple' | 'green' | 'orange' | 'red';
  showPercentage?: boolean;
  className?: string;
}

export function ProgressBar({
  value,
  max,
  label,
  color = 'blue',
  showPercentage = true,
  className = '',
}: ProgressBarProps) {
  const percentage = Math.min((value / max) * 100, 100);

  const getColorClasses = () => {
    switch (color) {
      case 'blue':
        return 'from-blue-500 to-cyan-500';
      case 'purple':
        return 'from-purple-500 to-pink-500';
      case 'green':
        return 'from-green-500 to-emerald-500';
      case 'orange':
        return 'from-orange-500 to-amber-500';
      case 'red':
        return 'from-red-500 to-rose-500';
      default:
        return 'from-blue-500 to-cyan-500';
    }
  };

  return (
    <div className={`space-y-2 ${className}`}>
      {label && (
        <div className="flex items-center justify-between text-sm">
          <span className="font-medium text-gray-700">{label}</span>
          {showPercentage && (
            <span className="text-gray-500">{percentage.toFixed(0)}%</span>
          )}
        </div>
      )}
      <div className="relative h-3 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`absolute inset-y-0 left-0 bg-gradient-to-r ${getColorClasses()} rounded-full transition-all duration-1000 ease-out`}
          style={{ width: `${percentage}%` }}
        >
          {/* Shimmer effect */}
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent animate-shimmer"></div>
        </div>
      </div>
    </div>
  );
}

// Bar Chart Component
interface BarChartProps {
  data: Array<{ label: string; value: number; color?: string }>;
  maxValue?: number;
  className?: string;
}

export function BarChart({ data, maxValue, className = '' }: BarChartProps) {
  const max = maxValue || Math.max(...data.map((d) => d.value));

  return (
    <div className={`space-y-3 ${className}`}>
      {data.map((item, index) => (
        <div key={index} className="space-y-1">
          <div className="flex items-center justify-between text-sm">
            <span className="font-medium text-gray-700">{item.label}</span>
            <span className="text-gray-500">{item.value.toLocaleString()}</span>
          </div>
          <div className="relative h-8 bg-gray-100 rounded-lg overflow-hidden">
            <div
              className={`absolute inset-y-0 left-0 ${
                item.color || 'bg-gradient-to-r from-blue-500 to-purple-600'
              } rounded-lg transition-all duration-1000 ease-out flex items-center justify-end px-3`}
              style={{ width: `${(item.value / max) * 100}%` }}
            >
              <span className="text-white text-xs font-bold">
                {item.value.toLocaleString()}
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
