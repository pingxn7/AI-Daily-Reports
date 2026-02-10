"""
Script to check system status and display statistics.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal
from app.models.monitored_account import MonitoredAccount
from app.models.tweet import Tweet
from app.models.processed_tweet import ProcessedTweet
from app.models.daily_summary import DailySummary
from sqlalchemy import func
from loguru import logger


def main():
    """Display system status and statistics."""
    db = SessionLocal()

    try:
        print("\n" + "="*60)
        print("AI NEWS COLLECTOR - SYSTEM STATUS")
        print("="*60 + "\n")

        # Monitored Accounts
        total_accounts = db.query(func.count(MonitoredAccount.id)).scalar()
        active_accounts = db.query(func.count(MonitoredAccount.id)).filter(
            MonitoredAccount.is_active == True
        ).scalar()

        print(f"📊 MONITORED ACCOUNTS")
        print(f"   Total: {total_accounts}")
        print(f"   Active: {active_accounts}")
        print()

        # Tweets
        total_tweets = db.query(func.count(Tweet.id)).scalar()
        processed_tweets = db.query(func.count(Tweet.id)).filter(
            Tweet.processed == True
        ).scalar()
        unprocessed_tweets = total_tweets - processed_tweets

        print(f"🐦 TWEETS")
        print(f"   Total collected: {total_tweets}")
        print(f"   Processed: {processed_tweets}")
        print(f"   Unprocessed: {unprocessed_tweets}")
        print()

        # AI Analysis
        ai_related = db.query(func.count(ProcessedTweet.id)).filter(
            ProcessedTweet.is_ai_related == True
        ).scalar()
        not_ai_related = db.query(func.count(ProcessedTweet.id)).filter(
            ProcessedTweet.is_ai_related == False
        ).scalar()
        total_processed = ai_related + not_ai_related

        ai_percentage = (ai_related / total_processed * 100) if total_processed > 0 else 0

        print(f"🤖 AI ANALYSIS")
        print(f"   Total analyzed: {total_processed}")
        print(f"   AI-related: {ai_related} ({ai_percentage:.1f}%)")
        print(f"   Not AI-related: {not_ai_related}")
        print()

        # Screenshots
        with_screenshots = db.query(func.count(ProcessedTweet.id)).filter(
            ProcessedTweet.screenshot_url.isnot(None)
        ).scalar()

        print(f"📸 SCREENSHOTS")
        print(f"   Generated: {with_screenshots}")
        print()

        # Translations
        with_translations = db.query(func.count(ProcessedTweet.id)).filter(
            ProcessedTweet.translation.isnot(None)
        ).scalar()

        print(f"🌐 TRANSLATIONS")
        print(f"   Generated: {with_translations}")
        print()

        # Daily Summaries
        total_summaries = db.query(func.count(DailySummary.id)).scalar()
        summaries_with_email = db.query(func.count(DailySummary.id)).filter(
            DailySummary.email_sent_at.isnot(None)
        ).scalar()

        latest_summary = db.query(DailySummary).order_by(
            DailySummary.date.desc()
        ).first()

        print(f"📧 DAILY SUMMARIES")
        print(f"   Total: {total_summaries}")
        print(f"   Emails sent: {summaries_with_email}")
        if latest_summary:
            print(f"   Latest: {latest_summary.date.strftime('%Y-%m-%d')} "
                  f"({latest_summary.tweet_count} tweets, "
                  f"{latest_summary.top_tweets_count} highlights)")
        print()

        # Top Topics
        print(f"🔥 TOP TOPICS (from latest summary)")
        if latest_summary and latest_summary.topics:
            for i, topic in enumerate(latest_summary.topics[:10], 1):
                print(f"   {i}. {topic}")
        else:
            print("   No topics available")
        print()

        # Engagement Stats
        avg_engagement = db.query(func.avg(Tweet.engagement_score)).filter(
            Tweet.processed == True
        ).scalar()
        max_engagement = db.query(func.max(Tweet.engagement_score)).filter(
            Tweet.processed == True
        ).scalar()

        print(f"📈 ENGAGEMENT STATS")
        print(f"   Average score: {avg_engagement:.2f}" if avg_engagement else "   No data")
        print(f"   Max score: {max_engagement:.2f}" if max_engagement else "   No data")
        print()

        # Top Tweet
        top_tweet = db.query(Tweet).join(ProcessedTweet).filter(
            ProcessedTweet.is_ai_related == True
        ).order_by(Tweet.engagement_score.desc()).first()

        if top_tweet:
            print(f"🏆 TOP TWEET")
            print(f"   Text: {top_tweet.text[:80]}...")
            print(f"   Engagement: {top_tweet.engagement_score:.0f}")
            print(f"   Likes: {top_tweet.like_count}, Retweets: {top_tweet.retweet_count}")
            print(f"   URL: {top_tweet.tweet_url}")
        print()

        print("="*60)
        print()

    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
