import React, { useState, useEffect } from 'react';

export interface ScrollToTopButtonProps {
  threshold?: number;
  className?: string;
}

/**
 * ScrollToTopButton - 返回顶部按钮组件
 *
 * 当页面滚动超过阈值时显示，点击平滑滚动到顶部
 *
 * @example
 * ```tsx
 * <ScrollToTopButton threshold={300} />
 * ```
 */
export const ScrollToTopButton = React.memo<ScrollToTopButtonProps>(({
  threshold = 300,
  className = '',
}) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const toggleVisibility = () => {
      if (window.pageYOffset > threshold) {
        setIsVisible(true);
      } else {
        setIsVisible(false);
      }
    };

    window.addEventListener('scroll', toggleVisibility);

    return () => {
      window.removeEventListener('scroll', toggleVisibility);
    };
  }, [threshold]);

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  };

  if (!isVisible) {
    return null;
  }

  return (
    <button
      onClick={scrollToTop}
      className={`
        fixed bottom-8 right-8 z-50
        w-12 h-12
        bg-gradient-to-br from-blue-500 to-purple-600
        text-white rounded-full
        shadow-lg hover:shadow-xl
        flex items-center justify-center
        transition-all duration-300
        hover:scale-110
        ${className}
      `}
      aria-label="返回顶部"
    >
      <svg
        className="w-6 h-6"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M5 10l7-7m0 0l7 7m-7-7v18"
        />
      </svg>
    </button>
  );
});

ScrollToTopButton.displayName = 'ScrollToTopButton';
