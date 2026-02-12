"""
Screenshot service - Generate screenshots of tweets using Playwright.
Only generates screenshots for top 10 curated tweets to save costs.
"""
from typing import Optional
from datetime import datetime
import hashlib
from loguru import logger
from io import BytesIO

from app.config import settings

# Try to import playwright, but gracefully degrade if not available
try:
    from playwright.async_api import async_playwright, Browser, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    logger.warning("Playwright not installed - screenshot functionality will be disabled")
    PLAYWRIGHT_AVAILABLE = False
    Browser = None
    Page = None

# Try to import boto3, but gracefully degrade if not available
try:
    import boto3
    from botocore.exceptions import ClientError
    BOTO3_AVAILABLE = True
except ImportError:
    logger.warning("boto3 not installed - S3 upload functionality will be disabled")
    BOTO3_AVAILABLE = False
    ClientError = Exception


class ScreenshotService:
    """Service to generate and store tweet screenshots."""

    def __init__(self):
        self.s3_client = None
        if BOTO3_AVAILABLE and settings.aws_access_key_id and settings.aws_secret_access_key:
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.aws_access_key_id,
                aws_secret_access_key=settings.aws_secret_access_key,
                region_name=settings.aws_region
            )
        self.browser: Optional[Browser] = None

    async def init_browser(self):
        """Initialize Playwright browser."""
        if not PLAYWRIGHT_AVAILABLE:
            logger.warning("Playwright not available - cannot initialize browser")
            return

        if not self.browser:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=settings.playwright_headless
            )
            logger.info("Playwright browser initialized")

    async def close_browser(self):
        """Close Playwright browser."""
        if self.browser:
            await self.browser.close()
            self.browser = None
            logger.info("Playwright browser closed")

    async def capture_tweet_screenshot(self, tweet_url: str) -> Optional[bytes]:
        """
        Capture screenshot of a tweet.

        Args:
            tweet_url: URL of the tweet

        Returns:
            Screenshot image bytes or None if error
        """
        if not PLAYWRIGHT_AVAILABLE:
            logger.debug("Playwright not available - skipping screenshot")
            return None

        if not settings.enable_screenshot:
            logger.info("Screenshot generation disabled")
            return None

        try:
            await self.init_browser()

            # Create new page
            page = await self.browser.new_page(
                viewport={
                    'width': settings.screenshot_width,
                    'height': settings.screenshot_height
                }
            )

            # Navigate to tweet
            await page.goto(tweet_url, wait_until='networkidle', timeout=30000)

            # Wait for tweet to load
            await page.wait_for_selector('article[data-testid="tweet"]', timeout=10000)

            # Take screenshot of the tweet element
            tweet_element = await page.query_selector('article[data-testid="tweet"]')
            if tweet_element:
                screenshot_bytes = await tweet_element.screenshot(type='png')
                await page.close()
                logger.info(f"Screenshot captured for {tweet_url}")
                return screenshot_bytes
            else:
                logger.warning(f"Tweet element not found for {tweet_url}")
                await page.close()
                return None

        except Exception as e:
            logger.error(f"Error capturing screenshot for {tweet_url}: {e}")
            return None

    def upload_to_s3(self, image_bytes: bytes, tweet_id: str) -> Optional[str]:
        """
        Upload screenshot to S3.

        Args:
            image_bytes: Screenshot image bytes
            tweet_id: Tweet ID for filename

        Returns:
            S3 URL or None if error
        """
        if not BOTO3_AVAILABLE:
            logger.debug("boto3 not available - skipping S3 upload")
            return None

        if not self.s3_client or not settings.aws_s3_bucket:
            logger.warning("S3 not configured, skipping upload")
            return None

        try:
            # Generate filename with hash to avoid collisions
            timestamp = datetime.utcnow().strftime('%Y%m%d')
            filename = f"screenshots/{timestamp}/{tweet_id}.png"

            # Upload to S3
            self.s3_client.put_object(
                Bucket=settings.aws_s3_bucket,
                Key=filename,
                Body=image_bytes,
                ContentType='image/png',
                CacheControl='max-age=31536000'  # Cache for 1 year
            )

            # Generate public URL
            url = f"https://{settings.aws_s3_bucket}.s3.{settings.aws_region}.amazonaws.com/{filename}"
            logger.info(f"Screenshot uploaded to S3: {url}")
            return url

        except ClientError as e:
            logger.error(f"Error uploading to S3: {e}")
            return None

    async def generate_screenshot(self, tweet_url: str, tweet_id: str) -> Optional[str]:
        """
        Generate screenshot and upload to S3.

        Args:
            tweet_url: URL of the tweet
            tweet_id: Tweet ID

        Returns:
            S3 URL of screenshot or None if error
        """
        # Capture screenshot
        screenshot_bytes = await self.capture_tweet_screenshot(tweet_url)
        if not screenshot_bytes:
            return None

        # Upload to S3
        screenshot_url = self.upload_to_s3(screenshot_bytes, tweet_id)
        return screenshot_url

    async def generate_screenshots_for_highlights(
        self,
        db,
        summary_id: int
    ) -> int:
        """
        Generate screenshots only for top 10 curated tweets (highlights).

        Args:
            db: Database session
            summary_id: DailySummary ID

        Returns:
            Number of screenshots generated
        """
        from app.models.processed_tweet import ProcessedTweet
        from app.models.daily_summary import SummaryTweet, DisplayType

        logger.info(f"Generating screenshots for summary {summary_id} highlights")

        # Get highlight tweets only (top 10)
        highlight_tweets = db.query(ProcessedTweet).join(SummaryTweet).filter(
            SummaryTweet.summary_id == summary_id,
            SummaryTweet.display_type == DisplayType.HIGHLIGHT,
            ProcessedTweet.screenshot_url.is_(None)  # Not already generated
        ).all()

        if not highlight_tweets:
            logger.info("No highlights need screenshots")
            return 0

        logger.info(f"Generating screenshots for {len(highlight_tweets)} curated tweets")

        generated_count = 0

        for processed_tweet in highlight_tweets:
            try:
                tweet = processed_tweet.tweet
                screenshot_url = await self.generate_screenshot(
                    tweet.tweet_url,
                    tweet.tweet_id
                )

                if screenshot_url:
                    processed_tweet.screenshot_url = screenshot_url
                    processed_tweet.screenshot_generated_at = datetime.utcnow()
                    generated_count += 1

            except Exception as e:
                logger.error(f"Failed to generate screenshot for tweet {processed_tweet.tweet_id}: {e}")
                continue

        db.commit()
        logger.info(f"Generated {generated_count} screenshots for highlights")
        return generated_count


# Global screenshot service instance
screenshot_service = ScreenshotService()
