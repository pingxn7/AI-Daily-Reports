"""
API routes for summaries and tweets.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List, Optional
from datetime import datetime
import math

from app.database import get_db
from app.schemas import (
    DailySummaryListResponse,
    DailySummaryDetailResponse,
    ProcessedTweetResponse,
    PaginatedSummariesResponse,
    HealthCheckResponse
)
from app.models.daily_summary import DailySummary, SummaryTweet, DisplayType
from app.models.processed_tweet import ProcessedTweet
from app.tasks.scheduler import get_scheduler_status

router = APIRouter(prefix="/api", tags=["summaries"])


@router.get("/health", response_model=HealthCheckResponse)
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint.
    """
    # Check database connection
    try:
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    # Check scheduler status
    scheduler_info = get_scheduler_status()
    scheduler_status = "running" if scheduler_info["running"] else "stopped"

    return HealthCheckResponse(
        status="healthy" if db_status == "healthy" else "degraded",
        database=db_status,
        scheduler=scheduler_status,
        timestamp=datetime.utcnow()
    )


@router.get("/summaries", response_model=PaginatedSummariesResponse)
async def list_summaries(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """
    List all daily summaries with pagination.
    """
    # Get total count
    total = db.query(func.count(DailySummary.id)).scalar()

    # Calculate pagination
    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size

    # Get summaries
    summaries = db.query(DailySummary).order_by(
        desc(DailySummary.date)
    ).offset(offset).limit(page_size).all()

    # Convert to response models
    items = [
        DailySummaryListResponse(
            id=s.id,
            date=s.date,
            url_slug=s.url_slug,
            tweet_count=s.tweet_count,
            top_tweets_count=s.top_tweets_count,
            other_tweets_count=s.other_tweets_count,
            topics=s.topics,
            highlights_summary=s.highlights_summary,
            created_at=s.created_at,
            email_sent_at=s.email_sent_at
        )
        for s in summaries
    ]

    return PaginatedSummariesResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/summaries/{summary_id}", response_model=DailySummaryDetailResponse)
async def get_summary_detail(
    summary_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed summary with all tweets organized by display type.
    """
    # Get summary
    summary = db.query(DailySummary).filter(DailySummary.id == summary_id).first()

    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    # Get highlights (top 10 with full display)
    highlights_query = db.query(ProcessedTweet).join(SummaryTweet).filter(
        SummaryTweet.summary_id == summary_id,
        SummaryTweet.display_type == DisplayType.HIGHLIGHT
    ).order_by(SummaryTweet.rank_order)

    highlights = highlights_query.all()

    # Get other news (compact display)
    other_news_query = db.query(ProcessedTweet).join(SummaryTweet).filter(
        SummaryTweet.summary_id == summary_id,
        SummaryTweet.display_type == DisplayType.SUMMARY
    ).order_by(SummaryTweet.rank_order)

    other_news = other_news_query.all()

    # Build response
    return DailySummaryDetailResponse(
        id=summary.id,
        date=summary.date,
        url_slug=summary.url_slug,
        tweet_count=summary.tweet_count,
        top_tweets_count=summary.top_tweets_count,
        other_tweets_count=summary.other_tweets_count,
        topics=summary.topics,
        highlights_summary=summary.highlights_summary,
        summary_text=summary.summary_text,
        created_at=summary.created_at,
        email_sent_at=summary.email_sent_at,
        highlights=[ProcessedTweetResponse.model_validate(h) for h in highlights],
        other_news=[ProcessedTweetResponse.model_validate(n) for n in other_news]
    )


@router.get("/summaries/slug/{url_slug}", response_model=DailySummaryDetailResponse)
async def get_summary_by_slug(
    url_slug: str,
    db: Session = Depends(get_db)
):
    """
    Get summary by URL slug.
    """
    # Get summary
    summary = db.query(DailySummary).filter(DailySummary.url_slug == url_slug).first()

    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    # Reuse the detail endpoint logic
    return await get_summary_detail(summary.id, db)


@router.get("/tweets", response_model=List[ProcessedTweetResponse])
async def list_tweets(
    ai_related: Optional[bool] = Query(None, description="Filter by AI-related status"),
    limit: int = Query(50, ge=1, le=200, description="Number of tweets to return"),
    offset: int = Query(0, ge=0, description="Number of tweets to skip"),
    db: Session = Depends(get_db)
):
    """
    List processed tweets with optional filtering.
    """
    query = db.query(ProcessedTweet)

    # Apply filters
    if ai_related is not None:
        query = query.filter(ProcessedTweet.is_ai_related == ai_related)

    # Order by importance score
    query = query.order_by(desc(ProcessedTweet.importance_score))

    # Apply pagination
    tweets = query.offset(offset).limit(limit).all()

    return [ProcessedTweetResponse.model_validate(t) for t in tweets]


@router.get("/metrics")
async def get_metrics(db: Session = Depends(get_db)):
    """
    Get system metrics and statistics.
    """
    # Count summaries
    total_summaries = db.query(func.count(DailySummary.id)).scalar()

    # Count tweets
    total_tweets = db.query(func.count(ProcessedTweet.id)).scalar()
    ai_related_tweets = db.query(func.count(ProcessedTweet.id)).filter(
        ProcessedTweet.is_ai_related == True
    ).scalar()

    # Get latest summary
    latest_summary = db.query(DailySummary).order_by(
        desc(DailySummary.date)
    ).first()

    return {
        "total_summaries": total_summaries,
        "total_tweets": total_tweets,
        "ai_related_tweets": ai_related_tweets,
        "ai_related_percentage": round(ai_related_tweets / total_tweets * 100, 1) if total_tweets > 0 else 0,
        "latest_summary_date": latest_summary.date.isoformat() if latest_summary else None,
        "scheduler": get_scheduler_status()
    }
