"""
Configuration management using pydantic-settings.
Loads and validates environment variables.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Application
    app_name: str = "ai-news-collector"
    app_env: str = "development"
    debug: bool = False
    secret_key: str = "change-me-in-production"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    frontend_url: str = "http://localhost:3000"

    # Database
    database_url: str = "postgresql://user:password@localhost:5432/ai_news"

    # Twitter API (twitterapi.io)
    twitter_api_key: str
    twitter_api_base_url: str = "https://api.twitterapi.io/v1"

    # Claude API
    anthropic_api_key: str
    claude_model: str = "claude-3-5-sonnet-20241022"
    claude_max_tokens: int = 4096

    # Screenshot Service
    playwright_headless: bool = True
    screenshot_width: int = 1200
    screenshot_height: int = 800

    # Storage (AWS S3)
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_s3_bucket: Optional[str] = None
    aws_region: str = "us-east-1"

    # Email Service
    resend_api_key: Optional[str] = None
    email_from: str = "noreply@yourdomain.com"
    email_to: str = "your-email@example.com"

    # Scheduled Tasks
    schedule_tweet_collection_cron: str = "0 */2 * * *"  # Every 2 hours
    schedule_daily_summary_cron: str = "0 8 * * *"       # Daily at 8 AM
    schedule_timezone: str = "UTC"

    # Logging
    log_level: str = "INFO"

    # Feature Flags
    enable_translation: bool = True
    enable_screenshot: bool = True
    enable_email: bool = True
    batch_size: int = 10

    # Ranking & Display Configuration
    top_tweets_count: int = 10  # Number of tweets to show in highlights section
    engagement_weight_likes: float = 1.0
    engagement_weight_retweets: float = 2.0
    engagement_weight_replies: float = 1.5
    engagement_weight_bookmarks: float = 2.5
    ai_relevance_weight: float = 3.0  # Weight for AI relevance in importance score

    # Security
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins if provided as comma-separated string."""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return [self.cors_origins]


# Global settings instance
settings = Settings()
