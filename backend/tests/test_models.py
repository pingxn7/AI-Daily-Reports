"""
Tests for database models.
"""
import pytest
from datetime import datetime
from app.models.monitored_account import MonitoredAccount
from app.models.tweet import Tweet
from app.models.processed_tweet import ProcessedTweet
from app.models.daily_summary import DailySummary, SummaryTweet, DisplayType


def test_create_monitored_account(test_db):
    """Test creating a monitored account."""
    account = MonitoredAccount(
        user_id="123456",
        username="testuser",
        display_name="Test User",
        is_active=True
    )
    test_db.add(account)
    test_db.commit()
    test_db.refresh(account)

    assert account.id is not None
    assert account.username == "testuser"
    assert account.is_active is True
    assert account.created_at is not None


def test_create_tweet(test_db, sample_monitored_account):
    """Test creating a tweet."""
    tweet = Tweet(
        tweet_id="1234567890",
        user_id=sample_monitored_account.id,
        text="Test tweet about AI",
        created_at=datetime.utcnow(),
        tweet_url="https://twitter.com/test/status/1234567890",
        like_count=100,
        retweet_count=50,
        reply_count=25,
        bookmark_count=10,
        engagement_score=262.5,
        processed=False
    )
    test_db.add(tweet)
    test_db.commit()
    test_db.refresh(tweet)

    assert tweet.id is not None
    assert tweet.tweet_id == "1234567890"
    assert tweet.engagement_score == 262.5
    assert tweet.processed is False


def test_create_processed_tweet(test_db, sample_monitored_account):
    """Test creating a processed tweet."""
    # Create tweet first
    tweet = Tweet(
        tweet_id="1234567890",
        user_id=sample_monitored_account.id,
        text="Test tweet about AI",
        created_at=datetime.utcnow(),
        tweet_url="https://twitter.com/test/status/1234567890",
        like_count=100,
        retweet_count=50,
        reply_count=25,
        bookmark_count=10,
        engagement_score=262.5,
        processed=True
    )
    test_db.add(tweet)
    test_db.commit()
    test_db.refresh(tweet)

    # Create processed tweet
    processed = ProcessedTweet(
        tweet_id=tweet.id,
        is_ai_related=True,
        summary="AI-related tweet about GPT",
        translation="关于GPT的AI相关推文",
        topics=["AI", "GPT"],
        importance_score=8.5,
        processed_at=datetime.utcnow()
    )
    test_db.add(processed)
    test_db.commit()
    test_db.refresh(processed)

    assert processed.id is not None
    assert processed.is_ai_related is True
    assert processed.importance_score == 8.5
    assert len(processed.topics) == 2


def test_create_daily_summary(test_db):
    """Test creating a daily summary."""
    summary = DailySummary(
        date=datetime.utcnow(),
        url_slug="2024-02-06-ai-news",
        tweet_count=50,
        top_tweets_count=10,
        other_tweets_count=40,
        topics=["AI", "GPT", "LLM"],
        highlights_summary="Today's key AI developments...",
        summary_text="Daily summary for 2024-02-06"
    )
    test_db.add(summary)
    test_db.commit()
    test_db.refresh(summary)

    assert summary.id is not None
    assert summary.tweet_count == 50
    assert summary.top_tweets_count == 10
    assert len(summary.topics) == 3


def test_tweet_account_relationship(test_db, sample_monitored_account):
    """Test relationship between tweet and account."""
    tweet = Tweet(
        tweet_id="1234567890",
        user_id=sample_monitored_account.id,
        text="Test tweet",
        created_at=datetime.utcnow(),
        tweet_url="https://twitter.com/test/status/1234567890",
        like_count=100,
        retweet_count=50,
        reply_count=25,
        bookmark_count=10,
        engagement_score=262.5,
        processed=False
    )
    test_db.add(tweet)
    test_db.commit()
    test_db.refresh(tweet)

    # Test relationship
    assert tweet.account.username == sample_monitored_account.username
    assert len(sample_monitored_account.tweets) == 1
    assert sample_monitored_account.tweets[0].tweet_id == "1234567890"


def test_summary_tweet_junction(test_db, sample_monitored_account):
    """Test junction table between summary and tweets."""
    # Create tweet and processed tweet
    tweet = Tweet(
        tweet_id="1234567890",
        user_id=sample_monitored_account.id,
        text="Test tweet",
        created_at=datetime.utcnow(),
        tweet_url="https://twitter.com/test/status/1234567890",
        like_count=100,
        retweet_count=50,
        reply_count=25,
        bookmark_count=10,
        engagement_score=262.5,
        processed=True
    )
    test_db.add(tweet)
    test_db.commit()
    test_db.refresh(tweet)

    processed = ProcessedTweet(
        tweet_id=tweet.id,
        is_ai_related=True,
        summary="Test summary",
        importance_score=8.5,
        processed_at=datetime.utcnow()
    )
    test_db.add(processed)
    test_db.commit()
    test_db.refresh(processed)

    # Create summary
    summary = DailySummary(
        date=datetime.utcnow(),
        url_slug="2024-02-06-ai-news",
        tweet_count=1,
        top_tweets_count=1,
        other_tweets_count=0,
        topics=["AI"]
    )
    test_db.add(summary)
    test_db.commit()
    test_db.refresh(summary)

    # Create junction
    link = SummaryTweet(
        summary_id=summary.id,
        processed_tweet_id=processed.id,
        display_type=DisplayType.HIGHLIGHT,
        rank_order=0
    )
    test_db.add(link)
    test_db.commit()
    test_db.refresh(link)

    assert link.id is not None
    assert link.display_type == DisplayType.HIGHLIGHT
    assert link.rank_order == 0
