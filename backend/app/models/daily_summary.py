"""
DailySummary and SummaryTweet models - Daily aggregations of AI news.
"""
from sqlalchemy import Column, String, Text, DateTime, Integer, BigInteger, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.database import Base


class DisplayType(str, enum.Enum):
    """How to display a tweet in the summary."""
    HIGHLIGHT = "highlight"  # Full display with screenshot (top 10)
    SUMMARY = "summary"      # Compact display (remaining tweets)


class DailySummary(Base):
    """Daily aggregation of AI-related tweets."""

    __tablename__ = "daily_summaries"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    date = Column(DateTime, unique=True, nullable=False, index=True)  # Summary date
    url_slug = Column(String(100), unique=True, nullable=False, index=True)  # URL-friendly slug

    # Tweet counts
    tweet_count = Column(Integer, default=0, nullable=False)  # Total AI-related tweets
    top_tweets_count = Column(Integer, default=0, nullable=False)  # Number in highlights
    other_tweets_count = Column(Integer, default=0, nullable=False)  # Number in summary section

    # Content
    topics = Column(JSON, nullable=True)  # Array of topics covered
    highlights_summary = Column(Text, nullable=True)  # AI-generated summary of key highlights
    summary_text = Column(Text, nullable=True)  # Overall summary text

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    email_sent_at = Column(DateTime, nullable=True)
    email_recipient = Column(String(200), nullable=True)

    # Relationships
    tweet_links = relationship("SummaryTweet", back_populates="summary", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<DailySummary(date='{self.date}', tweet_count={self.tweet_count}, top_tweets_count={self.top_tweets_count})>"


class SummaryTweet(Base):
    """Junction table linking summaries to processed tweets with display metadata."""

    __tablename__ = "summary_tweets"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    summary_id = Column(BigInteger, ForeignKey("daily_summaries.id"), nullable=False, index=True)
    processed_tweet_id = Column(BigInteger, ForeignKey("processed_tweets.id"), nullable=False, index=True)

    # Display configuration
    display_type = Column(Enum(DisplayType), nullable=False, index=True)  # 'highlight' or 'summary'
    rank_order = Column(Integer, nullable=False)  # Display order within the summary

    # Relationships
    summary = relationship("DailySummary", back_populates="tweet_links")
    processed_tweet = relationship("ProcessedTweet", back_populates="summary_links")

    def __repr__(self):
        return f"<SummaryTweet(summary_id={self.summary_id}, display_type={self.display_type}, rank_order={self.rank_order})>"
