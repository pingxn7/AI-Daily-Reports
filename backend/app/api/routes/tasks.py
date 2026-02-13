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


@router.get("/debug/test-claude")
async def test_claude_api() -> Dict[str, Any]:
    """
    Test if Claude API is working.
    """
    import anthropic
    from app.config import settings

    api_key_info = {
        "configured": bool(settings.anthropic_api_key),
        "length": len(settings.anthropic_api_key) if settings.anthropic_api_key else 0,
        "prefix": settings.anthropic_api_key[:15] + "..." if settings.anthropic_api_key and len(settings.anthropic_api_key) > 15 else None,
        "starts_with_sk": settings.anthropic_api_key.startswith("sk-") if settings.anthropic_api_key else False,
        "base_url": settings.anthropic_base_url if hasattr(settings, 'anthropic_base_url') else None
    }

    try:
        # Create client with optional base_url
        client_kwargs = {"api_key": settings.anthropic_api_key}
        if hasattr(settings, 'anthropic_base_url') and settings.anthropic_base_url:
            client_kwargs["base_url"] = settings.anthropic_base_url

        client = anthropic.Anthropic(**client_kwargs)

        message = client.messages.create(
            model=settings.claude_model,
            max_tokens=100,
            messages=[{"role": "user", "content": "Say hello"}]
        )

        return {
            "status": "success",
            "api_key_info": api_key_info,
            "model": settings.claude_model,
            "response": message.content[0].text
        }
    except Exception as e:
        import traceback
        return {
            "status": "error",
            "api_key_info": api_key_info,
            "message": str(e),
            "traceback": traceback.format_exc()
        }


@router.get("/debug/tweets")
async def debug_tweets(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Debug endpoint to check raw tweets in database.
    """
    from app.models.tweet import Tweet as TweetModel

    total_tweets = db.query(TweetModel).count()
    unprocessed_tweets = db.query(TweetModel).filter(TweetModel.processed == False).count()
    processed_tweets = db.query(TweetModel).filter(TweetModel.processed == True).count()

    # Get sample tweets
    sample = db.query(TweetModel).limit(3).all()
    sample_data = [
        {
            "id": t.id,
            "tweet_id": t.tweet_id,
            "text": t.text[:50] + "...",
            "processed": t.processed
        }
        for t in sample
    ]

    return {
        "total_tweets": total_tweets,
        "unprocessed": unprocessed_tweets,
        "processed": processed_tweets,
        "sample": sample_data
    }


@router.post("/process-tweets")
async def process_existing_tweets(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Process existing unprocessed tweets with AI analysis.

    Returns:
        Processing results
    """
    from app.services.ai_analyzer import ai_analyzer
    from app.models.tweet import Tweet as TweetModel

    try:
        # Check how many unprocessed tweets exist
        unprocessed_count = db.query(TweetModel).filter(TweetModel.processed == False).count()

        processed_count = await ai_analyzer.process_unprocessed_tweets(db)

        return {
            "status": "success",
            "message": f"Processed {processed_count} tweets",
            "processed": processed_count,
            "unprocessed_before": unprocessed_count
        }

    except Exception as e:
        import traceback
        return {
            "status": "error",
            "message": f"Error processing tweets: {str(e)}",
            "traceback": traceback.format_exc()
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

        # Use timestamp to ensure unique tweet IDs
        timestamp = int(datetime.utcnow().timestamp())

        for i, tweet_data in enumerate(sample_tweets):
            account = random.choice(accounts)
            engagement_score = (
                tweet_data["likes"] * 1.0 +
                tweet_data["retweets"] * 2.0 +
                tweet_data["replies"] * 1.5 +
                tweet_data["bookmarks"] * 2.5
            )

            tweet = Tweet(
                tweet_id=f"test_{timestamp}_{i}_{random.randint(1000, 9999)}",
                user_id=account.id,
                text=tweet_data["text"],
                created_at=base_time + timedelta(minutes=i*30),
                tweet_url=f"https://twitter.com/{account.username}/status/test_{timestamp}_{i}",
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

        # Verify tweets were created in a new session
        db.close()
        from app.database import SessionLocal
        verify_db = SessionLocal()
        try:
            from app.models.tweet import Tweet as TweetModel
            actual_count = verify_db.query(TweetModel).filter(TweetModel.processed == False).count()
        finally:
            verify_db.close()

        return {
            "status": "success",
            "message": f"Created {created_count} test tweets",
            "created": created_count,
            "verified_count": actual_count
        }

    except Exception as e:
        db.rollback()
        import traceback
        return {
            "status": "error",
            "message": f"Error creating test data: {str(e)}",
            "traceback": traceback.format_exc()
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


@router.post("/send-email")
async def send_summary_email(
    summary_id: int = None,
    summary_date: str = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Send email for an existing summary.

    Args:
        summary_id: Summary ID (optional)
        summary_date: Date in YYYY-MM-DD format (optional, defaults to latest)

    Returns:
        Email sending status
    """
    from app.models.daily_summary import DailySummary
    from app.services.email_service_v2 import email_service
    from app.services.aggregator import aggregator_service
    from sqlalchemy import desc

    try:
        # Find summary
        if summary_id:
            summary = db.query(DailySummary).filter(DailySummary.id == summary_id).first()
        elif summary_date:
            target_date = date.fromisoformat(summary_date)
            summary = db.query(DailySummary).filter(DailySummary.date == target_date).first()
        else:
            # Get latest summary
            summary = db.query(DailySummary).order_by(desc(DailySummary.date)).first()

        if not summary:
            return {
                "status": "error",
                "message": "Summary not found"
            }

        # Get summary with tweets
        summary_data = await aggregator_service.get_summary_with_tweets(db, summary.id)

        if not summary_data:
            return {
                "status": "error",
                "message": "Failed to load summary data"
            }

        # Send email
        email_sent = await email_service.send_daily_digest(
            summary=summary_data["summary"],
            highlights=summary_data["highlights"]
        )

        if email_sent:
            # Update email sent timestamp
            from datetime import datetime
            from app.config import settings
            summary.email_sent_at = datetime.now()
            summary.email_recipient = settings.email_to
            db.commit()

            return {
                "status": "success",
                "message": f"Email sent successfully for {summary.date}",
                "summary": {
                    "id": summary.id,
                    "date": str(summary.date),
                    "email_recipient": summary.email_recipient,
                    "email_sent_at": str(summary.email_sent_at)
                }
            }
        else:
            return {
                "status": "error",
                "message": "Failed to send email"
            }

    except Exception as e:
        import traceback
        return {
            "status": "error",
            "message": f"Error sending email: {str(e)}",
            "traceback": traceback.format_exc()
        }
