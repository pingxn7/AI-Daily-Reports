'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { apiClient, DailySummaryList, formatFullDate } from '@/lib/api';

export default function HomePage() {
  const router = useRouter();
  const [summaries, setSummaries] = useState<DailySummaryList[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    const fetchSummaries = async () => {
      try {
        setLoading(true);
        setError(null);

        const data = await apiClient.listSummaries(page, 10);
        setSummaries(data.items);
        setTotalPages(data.total_pages);
      } catch (err: any) {
        console.error('Error fetching summaries:', err);
        setError('Failed to load summaries. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchSummaries();
  }, [page]);

  const handleSummaryClick = (slug: string) => {
    router.push(`/summary/${slug}`);
  };

  const handlePreviousPage = () => {
    if (page > 1) {
      setPage(page - 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  const handleNextPage = () => {
    if (page < totalPages) {
      setPage(page + 1);
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg">
        <div className="max-w-5xl mx-auto px-4 py-12">
          <div className="flex items-center gap-3 mb-4">
            <span className="text-5xl">🤖</span>
            <h1 className="text-5xl font-bold">AI News Collector</h1>
          </div>
          <p className="text-xl text-white/90">
            Daily AI news curated from Twitter, analyzed by Claude
          </p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-5xl mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">Daily Summaries</h2>
          <p className="text-gray-600">
            Browse through our collection of AI news summaries
          </p>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="space-y-4">
            {[1, 2, 3].map((i) => (
              <div key={i} className="bg-white rounded-lg shadow-md p-6 animate-pulse">
                <div className="h-6 bg-gray-200 rounded w-1/3 mb-3"></div>
                <div className="h-4 bg-gray-200 rounded w-1/4 mb-4"></div>
                <div className="h-20 bg-gray-200 rounded mb-3"></div>
                <div className="flex gap-2">
                  <div className="h-6 bg-gray-200 rounded w-16"></div>
                  <div className="h-6 bg-gray-200 rounded w-16"></div>
                  <div className="h-6 bg-gray-200 rounded w-16"></div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Error State */}
        {error && !loading && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
            <p className="text-red-700 text-lg">{error}</p>
            <button
              onClick={() => window.location.reload()}
              className="mt-4 px-6 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
            >
              Retry
            </button>
          </div>
        )}

        {/* Summaries List */}
        {!loading && !error && summaries.length > 0 && (
          <>
            <div className="space-y-6">
              {summaries.map((summary) => (
                <div
                  key={summary.id}
                  onClick={() => handleSummaryClick(summary.url_slug)}
                  className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow cursor-pointer border border-gray-200"
                >
                  {/* Date */}
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="text-2xl font-bold text-gray-900">
                      {formatFullDate(summary.date)}
                    </h3>
                    {summary.email_sent_at && (
                      <span className="px-3 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">
                        ✓ Email Sent
                      </span>
                    )}
                  </div>

                  {/* Stats */}
                  <div className="flex items-center gap-4 text-sm text-gray-600 mb-4">
                    <span className="flex items-center gap-1">
                      <span className="font-semibold">{summary.tweet_count}</span>
                      <span>AI tweets</span>
                    </span>
                    <span className="text-gray-300">|</span>
                    <span className="flex items-center gap-1">
                      <span className="font-semibold text-blue-600">{summary.top_tweets_count}</span>
                      <span>curated highlights</span>
                    </span>
                    <span className="text-gray-300">|</span>
                    <span className="flex items-center gap-1">
                      <span className="font-semibold">{summary.other_tweets_count}</span>
                      <span>more news</span>
                    </span>
                  </div>

                  {/* Highlights Summary Preview */}
                  {summary.highlights_summary && (
                    <div className="mb-4 p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
                      <p className="text-sm text-gray-700 line-clamp-3 leading-relaxed">
                        {summary.highlights_summary}
                      </p>
                    </div>
                  )}

                  {/* Topics */}
                  {summary.topics && summary.topics.length > 0 && (
                    <div className="flex flex-wrap gap-2 mb-4">
                      {summary.topics.slice(0, 6).map((topic, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-purple-100 text-purple-700 text-xs font-medium rounded-full"
                        >
                          {topic}
                        </span>
                      ))}
                      {summary.topics.length > 6 && (
                        <span className="px-3 py-1 bg-gray-100 text-gray-600 text-xs font-medium rounded-full">
                          +{summary.topics.length - 6} more
                        </span>
                      )}
                    </div>
                  )}

                  {/* View Link */}
                  <div className="flex items-center gap-2 text-blue-600 font-medium">
                    <span>View full summary</span>
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="mt-8 flex items-center justify-center gap-4">
                <button
                  onClick={handlePreviousPage}
                  disabled={page === 1}
                  className={`px-6 py-3 rounded-lg font-medium transition-colors ${
                    page === 1
                      ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                      : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
                  }`}
                >
                  Previous
                </button>
                <span className="text-gray-600">
                  Page {page} of {totalPages}
                </span>
                <button
                  onClick={handleNextPage}
                  disabled={page === totalPages}
                  className={`px-6 py-3 rounded-lg font-medium transition-colors ${
                    page === totalPages
                      ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                      : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
                  }`}
                >
                  Next
                </button>
              </div>
            )}
          </>
        )}

        {/* Empty State */}
        {!loading && !error && summaries.length === 0 && (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <span className="text-6xl mb-4 block">📭</span>
            <h3 className="text-2xl font-bold text-gray-900 mb-2">No summaries yet</h3>
            <p className="text-gray-600">
              Check back later for AI news summaries
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-12">
        <div className="max-w-5xl mx-auto px-4 py-8">
          <div className="text-center text-gray-600">
            <p className="mb-2">
              <strong>AI News Collector</strong> - Monitoring Twitter for AI news
            </p>
            <p className="text-sm">
              Powered by Claude API • Built with Next.js & FastAPI
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
