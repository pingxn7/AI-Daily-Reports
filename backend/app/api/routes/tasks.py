"""
API routes for manually triggering tasks.
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import date, timedelta

from app.database import get_db

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("/collect")
async def trigger_collection(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Manually trigger tweet collection and processing.

    This will:
    1. Collect tweets from all monitored accounts
    2. Process tweets with AI analysis

    Returns:
        Status message
    """
    from app.services.twitter_collector import twitter_collector
    from app.services.ai_analyzer import ai_analyzer

    try:
        # Step 1: Collect tweets
        stats = await twitter_collector.collect_all_tweets(db)

        if stats.get("total_tweets", 0) == 0:
            return {
                "status": "success",
                "message": "No new tweets collected",
                "stats": stats
            }

        # Step 2: Process tweets with AI
        processed_count = await ai_analyzer.process_unprocessed_tweets(db)

        return {
            "status": "success",
            "message": f"Collected {stats['total_tweets']} tweets, processed {processed_count}",
            "stats": {
                "collected": stats,
                "processed": processed_count
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during collection: {str(e)}"
        }


@router.post("/summary")
async def trigger_summary(
    summary_date: str = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Manually trigger daily summary creation.

    Args:
        summary_date: Date in YYYY-MM-DD format (defaults to yesterday)

    Returns:
        Summary information
    """
    from app.services.aggregator import aggregator_service
    from app.services.email_service import email_service

    try:
        # Parse date
        if summary_date:
            target_date = date.fromisoformat(summary_date)
        else:
            target_date = date.today() - timedelta(days=1)

        # Create summary
        summary = await aggregator_service.create_daily_summary(db, target_date)

        if not summary:
            return {
                "status": "success",
                "message": f"No AI tweets found for {target_date}",
                "summary": None
            }

        # Get summary data
        summary_data = await aggregator_service.get_summary_with_tweets(db, summary.id)

        # Try to send email (if configured)
        email_sent = False
        if summary_data:
            email_sent = await email_service.send_daily_digest(
                summary=summary_data["summary"],
                highlights=summary_data["highlights"]
            )

        return {
            "status": "success",
            "message": f"Created summary for {target_date}",
            "summary": {
                "id": summary.id,
                "date": str(summary.date),
                "tweet_count": summary.tweet_count,
                "top_tweets_count": summary.top_tweets_count,
                "url_slug": summary.url_slug,
                "email_sent": email_sent
            }
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error creating summary: {str(e)}"
        }


@router.post("/full-run")
async def trigger_full_run(
    summary_date: str = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Run the complete workflow: collect tweets, process them, and create summary.

    Args:
        summary_date: Date in YYYY-MM-DD format (defaults to yesterday)

    Returns:
        Complete workflow results
    """
    from app.services.twitter_collector import twitter_collector
    from app.services.ai_analyzer import ai_analyzer
    from app.services.aggregator import aggregator_service
    from app.services.email_service import email_service

    try:
        results = {}

        # Step 1: Collect tweets
        stats = await twitter_collector.collect_all_tweets(db)
        results["collection"] = stats

        if stats.get("total_tweets", 0) == 0:
            return {
                "status": "success",
                "message": "No new tweets collected",
                "results": results
            }

        # Step 2: Process tweets
        processed_count = await ai_analyzer.process_unprocessed_tweets(db)
        results["processed"] = processed_count

        # Step 3: Create summary
        if summary_date:
            target_date = date.fromisoformat(summary_date)
        else:
            target_date = date.today() - timedelta(days=1)

        summary = await aggregator_service.create_daily_summary(db, target_date)

        if summary:
            summary_data = await aggregator_service.get_summary_with_tweets(db, summary.id)

            # Try to send email
            email_sent = False
            if summary_data:
                email_sent = await email_service.send_daily_digest(
                    summary=summary_data["summary"],
                    highlights=summary_data["highlights"]
                )

            results["summary"] = {
                "id": summary.id,
                "date": str(summary.date),
                "tweet_count": summary.tweet_count,
                "top_tweets_count": summary.top_tweets_count,
                "url_slug": summary.url_slug,
                "email_sent": email_sent
            }
        else:
            results["summary"] = None

        return {
            "status": "success",
            "message": "Full workflow completed",
            "results": results
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during full run: {str(e)}",
            "results": results if 'results' in locals() else {}
        }
