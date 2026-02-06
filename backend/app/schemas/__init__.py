"""
Pydantic schemas for API request/response validation.
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional, List


# MonitoredAccount schemas
class MonitoredAccountBase(BaseModel):
    user_id: str
    username: str
    display_name: Optional[str] = None
    is_active: bool = True


class MonitoredAccountCreate(MonitoredAccountBase):
    pass


class MonitoredAccountResponse(MonitoredAccountBase):
    id: int
    last_tweet_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Tweet schemas
class TweetBase(BaseModel):
    tweet_id: str
    text: str
    created_at: datetime
    tweet_url: str
    like_count: int = 0
    retweet_count: int = 0
    reply_count: int = 0
    bookmark_count: int = 0
    engagement_score: float = 0.0


class TweetCreate(TweetBase):
    user_id: int
    metadata: Optional[dict] = None


class TweetResponse(TweetBase):
    id: int
    user_id: int
    collected_at: datetime
    processed: bool

    model_config = ConfigDict(from_attributes=True)


# ProcessedTweet schemas
class ProcessedTweetBase(BaseModel):
    is_ai_related: bool
    summary: Optional[str] = None
    translation: Optional[str] = None
    topics: Optional[List[str]] = None
    importance_score: float = 0.0


class ProcessedTweetCreate(ProcessedTweetBase):
    tweet_id: int


class ProcessedTweetResponse(ProcessedTweetBase):
    id: int
    tweet_id: int
    screenshot_url: Optional[str] = None
    screenshot_generated_at: Optional[datetime] = None
    processed_at: datetime
    tweet: TweetResponse

    model_config = ConfigDict(from_attributes=True)


# DailySummary schemas
class DailySummaryBase(BaseModel):
    date: datetime
    url_slug: str
    tweet_count: int = 0
    top_tweets_count: int = 0
    other_tweets_count: int = 0
    topics: Optional[List[str]] = None
    highlights_summary: Optional[str] = None
    summary_text: Optional[str] = None


class DailySummaryCreate(DailySummaryBase):
    pass


class DailySummaryListResponse(BaseModel):
    """Response for summary list endpoint."""
    id: int
    date: datetime
    url_slug: str
    tweet_count: int
    top_tweets_count: int
    other_tweets_count: int
    topics: Optional[List[str]] = None
    highlights_summary: Optional[str] = None
    created_at: datetime
    email_sent_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class DailySummaryDetailResponse(DailySummaryBase):
    """Response for summary detail endpoint with tweets."""
    id: int
    created_at: datetime
    email_sent_at: Optional[datetime] = None
    highlights: List[ProcessedTweetResponse] = []
    other_news: List[ProcessedTweetResponse] = []

    model_config = ConfigDict(from_attributes=True)


# Pagination
class PaginatedResponse(BaseModel):
    """Generic paginated response."""
    items: List[BaseModel]
    total: int
    page: int
    page_size: int
    total_pages: int


class PaginatedSummariesResponse(BaseModel):
    """Paginated summaries response."""
    items: List[DailySummaryListResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


# Health check
class HealthCheckResponse(BaseModel):
    status: str
    database: str
    scheduler: str
    timestamp: datetime
