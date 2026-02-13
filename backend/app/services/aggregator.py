"""
Aggregator service - Create daily summaries with ranked tweets.
Selects top 10 for highlights, generates AI summary of key insights.
"""
from typing import List, Dict, Optional
from datetime import datetime, date, timedelta
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy import func
import anthropic

from app.config import settings
from app.models.processed_tweet import ProcessedTweet
from app.models.daily_summary import DailySummary, SummaryTweet, DisplayType
from app.services.ai_analyzer import ai_analyzer
from app.services.screenshot_service import screenshot_service


class AggregatorService:
    """Service to create daily summaries of AI news."""

    def __init__(self):
        # Create Anthropic client with optional base_url for proxy/relay
        client_kwargs = {"api_key": settings.anthropic_api_key}
        if settings.anthropic_base_url:
            client_kwargs["base_url"] = settings.anthropic_base_url

        self.client = anthropic.Anthropic(**client_kwargs)

    def generate_url_slug(self, summary_date: date) -> str:
        """
        Generate URL-friendly slug for summary.

        Args:
            summary_date: Date of the summary

        Returns:
            URL slug
        """
        return summary_date.strftime("%Y-%m-%d-ai-news")

    def extract_topics(self, tweets: List[ProcessedTweet]) -> List[str]:
        """
        Extract and count topics from tweets.

        Args:
            tweets: List of ProcessedTweet objects

        Returns:
            List of top topics
        """
        topic_counts = {}

        for tweet in tweets:
            if tweet.topics:
                for topic in tweet.topics:
                    topic_counts[topic] = topic_counts.get(topic, 0) + 1

        # Sort by count and return top topics
        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        return [topic for topic, count in sorted_topics[:10]]

    async def generate_highlights_summary(self, top_tweets: List[ProcessedTweet]) -> str:
        """
        Generate AI summary of top 10 curated tweets.

        Args:
            top_tweets: List of top 10 ProcessedTweet objects

        Returns:
            AI-generated highlights summary
        """
        if not top_tweets:
            return "No highlights available."

        # Prepare tweets for summarization
        tweets_text = "\n\n".join([
            f"Tweet {i+1} by @{tweet.tweet.account.username} ({tweet.tweet.account.display_name}):\n"
            f"Summary: {tweet.summary}\n"
            f"Likes: {tweet.tweet.like_count}, Retweets: {tweet.tweet.retweet_count}, "
            f"Replies: {tweet.tweet.reply_count}, Bookmarks: {tweet.tweet.bookmark_count}\n"
            f"Tweet URL: {tweet.tweet.tweet_url}\n"
            f"Importance: {tweet.importance_score}/10"
            for i, tweet in enumerate(top_tweets)
        ])

        prompt = f"""基于以下 10 条 AI 新闻推文，生成一份按事件聚合的中文摘要报告。

要求：
1. 将相关推文按事件主题聚合（如：新模型发布、产品更新、公司动态等）
2. 每个事件包含：事件标题、事件总结、相关推文信息
3. 严格使用以下格式：

## 🔥 今日关键信息

- 【模型】简短描述模型相关的关键信息（一段话，突出核心亮点）
- 【产品】简短描述产品相关的关键信息（一段话，突出核心亮点）
- 【公司】简短描述公司相关的关键信息（一段话，突出核心亮点）
- 【应用】简短描述应用相关的关键信息（一段话，突出核心亮点）
- 【市场】简短描述市场相关的关键信息（一段话，突出核心亮点）

（标签可以是：模型、产品、公司、应用、市场、融资、研究、开源等，每个亮点是一段关键信息）

## 📰 今日精选事件

### 事件标题1

事件的中文总结（2-3句话，描述这个事件的核心内容和意义）

#### 关键信息

- **@username (Display Name)** - 这条推文的中文摘要（提取核心观点，不需要原文）
👍 1,234 | 🔁 567 | 💬 89 | 🔖 123
[查看原文](实际的推文URL)

注意：必须使用推文数据中提供的 Tweet URL，不要使用 twitter.com/username 这样的个人主页链接

- **@username2 (Display Name)** - 另一条相关推文的中文摘要
👍 2,345 | 🔁 678 | 💬 90 | 🔖 234
[查看原文](tweet_url)

### 事件标题2

事件的中文总结...

#### 关键信息

- **@username (Display Name)** - 推文摘要
👍 xxx | 🔁 xxx | 💬 xxx | 🔖 xxx
[查看原文](url)

推文数据：
{tweets_text}

请严格按照上述格式生成报告，确保：
1. 今日关键信息部分：只列出5-8个核心亮点，每个用【标签】开头，每个亮点是一段关键信息
2. 今日精选事件部分：将推文按主题聚合成3-5个事件，每个事件下列出2-3条最相关的推文
3. 推文信息必须包含：作者、中文摘要（不需要原文）、点赞、评论、回复、转发、原文链接
4. 全部使用中文，专业且简洁
5. 不要在开头添加整体摘要段落"""

        try:
            message = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )

            summary = message.content[0].text.strip()
            logger.info("Generated highlights summary with Claude API")
            return summary

        except Exception as e:
            logger.error(f"Error generating highlights summary: {e}")
            return "今日AI领域有多项重要进展，详见下方精选推文。"

    async def create_daily_summary(
        self,
        db: Session,
        summary_date: Optional[date] = None
    ) -> Optional[DailySummary]:
        """
        Create daily summary with ranked tweets.

        Args:
            db: Database session
            summary_date: Date for summary (defaults to yesterday)

        Returns:
            Created DailySummary or None if error
        """
        if summary_date is None:
            summary_date = date.today() - timedelta(days=1)

        logger.info(f"Creating daily summary for {summary_date}")

        # Check if summary already exists
        existing = db.query(DailySummary).filter(
            func.date(DailySummary.date) == summary_date
        ).first()

        if existing:
            logger.warning(f"Summary for {summary_date} already exists")
            return existing

        # Get all AI-related tweets for the day (by tweet creation date, not processing date)
        start_datetime = datetime.combine(summary_date, datetime.min.time())
        end_datetime = datetime.combine(summary_date, datetime.max.time())

        from app.models.tweet import Tweet
        ai_tweets = db.query(ProcessedTweet).join(Tweet).filter(
            ProcessedTweet.is_ai_related == True,
            Tweet.created_at >= start_datetime,
            Tweet.created_at <= end_datetime
        ).order_by(ProcessedTweet.importance_score.desc()).all()

        if not ai_tweets:
            logger.info(f"No AI-related tweets found for {summary_date}")
            return None

        logger.info(f"Found {len(ai_tweets)} AI-related tweets for {summary_date}")

        # Select top tweets for highlights
        top_count = min(settings.top_tweets_count, len(ai_tweets))
        top_tweets = ai_tweets[:top_count]
        other_tweets = ai_tweets[top_count:]

        # Generate highlights summary using Claude (focus on top 10 only)
        highlights_summary = await self.generate_highlights_summary(top_tweets)

        # Extract topics from all tweets
        topics = self.extract_topics(ai_tweets)

        # Create summary record
        summary = DailySummary(
            date=start_datetime,
            url_slug=self.generate_url_slug(summary_date),
            tweet_count=len(ai_tweets),
            top_tweets_count=len(top_tweets),
            other_tweets_count=len(other_tweets),
            highlights_summary=highlights_summary,
            topics=topics,
            summary_text=f"Daily AI news summary for {summary_date}",
            created_at=datetime.utcnow()
        )

        db.add(summary)
        db.flush()  # Get summary.id

        # Link highlight tweets (top 10)
        for i, tweet in enumerate(top_tweets):
            link = SummaryTweet(
                summary_id=summary.id,
                processed_tweet_id=tweet.id,
                display_type=DisplayType.HIGHLIGHT,
                rank_order=i
            )
            db.add(link)

        # Link other tweets (compact display)
        for i, tweet in enumerate(other_tweets):
            link = SummaryTweet(
                summary_id=summary.id,
                processed_tweet_id=tweet.id,
                display_type=DisplayType.SUMMARY,
                rank_order=i
            )
            db.add(link)

        db.commit()
        logger.info(
            f"Created summary {summary.id}: {len(top_tweets)} highlights, "
            f"{len(other_tweets)} other tweets"
        )

        # Translate top tweets and first 10 other tweets
        top_tweet_ids = [tweet.id for tweet in top_tweets]
        other_tweet_ids = [tweet.id for tweet in other_tweets[:10]]  # 只翻译前10条
        all_tweet_ids = top_tweet_ids + other_tweet_ids
        await ai_analyzer.translate_top_tweets(db, all_tweet_ids)

        # Generate screenshots for highlights only
        await screenshot_service.generate_screenshots_for_highlights(db, summary.id)

        return summary

    async def get_summary_with_tweets(
        self,
        db: Session,
        summary_id: int
    ) -> Optional[Dict]:
        """
        Get summary with all tweets organized by display type.

        Args:
            db: Database session
            summary_id: DailySummary ID

        Returns:
            Dictionary with summary and organized tweets
        """
        summary = db.query(DailySummary).filter(DailySummary.id == summary_id).first()

        if not summary:
            return None

        # Get highlights (top 10 with full display)
        highlights = db.query(ProcessedTweet).join(SummaryTweet).filter(
            SummaryTweet.summary_id == summary_id,
            SummaryTweet.display_type == DisplayType.HIGHLIGHT
        ).order_by(SummaryTweet.rank_order).all()

        # Get other news (compact display)
        other_news = db.query(ProcessedTweet).join(SummaryTweet).filter(
            SummaryTweet.summary_id == summary_id,
            SummaryTweet.display_type == DisplayType.SUMMARY
        ).order_by(SummaryTweet.rank_order).all()

        return {
            "summary": summary,
            "highlights": highlights,
            "other_news": other_news
        }


# Global aggregator instance
aggregator_service = AggregatorService()
