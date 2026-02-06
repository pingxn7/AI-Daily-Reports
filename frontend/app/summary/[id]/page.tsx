'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { apiClient, DailySummaryDetail, formatFullDate } from '@/lib/api';
import { SummaryView } from '@/components/SummaryView';

export default function SummaryDetailPage() {
  const params = useParams();
  const router = useRouter();
  const [summary, setSummary] = useState<DailySummaryDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-5xl mx-auto px-4 py-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
            <div className="h-4 bg-gray-200 rounded w-1/4 mb-8"></div>
            <div className="space-y-4">
              <div className="h-64 bg-gray-200 rounded"></div>
              <div className="h-64 bg-gray-200 rounded"></div>
              <div className="h-64 bg-gray-200 rounded"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !summary) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            {error || 'Summary not found'}
          </h1>
          <button
            onClick={() => router.push('/')}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg">
        <div className="max-w-5xl mx-auto px-4 py-8">
          <button
            onClick={() => router.push('/')}
            className="mb-4 flex items-center gap-2 text-white/90 hover:text-white transition-colors"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
            </svg>
            Back to Summaries
          </button>
          <h1 className="text-4xl font-bold mb-2">AI News Digest</h1>
          <p className="text-xl text-white/90">{formatFullDate(summary.date)}</p>
        </div>
      </header>

      {/* Content */}
      <main className="max-w-5xl mx-auto px-4 py-8">
        <SummaryView summary={summary} />
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-5xl mx-auto px-4 py-6 text-center text-gray-600 text-sm">
          <p>AI News Collector - Powered by Claude API</p>
        </div>
      </footer>
    </div>
  );
}
