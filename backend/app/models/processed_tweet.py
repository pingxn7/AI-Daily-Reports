"""
ProcessedTweet model - AI-analyzed tweets with summaries and importance scores.
"""
from sqlalchemy import Column, String, Text, DateTime, Boolean, Float, BigInteger, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class ProcessedTweet(Base):
    """Tweets that have been analyzed by AI for relevance and importance."""

    __tablename__ = "processed_tweets"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tweet_id = Column(BigInteger, ForeignKey("tweets.id"), unique=True, nullable=False, index=True)

    # AI Analysis results
    is_ai_related = Column(Boolean, nullable=False, index=True)
    summary = Column(Text, nullable=True)  # AI-generated summary
    translation = Column(Text, nullable=True)  # Chinese translation (only for top 10)
    topics = Column(JSON, nullable=True)  # Array of topics/tags

    # Screenshot
    screenshot_url = Column(String(500), nullable=True)
    screenshot_generated_at = Column(DateTime, nullable=True)

    # Importance scoring
    importance_score = Column(Float, default=0.0, nullable=False, index=True)  # Combined engagement + AI relevance

    # Processing metadata
    processed_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    tweet = relationship("Tweet", back_populates="processed_tweet")
    summary_links = relationship("SummaryTweet", back_populates="processed_tweet", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ProcessedTweet(tweet_id={self.tweet_id}, is_ai_related={self.is_ai_related}, importance_score={self.importance_score})>"
