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


@router.post("/create-test-data")
async def create_test_data(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Create test data for demonstration purposes.

    This will create sample tweets and process them.

    Returns:
        Status message
    """
    from app.models.tweet import Tweet
    from app.models.monitored_account import MonitoredAccount
    from datetime import datetime, timedelta
    import random

    try:
        # Sample tweets
        sample_tweets = [
            {"text": "Excited to announce GPT-5 will be released next month with groundbreaking multimodal capabilities!", "likes": 15000, "retweets": 3500, "replies": 890, "bookmarks": 2100},
            {"text": "Our new AI model achieves 95% accuracy on complex reasoning tasks. Paper coming soon!", "likes": 8900, "retweets": 2100, "replies": 450, "bookmarks": 1200},
            {"text": "Just published: 'Scaling Laws for Neural Language Models' - fascinating insights on model performance", "likes": 5600, "retweets": 1800, "replies": 320, "bookmarks": 980},
            {"text": "AI safety research is more important than ever. We need robust alignment techniques before AGI.", "likes": 12000, "retweets": 4200, "replies": 1100, "bookmarks": 3400},
            {"text": "New breakthrough in computer vision: our model can now understand 3D scenes from single images", "likes": 7800, "retweets": 2300, "replies": 560, "bookmarks": 1500},
            {"text": "Just tried the new Claude 3.5 Sonnet - the coding capabilities are incredible!", "likes": 9200, "retweets": 2800, "replies": 650, "bookmarks": 1900},
            {"text": "Machine learning is revolutionizing drug discovery. Excited about the future of AI in healthcare!", "likes": 11000, "retweets": 3100, "replies": 890, "bookmarks": 2500},
            {"text": "Open source AI models are democratizing access to powerful technology. This is huge!", "likes": 13000, "retweets": 4100, "replies": 1200, "bookmarks": 3100},
            {"text": "Neural networks can now generate photorealistic images from text descriptions. Mind-blowing!", "likes": 16000, "retweets": 4800, "replies": 1400, "bookmarks": 3800},
            {"text": "AI-powered code completion is changing how we write software. Productivity gains are real.", "likes": 9800, "retweets": 2900, "replies": 720, "bookmarks": 2000},
        ]

        # Get accounts
        accounts = db.query(MonitoredAccount).filter(MonitoredAccount.is_active == True).all()
        if not accounts:
            return {"status": "error", "message": "No monitored accounts found"}

        # Create tweets
        created_count = 0
        base_time = datetime.utcnow() - timedelta(hours=12)

        for i, tweet_data in enumerate(sample_tweets):
            account = random.choice(accounts)
            engagement_score = (
                tweet_data["likes"] * 1.0 +
                tweet_data["retweets"] * 2.0 +
                tweet_data["replies"] * 1.5 +
                tweet_data["bookmarks"] * 2.5
            )

            tweet = Tweet(
                tweet_id=f"test_{random.randint(100000, 999999)}",
                user_id=account.id,
                text=tweet_data["text"],
                created_at=base_time + timedelta(minutes=i*30),
                tweet_url=f"https://twitter.com/{account.username}/status/test_{i+1}",
                like_count=tweet_data["likes"],
                retweet_count=tweet_data["retweets"],
                reply_count=tweet_data["replies"],
                bookmark_count=tweet_data["bookmarks"],
                engagement_score=engagement_score,
                processed=False
            )
            db.add(tweet)
            created_count += 1

        db.commit()

        return {
            "status": "success",
            "message": f"Created {created_count} test tweets",
            "created": created_count
        }

    except Exception as e:
        db.rollback()
        return {
            "status": "error",
            "message": f"Error creating test data: {str(e)}"
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
