"""
Scheduled tasks using APScheduler.
"""
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, date, timedelta
from loguru import logger

from app.config import settings
from app.database import get_db_context
from app.services.twitter_collector import twitter_collector
from app.services.ai_analyzer import ai_analyzer
from app.services.aggregator import aggregator_service
from app.services.email_service_v2 import email_service


# Global scheduler instance
scheduler = AsyncIOScheduler(timezone=settings.schedule_timezone)


async def collect_tweets_task():
    """
    Scheduled task to collect tweets from monitored accounts.
    Runs every 2 hours by default.
    """
    logger.info("Starting scheduled tweet collection task")

    try:
        with get_db_context() as db:
            # Collect tweets
            stats = await twitter_collector.collect_all_tweets(db)
            logger.info(f"Tweet collection complete: {stats}")

            # Process collected tweets with AI
            if stats.get("total_tweets", 0) > 0:
                processed_count = await ai_analyzer.process_unprocessed_tweets(db)
                logger.info(f"Processed {processed_count} tweets with AI")

    except Exception as e:
        logger.error(f"Error in tweet collection task: {e}")


async def daily_summary_task():
    """
    Scheduled task to create daily summary and send email.
    Runs daily at 8 AM Beijing time by default.
    """
    logger.info("Starting scheduled daily summary task")

    try:
        with get_db_context() as db:
            # Create summary for yesterday
            yesterday = date.today() - timedelta(days=1)
            summary = await aggregator_service.create_daily_summary(db, yesterday)

            if not summary:
                logger.warning("No summary created (no AI tweets found)")
                return

            logger.info(f"Created daily summary {summary.id} for {yesterday}")

            # Get highlights for email
            summary_data = await aggregator_service.get_summary_with_tweets(db, summary.id)

            if summary_data:
                # Send email with new email service
                email_sent = await email_service.send_daily_digest(
                    summary=summary_data["summary"],
                    highlights=summary_data["highlights"]
                )

                if email_sent:
                    summary.email_sent_at = datetime.now()
                    summary.email_recipient = settings.email_to
                    db.commit()
                    logger.info(f"Daily digest email sent successfully to {settings.email_to}")

    except Exception as e:
        logger.error(f"Error in daily summary task: {e}")


def start_scheduler():
    """Initialize and start the scheduler with all tasks."""
    logger.info("Initializing scheduler")

    # Add tweet collection task (every 2 hours)
    scheduler.add_job(
        collect_tweets_task,
        trigger=CronTrigger.from_crontab(settings.schedule_tweet_collection_cron),
        id="collect_tweets",
        name="Collect tweets from monitored accounts",
        replace_existing=True
    )
    logger.info(f"Scheduled tweet collection: {settings.schedule_tweet_collection_cron}")

    # Add daily summary task (daily at 8 AM)
    scheduler.add_job(
        daily_summary_task,
        trigger=CronTrigger.from_crontab(settings.schedule_daily_summary_cron),
        id="daily_summary",
        name="Create daily summary and send email",
        replace_existing=True
    )
    logger.info(f"Scheduled daily summary: {settings.schedule_daily_summary_cron}")

    # Start scheduler
    scheduler.start()
    logger.info("Scheduler started successfully")


def stop_scheduler():
    """Stop the scheduler."""
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler stopped")


def get_scheduler_status() -> dict:
    """
    Get scheduler status and job information.

    Returns:
        Dictionary with scheduler status
    """
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run": job.next_run_time.isoformat() if job.next_run_time else None,
            "trigger": str(job.trigger)
        })

    return {
        "running": scheduler.running,
        "jobs": jobs
    }
