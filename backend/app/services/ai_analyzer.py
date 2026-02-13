"""
AI analyzer service - Analyze tweets using Claude API.
Identifies AI-related content, generates summaries, translations, and calculates importance scores.
"""
import anthropic
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from loguru import logger
from sqlalchemy.orm import Session

from app.config import settings
from app.models.tweet import Tweet
from app.models.processed_tweet import ProcessedTweet


class AIAnalyzer:
    """Service to analyze tweets using Claude API."""

    def __init__(self):
        # Create Anthropic client with optional base_url for proxy/relay
        client_kwargs = {"api_key": settings.anthropic_api_key}
        if settings.anthropic_base_url:
            client_kwargs["base_url"] = settings.anthropic_base_url

        self.client = anthropic.Anthropic(**client_kwargs)
        self.model = settings.claude_model
        self.max_tokens = settings.claude_max_tokens

    async def analyze_tweet_batch(self, tweets: List[Tweet]) -> List[Dict]:
        """
        Analyze a batch of tweets for AI relevance and generate summaries.

        Args:
            tweets: List of Tweet objects to analyze

        Returns:
            List of analysis results
        """
        if not tweets:
            return []

        # Prepare batch prompt
        tweets_text = "\n\n".join([
            f"Tweet {i+1} (ID: {tweet.tweet_id}):\n{tweet.text}"
            for i, tweet in enumerate(tweets)
        ])

        prompt = f"""Analyze the following tweets and determine if they are related to AI/ML/LLM technology.
For each tweet, provide:
1. is_ai_related (true/false): Whether the tweet discusses AI, machine learning, LLMs, or related topics
2. ai_relevance_score (0-10): How central and important AI is to the content (0=not related, 10=major AI announcement)
3. summary (string): A concise 1-2 sentence summary in English (only if AI-related)
4. topics (array): List of 2-4 relevant topic tags (e.g., ["GPT", "OpenAI", "LLM"])

Tweets:
{tweets_text}

Respond in JSON format as an array of objects, one per tweet in order:
[
  {{
    "tweet_id": "123...",
    "is_ai_related": true,
    "ai_relevance_score": 8,
    "summary": "OpenAI announces GPT-5 with significant performance improvements...",
    "topics": ["GPT", "OpenAI", "LLM"]
  }},
  ...
]"""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse response
            response_text = message.content[0].text
            # Extract JSON from response (handle markdown code blocks)
            if "```json" in response_text:
                response_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                response_text = response_text.split("```")[1].split("```")[0].strip()

            import json
            results = json.loads(response_text)

            logger.info(f"Analyzed {len(results)} tweets with Claude API")
            return results

        except Exception as e:
            logger.error(f"Error analyzing tweets with Claude: {e}")
            return []

    async def translate_tweet(self, text: str) -> Optional[str]:
        """
        Translate tweet text to Chinese.

        Args:
            text: Tweet text to translate

        Returns:
            Chinese translation or None if error
        """
        if not settings.enable_translation:
            return None

        prompt = f"""Translate the following tweet to Chinese (Simplified). Keep technical terms in English when appropriate.

Tweet:
{text}

Provide only the translation, no explanations."""

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            translation = message.content[0].text.strip()
            return translation

        except Exception as e:
            logger.error(f"Error translating tweet: {e}")
            return None

    def calculate_importance_score(
        self,
        engagement_score: float,
        ai_relevance_score: float,
        max_engagement: float
    ) -> float:
        """
        Combine engagement and AI relevance into importance score.

        Args:
            engagement_score: Raw engagement score
            ai_relevance_score: AI relevance score (0-10)
            max_engagement: Maximum engagement score in the batch for normalization

        Returns:
            Importance score (0-10)
        """
        # Normalize engagement score to 0-10 scale
        normalized_engagement = (engagement_score / max_engagement) * 10 if max_engagement > 0 else 0

        # Weighted combination
        importance = (
            normalized_engagement * (1 - settings.ai_relevance_weight / 10) +
            ai_relevance_score * (settings.ai_relevance_weight / 10)
        )

        return round(importance, 2)

    async def process_unprocessed_tweets(self, db: Session, batch_size: int = None) -> int:
        """
        Process all unprocessed tweets in batches.

        Args:
            db: Database session
            batch_size: Number of tweets to process per batch

        Returns:
            Number of tweets processed
        """
        if batch_size is None:
            batch_size = settings.batch_size

        logger.info("Starting AI analysis of unprocessed tweets")

        # Get unprocessed tweets
        unprocessed_tweets = db.query(Tweet).filter(
            Tweet.processed == False
        ).order_by(Tweet.created_at.desc()).limit(batch_size * 10).all()

        logger.info(f"Found {len(unprocessed_tweets)} unprocessed tweets")

        if not unprocessed_tweets:
            logger.info("No unprocessed tweets found")
            return 0

        # Calculate max engagement for normalization
        max_engagement = max(tweet.engagement_score for tweet in unprocessed_tweets) if unprocessed_tweets else 1.0
        # Ensure max_engagement is never 0 to avoid division by zero
        if max_engagement == 0:
            max_engagement = 1.0

        # Process in batches
        total_processed = 0
        ai_related_count = 0

        for i in range(0, len(unprocessed_tweets), batch_size):
            batch = unprocessed_tweets[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1}: {len(batch)} tweets")

            # Analyze batch
            analysis_results = await self.analyze_tweet_batch(batch)

            if not analysis_results:
                logger.warning(f"No results from analysis for batch {i//batch_size + 1}")
                continue

            # Process results
            for tweet, result in zip(batch, analysis_results):
                try:
                    is_ai_related = result.get("is_ai_related", False)
                    ai_relevance_score = result.get("ai_relevance_score", 0)

                    # Calculate importance score
                    importance_score = self.calculate_importance_score(
                        tweet.engagement_score,
                        ai_relevance_score,
                        max_engagement
                    )

                    # Create processed tweet record
                    processed_tweet = ProcessedTweet(
                        tweet_id=tweet.id,
                        is_ai_related=is_ai_related,
                        summary=result.get("summary") if is_ai_related else None,
                        topics=result.get("topics", []) if is_ai_related else None,
                        importance_score=importance_score,
                        translation=None,  # Translation done later for top 10 only
                        processed_at=datetime.utcnow()
                    )

                    db.add(processed_tweet)
                    tweet.processed = True
                    total_processed += 1

                    if is_ai_related:
                        ai_related_count += 1

                except Exception as e:
                    logger.error(f"Error processing tweet {tweet.tweet_id}: {e}")
                    continue

            db.commit()
            logger.info(f"Batch {i//batch_size + 1} complete: {len(batch)} tweets processed")

        percentage = (ai_related_count/total_processed*100) if total_processed > 0 else 0
        logger.info(
            f"AI analysis complete: {total_processed} tweets processed, "
            f"{ai_related_count} AI-related ({percentage:.1f}%)"
        )

        return total_processed

    async def translate_top_tweets(self, db: Session, processed_tweet_ids: List[int]) -> int:
        """
        Translate only the top tweets (for highlights section).

        Args:
            db: Database session
            processed_tweet_ids: List of ProcessedTweet IDs to translate

        Returns:
            Number of tweets translated
        """
        if not settings.enable_translation:
            logger.info("Translation disabled, skipping")
            return 0

        logger.info(f"Translating {len(processed_tweet_ids)} top tweets")

        translated_count = 0

        for tweet_id in processed_tweet_ids:
            try:
                processed_tweet = db.query(ProcessedTweet).filter(
                    ProcessedTweet.id == tweet_id
                ).first()

                if not processed_tweet or processed_tweet.translation:
                    continue

                # Get original tweet text
                tweet = processed_tweet.tweet
                translation = await self.translate_tweet(tweet.text)

                if translation:
                    processed_tweet.translation = translation
                    translated_count += 1

            except Exception as e:
                logger.error(f"Error translating tweet {tweet_id}: {e}")
                continue

        db.commit()
        logger.info(f"Translated {translated_count} tweets")
        return translated_count


# Global analyzer instance
ai_analyzer = AIAnalyzer()
