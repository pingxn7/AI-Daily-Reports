"""
Tests for Twitter collector service.
"""
import pytest
from app.services.twitter_collector import TwitterCollector


def test_calculate_engagement_score():
    """Test engagement score calculation."""
    collector = TwitterCollector()

    tweet_data = {
        'like_count': 100,
        'retweet_count': 50,
        'reply_count': 25,
        'bookmark_count': 10
    }

    score = collector.calculate_engagement_score(tweet_data)

    # Expected: 100*1.0 + 50*2.0 + 25*1.5 + 10*2.5 = 262.5
    assert score == 262.5
    assert isinstance(score, float)


def test_calculate_engagement_score_zero():
    """Test engagement score with zero metrics."""
    collector = TwitterCollector()

    tweet_data = {
        'like_count': 0,
        'retweet_count': 0,
        'reply_count': 0,
        'bookmark_count': 0
    }

    score = collector.calculate_engagement_score(tweet_data)
    assert score == 0.0


def test_calculate_engagement_score_missing_fields():
    """Test engagement score with missing fields."""
    collector = TwitterCollector()

    tweet_data = {
        'like_count': 100
        # Missing other fields
    }

    score = collector.calculate_engagement_score(tweet_data)
    assert score == 100.0  # Only likes counted


def test_parse_tweet(sample_monitored_account):
    """Test tweet parsing."""
    collector = TwitterCollector()

    tweet_data = {
        "id": "1234567890",
        "text": "Test tweet about AI",
        "created_at": "2024-02-06T10:30:00Z",
        "public_metrics": {
            "like_count": 100,
            "retweet_count": 50,
            "reply_count": 25,
            "bookmark_count": 10
        }
    }

    parsed = collector.parse_tweet(tweet_data, sample_monitored_account.id)

    assert parsed['tweet_id'] == "1234567890"
    assert parsed['text'] == "Test tweet about AI"
    assert parsed['like_count'] == 100
    assert parsed['retweet_count'] == 50
    assert parsed['reply_count'] == 25
    assert parsed['bookmark_count'] == 10
    assert parsed['engagement_score'] == 262.5
    assert parsed['user_id'] == sample_monitored_account.id
    assert parsed['processed'] is False
