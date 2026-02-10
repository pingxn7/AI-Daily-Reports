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
            "x-api-key": self.api_key,
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

    async def fetch_user_by_username(self, username: str) -> Optional[Dict]:
        """
        Fetch user information by username.

        Args:
            username: Twitter username (without @)

        Returns:
            Dictionary with user_id, username, and display_name, or None if not found
        """
        try:
            # Use the twitter/user/last_tweets endpoint to get user info
            # This endpoint works with userName parameter (note the capital N)
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/twitter/user/last_tweets",
                    headers=self.headers,
                    params={"userName": username}  # Note: userName with capital N
                )
                response.raise_for_status()
                data = response.json()

                # Check if request was successful
                if data.get("status") != "success":
                    logger.error(f"API returned non-success status for user {username}")
                    return None

                # Check if user is unavailable (suspended, etc.)
                if data.get("data", {}).get("unavailable"):
                    reason = data.get("data", {}).get("unavailableReason", "Unknown")
                    logger.warning(f"User {username} is unavailable: {reason}")
                    return None

                # Extract user info from the first tweet's author
                tweets = data.get("data", {}).get("tweets", [])
                if not tweets:
                    logger.warning(f"No tweets found for user {username}")
                    return None

                author = tweets[0].get("author", {})
                return {
                    "user_id": author.get("id"),
                    "username": author.get("userName"),
                    "display_name": author.get("name"),
                }
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching user {username}: {e}")
            return None
        except Exception as e:
            logger.error(f"Error fetching user {username}: {e}")
            return None

    async def fetch_user_tweets(
        self,
        username: str,
        since_id: Optional[str] = None,
        max_results: int = 100
    ) -> List[Dict]:
        """
        Fetch tweets from a specific user.

        Args:
            username: Twitter username (without @)
            since_id: Only return tweets after this ID
            max_results: Maximum number of tweets to fetch

        Returns:
            List of tweet dictionaries
        """
        try:
            # Use the correct twitterapi.io endpoint
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(
                    f"{self.base_url}/twitter/user/last_tweets",
                    headers=self.headers,
                    params={"userName": username}
                )
                response.raise_for_status()
                data = response.json()

                # Check if request was successful
                if data.get("status") != "success":
                    logger.error(f"API returned non-success status for user @{username}")
                    return []

                # Check if user is unavailable
                if data.get("data", {}).get("unavailable"):
                    reason = data.get("data", {}).get("unavailableReason", "Unknown")
                    logger.warning(f"User @{username} is unavailable: {reason}")
                    return []

                # Extract tweets from response
                tweets = data.get("data", {}).get("tweets", [])

                # Filter out retweets and replies
                original_tweets = [
                    t for t in tweets
                    if t.get("type") == "tweet" and not t.get("isReply", False)
                ]

                # Filter by since_id if provided
                if since_id:
                    original_tweets = [
                        t for t in original_tweets
                        if int(t.get("id", 0)) > int(since_id)
                    ]

                # Limit results
                original_tweets = original_tweets[:max_results]

                logger.info(f"Fetched {len(original_tweets)} tweets from @{username}")
                return original_tweets

        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching tweets for @{username}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching tweets for @{username}: {e}")
            return []

    def parse_tweet(self, tweet_data: dict, account_id: int) -> Dict:
        """
        Parse raw tweet data into database format.

        Args:
            tweet_data: Raw tweet data from twitterapi.io API
            account_id: Database ID of the monitored account

        Returns:
            Dictionary ready for database insertion
        """
        tweet_id = tweet_data.get("id")
        text = tweet_data.get("text", "")

        # Parse created_at from twitterapi.io format
        # Format: "Tue Feb 10 00:43:37 +0000 2026"
        created_at_str = tweet_data.get("createdAt", "")
        try:
            created_at = datetime.strptime(created_at_str, "%a %b %d %H:%M:%S %z %Y")
        except (ValueError, TypeError):
            # Fallback to current time if parsing fails
            created_at = datetime.utcnow()
            logger.warning(f"Failed to parse created_at: {created_at_str}, using current time")

        # Extract engagement metrics from twitterapi.io format
        like_count = tweet_data.get("likeCount", 0)
        retweet_count = tweet_data.get("retweetCount", 0)
        reply_count = tweet_data.get("replyCount", 0)
        bookmark_count = tweet_data.get("bookmarkCount", 0)

        # Calculate engagement score
        engagement_score = self.calculate_engagement_score({
            "like_count": like_count,
            "retweet_count": retweet_count,
            "reply_count": reply_count,
            "bookmark_count": bookmark_count
        })

        # Use the URL from API response
        tweet_url = tweet_data.get("url", f"https://twitter.com/i/status/{tweet_id}")

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

        # Fetch tweets from API using username
        tweets_data = await self.fetch_user_tweets(
            username=account.username,
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
