"""
Tweet model - Raw tweets collected from Twitter.
"""
from sqlalchemy import Column, String, Text, DateTime, Boolean, Integer, Float, BigInteger, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Tweet(Base):
    """Raw tweets collected from monitored accounts."""

    __tablename__ = "tweets"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tweet_id = Column(String(50), unique=True, nullable=False, index=True)  # Twitter tweet ID
    user_id = Column(BigInteger, ForeignKey("monitored_accounts.id"), nullable=False, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, index=True)  # Tweet creation time
    tweet_url = Column(String(500), nullable=False)
    metadata = Column(JSON, nullable=True)  # Additional tweet metadata

    # Engagement metrics
    like_count = Column(Integer, default=0, nullable=False)
    retweet_count = Column(Integer, default=0, nullable=False)
    reply_count = Column(Integer, default=0, nullable=False)
    bookmark_count = Column(Integer, default=0, nullable=False)
    engagement_score = Column(Float, default=0.0, nullable=False, index=True)  # Calculated engagement score

    # Collection metadata
    collected_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    processed = Column(Boolean, default=False, nullable=False, index=True)

    # Relationships
    account = relationship("MonitoredAccount", back_populates="tweets")
    processed_tweet = relationship("ProcessedTweet", back_populates="tweet", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Tweet(tweet_id='{self.tweet_id}', engagement_score={self.engagement_score})>"
