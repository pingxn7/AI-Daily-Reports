"""
Example script to manually trigger tweet collection and processing.
Useful for testing and debugging.
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import get_db_context
from app.services.twitter_collector import twitter_collector
from app.services.ai_analyzer import ai_analyzer
from loguru import logger


async def main():
    """Collect and process tweets manually."""
    logger.info("Starting manual tweet collection and processing")

    try:
        with get_db_context() as db:
            # Step 1: Collect tweets
            logger.info("Step 1: Collecting tweets from monitored accounts")
            stats = await twitter_collector.collect_all_tweets(db)
            logger.info(f"Collection stats: {stats}")

            if stats.get("total_tweets", 0) == 0:
                logger.warning("No new tweets collected")
                return

            # Step 2: Process tweets with AI
            logger.info("Step 2: Processing tweets with AI")
            processed_count = await ai_analyzer.process_unprocessed_tweets(db)
            logger.info(f"Processed {processed_count} tweets")

            if processed_count == 0:
                logger.warning("No tweets were processed")
                return

            logger.info("Manual collection and processing complete!")
            logger.info(f"Summary: Collected {stats['total_tweets']} tweets, processed {processed_count}")

    except Exception as e:
        logger.error(f"Error during manual collection: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
