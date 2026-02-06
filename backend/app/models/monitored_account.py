"""
MonitoredAccount model - Twitter accounts to monitor for AI news.
"""
from sqlalchemy import Column, String, Boolean, DateTime, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class MonitoredAccount(Base):
    """Twitter accounts being monitored for AI-related content."""

    __tablename__ = "monitored_accounts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(50), unique=True, nullable=False, index=True)  # Twitter user ID
    username = Column(String(100), nullable=False, index=True)  # Twitter handle
    display_name = Column(String(200), nullable=True)  # Display name
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    last_tweet_id = Column(String(50), nullable=True)  # Last collected tweet ID
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    tweets = relationship("Tweet", back_populates="account", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MonitoredAccount(username='{self.username}', is_active={self.is_active})>"
