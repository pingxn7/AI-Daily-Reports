"""
Test configuration and fixtures for pytest.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.config import settings


@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine."""
    # Use in-memory SQLite for tests
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_db(test_engine):
    """Create test database session."""
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def sample_tweet_data():
    """Sample tweet data for testing."""
    return {
        "id": "1234567890",
        "text": "Exciting news about GPT-5 and its capabilities in reasoning!",
        "created_at": "2024-02-06T10:30:00Z",
        "public_metrics": {
            "like_count": 1000,
            "retweet_count": 250,
            "reply_count": 50,
            "bookmark_count": 100
        }
    }


@pytest.fixture
def sample_monitored_account(test_db):
    """Create sample monitored account."""
    from app.models.monitored_account import MonitoredAccount

    account = MonitoredAccount(
        user_id="123456",
        username="testuser",
        display_name="Test User",
        is_active=True
    )
    test_db.add(account)
    test_db.commit()
    test_db.refresh(account)
    return account
