'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { apiClient, DailySummaryDetail, formatFullDate } from '@/lib/api';
import { SummaryView } from '@/components/SummaryView';
import { ShareButton } from '@/components/ShareButton';
import { ScrollToTop } from '@/components/ScrollToTop';
import { ReadingProgress } from '@/components/ReadingProgress';
import { ToastContainer, useToast } from '@/components/Toast';

export default function SummaryDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [summary, setSummary] = useState<DailySummaryDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { toasts, success, removeToast } = useToast();

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      // ESC: Go back to home
      if (e.key === 'Escape') {
        router.push('/');
      }
      // Arrow Up: Scroll to top
      if (e.key === 'ArrowUp' && e.ctrlKey) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
      // Arrow Down: Scroll to bottom
      if (e.key === 'ArrowDown' && e.ctrlKey) {
        e.preventDefault();
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [router]);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        setLoading(true);
        setError(null);

        const id = params.id as string;

        // Try to fetch by slug first, then by ID
        let data: DailySummaryDetail;
        if (isNaN(Number(id))) {
          // It's a slug
          data = await apiClient.getSummaryBySlug(id);
        } else {
          // It's an ID
          data = await apiClient.getSummaryById(Number(id));
        }

        setSummary(data);
      } catch (err: any) {
        console.error('Error fetching summary:', err);
        if (err.response?.status === 404) {
          setError('Summary not found');
        } else {
          setError('Failed to load summary. Please try again later.');
        }
      } finally {
        setLoading(false);
      }
    };

    if (params.id) {
      fetchSummary();
    }
  }, [params.id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50">
        {/* Header Skeleton */}
        <header className="relative bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white shadow-2xl overflow-hidden">
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full blur-3xl animate-pulse"></div>
            <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full blur-3xl animate-pulse"></div>
          </div>
          <div className="relative max-w-5xl mx-auto px-4 py-10">
            <div className="animate-pulse">
              <div className="h-10 bg-white/20 rounded-xl w-32 mb-6"></div>
              <div className="flex items-center gap-4 mb-4">
                <div className="bg-white/20 rounded-2xl p-4 w-20 h-20"></div>
                <div className="flex-1">
                  <div className="h-12 bg-white/20 rounded-xl w-64 mb-2"></div>
                  <div className="flex gap-3">
                    <div className="h-10 bg-white/20 rounded-xl w-40"></div>
                    <div className="h-10 bg-white/20 rounded-xl w-32"></div>
                    <div className="h-10 bg-white/20 rounded-xl w-32"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="absolute bottom-0 left-0 right-0">
            <svg viewBox="0 0 1440 48" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full">
              <path d="M0 48h1440V0c-240 48-480 48-720 24C480 0 240 0 0 24v24z" fill="rgb(249, 250, 251)" fillOpacity="0.5"/>
              <path d="M0 48h1440V12c-240 36-480 36-720 18C480 12 240 12 0 30v18z" fill="rgb(249, 250, 251)"/>
            </svg>
          </div>
        </header>

        {/* Content Skeleton */}
        <div className="max-w-5xl mx-auto px-4 py-8">
          <div className="animate-pulse space-y-6">
            {/* Stats Cards Skeleton */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="bg-white rounded-2xl p-6 shadow-lg">
                  <div className="flex items-center justify-between mb-2">
                    <div className="w-12 h-12 bg-gray-200 rounded-xl"></div>
                    <div className="text-right">
                      <div className="h-8 w-16 bg-gray-200 rounded mb-2"></div>
                      <div className="h-4 w-20 bg-gray-200 rounded"></div>
                    </div>
                  </div>
                  <div className="mt-4 h-1 bg-gray-200 rounded-full"></div>
                </div>
              ))}
            </div>

            {/* Content Cards Skeleton */}
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-2xl p-6 shadow-lg">
                <div className="h-6 bg-gray-200 rounded w-2/3 mb-4"></div>
                <div className="space-y-3">
                  <div className="h-4 bg-gray-200 rounded w-full"></div>
                  <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                  <div className="h-4 bg-gray-200 rounded w-4/6"></div>
                </div>
                <div className="mt-4 flex gap-2">
                  <div className="h-8 w-20 bg-gray-200 rounded-lg"></div>
                  <div className="h-8 w-20 bg-gray-200 rounded-lg"></div>
                  <div className="h-8 w-20 bg-gray-200 rounded-lg"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error || !summary) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50 flex items-center justify-center">
        <div className="text-center max-w-md mx-auto px-4">
          {/* Error Icon */}
          <div className="mb-8 relative">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full blur-3xl opacity-20 animate-pulse"></div>
            <div className="relative bg-white rounded-full w-32 h-32 mx-auto flex items-center justify-center shadow-2xl">
              <span className="text-6xl">😕</span>
            </div>
          </div>

          {/* Error Message */}
          <h1 className="text-4xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent mb-4">
            {error === 'Summary not found' ? '找不到报告' : '出错了'}
          </h1>
          <p className="text-gray-600 mb-8 text-lg">
            {error === 'Summary not found'
              ? '抱歉，我们找不到您要查看的报告。可能该报告不存在或已被删除。'
              : '加载报告时出现问题，请稍后重试。'}
          </p>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => router.push('/')}
              className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 flex items-center justify-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              <span>返回首页</span>
            </button>
            <button
              onClick={() => window.location.reload()}
              className="px-8 py-4 bg-white text-gray-700 rounded-xl font-semibold shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300 border-2 border-gray-200 flex items-center justify-center gap-2"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span>重新加载</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50">
      {/* Toast Notifications */}
      <ToastContainer toasts={toasts} onRemove={removeToast} />

      {/* Reading Progress Bar */}
      <ReadingProgress />

      {/* Scroll to Top Button */}
      <ScrollToTop />

      {/* Header */}
      <header className="relative bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 text-white shadow-2xl overflow-hidden">
        {/* Animated background pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full blur-3xl"></div>
        </div>

        <div className="relative max-w-5xl mx-auto px-4 py-10">
          <div className="flex items-center justify-between mb-6">
            <button
              onClick={() => router.push('/')}
              className="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-xl transition-all duration-300 hover:scale-105 shadow-lg"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              <span className="font-semibold">返回列表</span>
            </button>

            {/* Share Button */}
            <div className="hidden md:block">
              <ShareButton
                url={typeof window !== 'undefined' ? window.location.href : ''}
                title={`AI 行业日报 | ${formatFullDate(summary.date)}`}
                onCopySuccess={() => success('链接已复制到剪贴板！')}
              />
            </div>
          </div>

          <div className="flex items-center gap-4 mb-4">
            <div className="bg-white/20 backdrop-blur-sm rounded-2xl p-4 shadow-lg">
              <span className="text-5xl">🤖</span>
            </div>
            <div className="flex-1">
              <h1 className="text-5xl font-bold mb-2 drop-shadow-lg">AI 行业日报</h1>
              <div className="flex flex-wrap items-center gap-3">
                <div className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-xl shadow-lg">
                  <p className="text-xl font-semibold">{formatFullDate(summary.date)}</p>
                </div>
                <div className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-xl shadow-lg flex items-center gap-2">
                  <span className="text-lg">📊</span>
                  <span className="font-semibold">{summary.tweet_count} 条推文</span>
                </div>
                <div className="bg-white/20 backdrop-blur-sm px-4 py-2 rounded-xl shadow-lg flex items-center gap-2">
                  <span className="text-lg">⭐</span>
                  <span className="font-semibold">{summary.top_tweets_count} 条精选</span>
                </div>
              </div>
            </div>
          </div>

          {/* Mobile Share Button */}
          <div className="md:hidden mt-4">
            <ShareButton
              url={typeof window !== 'undefined' ? window.location.href : ''}
              title={`AI 行业日报 | ${formatFullDate(summary.date)}`}
              onCopySuccess={() => success('链接已复制到剪贴板！')}
            />
          </div>
        </div>

        {/* Wave decoration */}
        <div className="absolute bottom-0 left-0 right-0">
          <svg viewBox="0 0 1440 48" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full">
            <path d="M0 48h1440V0c-240 48-480 48-720 24C480 0 240 0 0 24v24z" fill="rgb(249, 250, 251)" fillOpacity="0.5"/>
            <path d="M0 48h1440V12c-240 36-480 36-720 18C480 12 240 12 0 30v18z" fill="rgb(249, 250, 251)"/>
          </svg>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-5xl mx-auto px-4 py-8 relative z-10">
        <SummaryView summary={summary} />
      </main>

      {/* Footer */}
      <footer className="relative bg-gradient-to-r from-gray-800 via-gray-900 to-black text-white mt-20 overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute inset-0 opacity-5">
          <div className="absolute top-0 left-1/4 w-64 h-64 bg-blue-500 rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 right-1/4 w-64 h-64 bg-purple-500 rounded-full blur-3xl"></div>
        </div>

        <div className="relative max-w-5xl mx-auto px-4 py-10">
          <div className="text-center">
            <div className="flex items-center justify-center gap-3 mb-4">
              <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl p-3 shadow-lg">
                <span className="text-3xl">🤖</span>
              </div>
              <h3 className="text-2xl font-bold">AI News Collector</h3>
            </div>
            <p className="text-gray-400 mb-4">
              由 Claude API 驱动的智能 AI 资讯聚合平台
            </p>
            <div className="flex items-center justify-center gap-4 text-sm text-gray-500">
              <span>📧 每日邮件推送</span>
              <span>•</span>
              <span>🔍 智能内容筛选</span>
              <span>•</span>
              <span>📊 数据可视化</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
