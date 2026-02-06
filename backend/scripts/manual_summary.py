"""
Example script to manually create a daily summary.
Useful for testing and debugging.
"""
import asyncio
import sys
from pathlib import Path
from datetime import date, timedelta

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import get_db_context
from app.services.aggregator import aggregator_service
from app.services.email_service import email_service
from loguru import logger


async def main():
    """Create daily summary manually."""
    logger.info("Starting manual daily summary creation")

    # Get date from command line or use yesterday
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
        summary_date = date.fromisoformat(date_str)
    else:
        summary_date = date.today() - timedelta(days=1)

    logger.info(f"Creating summary for {summary_date}")

    try:
        with get_db_context() as db:
            # Create summary
            logger.info("Creating daily summary")
            summary = await aggregator_service.create_daily_summary(db, summary_date)

            if not summary:
                logger.warning(f"No AI tweets found for {summary_date}")
                return

            logger.info(
                f"Created summary {summary.id}: "
                f"{summary.top_tweets_count} highlights, "
                f"{summary.other_tweets_count} other tweets"
            )

            # Get summary data for email
            summary_data = await aggregator_service.get_summary_with_tweets(db, summary.id)

            if summary_data:
                # Send email
                logger.info("Sending email digest")
                email_sent = await email_service.send_daily_digest(
                    summary=summary_data["summary"],
                    highlights=summary_data["highlights"]
                )

                if email_sent:
                    logger.info("Email sent successfully")
                else:
                    logger.warning("Email sending failed or disabled")

            logger.info("Manual summary creation complete!")

    except Exception as e:
        logger.error(f"Error during manual summary creation: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
