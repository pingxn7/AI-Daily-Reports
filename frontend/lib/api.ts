/**
 * Frontend API client for communicating with the backend.
 */
import axios, { AxiosInstance } from 'axios';

// Types
export interface MonitoredAccount {
  id: number;
  user_id: string;
  username: string;
  display_name: string | null;
  is_active: boolean;
  last_tweet_id: string | null;
  created_at: string;
  updated_at: string;
}

export interface Tweet {
  id: number;
  tweet_id: string;
  text: string;
  created_at: string;
  tweet_url: string;
  like_count: number;
  retweet_count: number;
  reply_count: number;
  bookmark_count: number;
  engagement_score: number;
  user_id: number;
  collected_at: string;
  processed: boolean;
  account: MonitoredAccount;
}

export interface ProcessedTweet {
  id: number;
  tweet_id: number;
  is_ai_related: boolean;
  summary: string | null;
  translation: string | null;
  topics: string[] | null;
  screenshot_url: string | null;
  screenshot_generated_at: string | null;
  importance_score: number;
  processed_at: string;
  tweet: Tweet;
}

export interface DailySummaryList {
  id: number;
  date: string;
  url_slug: string;
  tweet_count: number;
  top_tweets_count: number;
  other_tweets_count: number;
  topics: string[] | null;
  highlights_summary: string | null;
  created_at: string;
  email_sent_at: string | null;
}

export interface DailySummaryDetail extends DailySummaryList {
  summary_text: string | null;
  highlights: ProcessedTweet[];
  other_news: ProcessedTweet[];
}

export interface PaginatedSummaries {
  items: DailySummaryList[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface HealthCheck {
  status: string;
  database: string;
  scheduler: string;
  timestamp: string;
}

export interface Metrics {
  total_summaries: number;
  total_tweets: number;
  ai_related_tweets: number;
  ai_related_percentage: number;
  latest_summary_date: string | null;
  scheduler: {
    running: boolean;
    jobs: Array<{
      id: string;
      name: string;
      next_run: string | null;
      trigger: string;
    }>;
  };
}

// API Client Class
class APIClient {
  private client: AxiosInstance;

  constructor() {
    const baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    const timeout = parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || '10000', 10);

    this.client = axios.create({
      baseURL,
      timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response) {
          // Server responded with error status
          console.error('API Error:', error.response.status, error.response.data);
        } else if (error.request) {
          // Request made but no response
          console.error('Network Error:', error.message);
        } else {
          // Something else happened
          console.error('Error:', error.message);
        }
        return Promise.reject(error);
      }
    );
  }

  // Health check
  async healthCheck(): Promise<HealthCheck> {
    const response = await this.client.get<HealthCheck>('/api/health');
    return response.data;
  }

  // Get metrics
  async getMetrics(): Promise<Metrics> {
    const response = await this.client.get<Metrics>('/api/metrics');
    return response.data;
  }

  // List summaries with pagination
  async listSummaries(page: number = 1, pageSize: number = 10): Promise<PaginatedSummaries> {
    const response = await this.client.get<PaginatedSummaries>('/api/summaries', {
      params: { page, page_size: pageSize },
    });
    return response.data;
  }

  // Get summary detail by ID
  async getSummaryById(id: number): Promise<DailySummaryDetail> {
    const response = await this.client.get<DailySummaryDetail>(`/api/summaries/${id}`);
    return response.data;
  }

  // Get summary detail by slug
  async getSummaryBySlug(slug: string): Promise<DailySummaryDetail> {
    const response = await this.client.get<DailySummaryDetail>(`/api/summaries/slug/${slug}`);
    return response.data;
  }

  // List tweets
  async listTweets(
    aiRelated?: boolean,
    limit: number = 50,
    offset: number = 0
  ): Promise<ProcessedTweet[]> {
    const response = await this.client.get<ProcessedTweet[]>('/api/tweets', {
      params: {
        ai_related: aiRelated,
        limit,
        offset,
      },
    });
    return response.data;
  }
}

// Export singleton instance
export const apiClient = new APIClient();

// Utility functions
export function formatNumber(num: number): string {
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1)}M`;
  }
  if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}K`;
  }
  return num.toString();
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;

  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined,
  });
}

export function formatFullDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}
