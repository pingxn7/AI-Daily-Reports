"""
Twitter collector service - Fetch tweets from monitored accounts.
Extracts engagement metrics and calculates engagement scores.
"""
import httpx
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from loguru import logger
from sqlalchemy.orm import Session

from app.config import settings
from app.models.tweet import Tweet
from app.models.monitored_account import MonitoredAccount


class TwitterCollector:
    """Service to collect tweets from Twitter API."""

    def __init__(self):
        self.api_key = settings.twitter_api_key
        self.base_url = settings.twitter_api_base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def calculate_engagement_score(self, tweet_data: dict) -> float:
        """
        Calculate engagement score from tweet metrics.

        Args:
            tweet_data: Dictionary containing engagement metrics

        Returns:
            Calculated engagement score
        """
        likes = tweet_data.get('like_count', 0)
        retweets = tweet_data.get('retweet_count', 0)
        replies = tweet_data.get('reply_count', 0)
        bookmarks = tweet_data.get('bookmark_count', 0)

        score = (
            likes * settings.engagement_weight_likes +
            retweets * settings.engagement_weight_retweets +
            replies * settings.engagement_weight_replies +
            bookmarks * settings.engagement_weight_bookmarks
        )

        return score

    async def fetch_user_tweets(
        self,
        user_id: str,
        since_id: Optional[str] = None,
        max_results: int = 100
    ) -> List[Dict]:
        """
        Fetch tweets from a specific user.

        Args:
            user_id: Twitter user ID
            since_id: Only return tweets after this ID
            max_results: Maximum number of tweets to fetch

        Returns:
            List of tweet dictionaries
        """
        try:
            params = {
                "max_results": max_results,
                "tweet.fields": "created_at,public_metrics,entities",
                "exclude": "retweets,replies"  # Only original tweets
            }

            if since_id:
                params["since_id"] = since_id

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/users/{user_id}/tweets",
                    headers=self.headers,
                    params=params
                )
                response.raise_for_status()
                data = response.json()

                tweets = data.get("data", [])
                logger.info(f"Fetched {len(tweets)} tweets from user {user_id}")
                return tweets

        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching tweets for user {user_id}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching tweets for user {user_id}: {e}")
            return []

    def parse_tweet(self, tweet_data: dict, account_id: int) -> Dict:
        """
        Parse raw tweet data into database format.

        Args:
            tweet_data: Raw tweet data from API
            account_id: Database ID of the monitored account

        Returns:
            Dictionary ready for database insertion
        """
        tweet_id = tweet_data.get("id")
        text = tweet_data.get("text", "")
        created_at = datetime.fromisoformat(
            tweet_data.get("created_at", "").replace("Z", "+00:00")
        )

        # Extract engagement metrics
        metrics = tweet_data.get("public_metrics", {})
        like_count = metrics.get("like_count", 0)
        retweet_count = metrics.get("retweet_count", 0)
        reply_count = metrics.get("reply_count", 0)
        bookmark_count = metrics.get("bookmark_count", 0)

        # Calculate engagement score
        engagement_score = self.calculate_engagement_score({
            "like_count": like_count,
            "retweet_count": retweet_count,
            "reply_count": reply_count,
            "bookmark_count": bookmark_count
        })

        # Build tweet URL
        tweet_url = f"https://twitter.com/i/status/{tweet_id}"

        return {
            "tweet_id": tweet_id,
            "user_id": account_id,
            "text": text,
            "created_at": created_at,
            "tweet_url": tweet_url,
            "like_count": like_count,
            "retweet_count": retweet_count,
            "reply_count": reply_count,
            "bookmark_count": bookmark_count,
            "engagement_score": engagement_score,
            "metadata": tweet_data,
            "processed": False
        }

    async def collect_tweets_for_account(
        self,
        db: Session,
        account: MonitoredAccount
    ) -> int:
        """
        Collect tweets for a single monitored account.

        Args:
            db: Database session
            account: MonitoredAccount instance

        Returns:
            Number of new tweets collected
        """
        logger.info(f"Collecting tweets for @{account.username}")

        # Fetch tweets from API
        tweets_data = await self.fetch_user_tweets(
            user_id=account.user_id,
            since_id=account.last_tweet_id
        )

        if not tweets_data:
            logger.info(f"No new tweets for @{account.username}")
            return 0

        # Parse and store tweets
        new_tweets_count = 0
        latest_tweet_id = account.last_tweet_id

        for tweet_data in tweets_data:
            tweet_id = tweet_data.get("id")

            # Check if tweet already exists (deduplication)
            existing = db.query(Tweet).filter(Tweet.tweet_id == tweet_id).first()
            if existing:
                logger.debug(f"Tweet {tweet_id} already exists, skipping")
                continue

            # Parse and create tweet
            parsed_tweet = self.parse_tweet(tweet_data, account.id)
            tweet = Tweet(**parsed_tweet)
            db.add(tweet)
            new_tweets_count += 1

            # Track latest tweet ID
            if not latest_tweet_id or int(tweet_id) > int(latest_tweet_id):
                latest_tweet_id = tweet_id

        # Update account's last_tweet_id
        if latest_tweet_id and latest_tweet_id != account.last_tweet_id:
            account.last_tweet_id = latest_tweet_id
            account.updated_at = datetime.utcnow()

        db.commit()
        logger.info(f"Collected {new_tweets_count} new tweets for @{account.username}")
        return new_tweets_count

    async def collect_all_tweets(self, db: Session) -> Dict[str, int]:
        """
        Collect tweets from all active monitored accounts.

        Args:
            db: Database session

        Returns:
            Dictionary with collection statistics
        """
        logger.info("Starting tweet collection for all accounts")

        # Get all active accounts
        accounts = db.query(MonitoredAccount).filter(
            MonitoredAccount.is_active == True
        ).all()

        if not accounts:
            logger.warning("No active accounts to monitor")
            return {"total_accounts": 0, "total_tweets": 0}

        total_tweets = 0
        successful_accounts = 0
        failed_accounts = 0

        for account in accounts:
            try:
                count = await self.collect_tweets_for_account(db, account)
                total_tweets += count
                successful_accounts += 1
            except Exception as e:
                logger.error(f"Failed to collect tweets for @{account.username}: {e}")
                failed_accounts += 1

        logger.info(
            f"Collection complete: {total_tweets} tweets from "
            f"{successful_accounts}/{len(accounts)} accounts"
        )

        return {
            "total_accounts": len(accounts),
            "successful_accounts": successful_accounts,
            "failed_accounts": failed_accounts,
            "total_tweets": total_tweets
        }


# Global collector instance
twitter_collector = TwitterCollector()
