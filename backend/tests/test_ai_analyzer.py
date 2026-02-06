"""
Tests for AI analyzer service.
"""
import pytest
from app.services.ai_analyzer import AIAnalyzer


def test_calculate_importance_score():
    """Test importance score calculation."""
    analyzer = AIAnalyzer()

    # Test with normalized values
    engagement_score = 500.0
    ai_relevance_score = 8.0
    max_engagement = 1000.0

    importance = analyzer.calculate_importance_score(
        engagement_score,
        ai_relevance_score,
        max_engagement
    )

    # Expected: (500/1000)*10 * 0.7 + 8 * 0.3 = 5*0.7 + 8*0.3 = 3.5 + 2.4 = 5.9
    assert importance == 5.9
    assert 0 <= importance <= 10


def test_calculate_importance_score_max_engagement():
    """Test importance score with max engagement."""
    analyzer = AIAnalyzer()

    importance = analyzer.calculate_importance_score(
        engagement_score=1000.0,
        ai_relevance_score=10.0,
        max_engagement=1000.0
    )

    # Expected: 10*0.7 + 10*0.3 = 7 + 3 = 10
    assert importance == 10.0


def test_calculate_importance_score_zero_engagement():
    """Test importance score with zero engagement."""
    analyzer = AIAnalyzer()

    importance = analyzer.calculate_importance_score(
        engagement_score=0.0,
        ai_relevance_score=8.0,
        max_engagement=1000.0
    )

    # Expected: 0*0.7 + 8*0.3 = 2.4
    assert importance == 2.4


def test_calculate_importance_score_zero_max():
    """Test importance score with zero max engagement."""
    analyzer = AIAnalyzer()

    importance = analyzer.calculate_importance_score(
        engagement_score=100.0,
        ai_relevance_score=5.0,
        max_engagement=0.0
    )

    # When max is 0, normalized engagement should be 0
    # Expected: 0*0.7 + 5*0.3 = 1.5
    assert importance == 1.5
