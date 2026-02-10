"""
Create test data for demonstrating the system functionality.
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal
from app.models.tweet import Tweet
from app.models.monitored_account import MonitoredAccount
from loguru import logger

# Sample AI-related tweets
SAMPLE_TWEETS = [
    {
        "text": "Excited to announce GPT-5 will be released next month with groundbreaking multimodal capabilities!",
        "likes": 15000,
        "retweets": 3500,
        "replies": 890,
        "bookmarks": 2100
    },
    {
        "text": "Our new AI model achieves 95% accuracy on complex reasoning tasks. Paper coming soon!",
        "likes": 8900,
        "retweets": 2100,
        "replies": 450,
        "bookmarks": 1200
    },
    {
        "text": "Just published: 'Scaling Laws for Neural Language Models' - fascinating insights on model performance",
        "likes": 5600,
        "retweets": 1800,
        "replies": 320,
        "bookmarks": 980
    },
    {
        "text": "AI safety research is more important than ever. We need robust alignment techniques before AGI.",
        "likes": 12000,
        "retweets": 4200,
        "replies": 1100,
        "bookmarks": 3400
    },
    {
        "text": "New breakthrough in computer vision: our model can now understand 3D scenes from single images",
        "likes": 7800,
        "retweets": 2300,
        "replies": 560,
        "bookmarks": 1500
    },
    {
        "text": "Transformer architecture continues to dominate. What's next for deep learning?",
        "likes": 6700,
        "retweets": 1900,
        "replies": 780,
        "bookmarks": 1100
    },
    {
        "text": "Just tried the new Claude 3.5 Sonnet - the coding capabilities are incredible!",
        "likes": 9200,
        "retweets": 2800,
        "replies": 650,
        "bookmarks": 1900
    },
    {
        "text": "Machine learning is revolutionizing drug discovery. Excited about the future of AI in healthcare!",
        "likes": 11000,
        "retweets": 3100,
        "replies": 890,
        "bookmarks": 2500
    },
    {
        "text": "New paper on few-shot learning shows promising results with minimal training data",
        "likes": 4500,
        "retweets": 1200,
        "replies": 290,
        "bookmarks": 780
    },
    {
        "text": "AI ethics and responsible AI development should be at the forefront of every project",
        "likes": 8100,
        "retweets": 2400,
        "replies": 670,
        "bookmarks": 1600
    },
    {
        "text": "Reinforcement learning agents now beating humans at complex strategy games consistently",
        "likes": 10500,
        "retweets": 3300,
        "replies": 920,
        "bookmarks": 2200
    },
    {
        "text": "The future of AI is multimodal - text, images, audio, and video all working together",
        "likes": 7200,
        "retweets": 2100,
        "replies": 540,
        "bookmarks": 1400
    },
    {
        "text": "Open source AI models are democratizing access to powerful technology. This is huge!",
        "likes": 13000,
        "retweets": 4100,
        "replies": 1200,
        "bookmarks": 3100
    },
    {
        "text": "Neural networks can now generate photorealistic images from text descriptions. Mind-blowing!",
        "likes": 16000,
        "retweets": 4800,
        "replies": 1400,
        "bookmarks": 3800
    },
    {
        "text": "AI-powered code completion is changing how we write software. Productivity gains are real.",
        "likes": 9800,
        "retweets": 2900,
        "replies": 720,
        "bookmarks": 2000
    }
]

def create_test_data():
    """Create test tweets in the database."""
    db = SessionLocal()
    
    try:
        logger.info("Creating test data...")
        
        # Get monitored accounts
        accounts = db.query(MonitoredAccount).filter(
            MonitoredAccount.is_active == True
        ).all()
        
        if not accounts:
            logger.error("No monitored accounts found!")
            return
        
        logger.info(f"Found {len(accounts)} monitored accounts")
        
        # Create tweets
        created_count = 0
        base_time = datetime.utcnow() - timedelta(hours=12)
        
        for i, tweet_data in enumerate(SAMPLE_TWEETS):
            # Randomly assign to an account
            account = random.choice(accounts)
            
            # Calculate engagement score
            engagement_score = (
                tweet_data["likes"] * 1.0 +
                tweet_data["retweets"] * 2.0 +
                tweet_data["replies"] * 1.5 +
                tweet_data["bookmarks"] * 2.5
            )
            
            # Create tweet
            tweet = Tweet(
                tweet_id=f"test_tweet_{i+1}_{random.randint(1000, 9999)}",
                user_id=account.id,
                text=tweet_data["text"],
                created_at=base_time + timedelta(minutes=i*30),
                tweet_url=f"https://twitter.com/{account.username}/status/test_{i+1}",
                like_count=tweet_data["likes"],
                retweet_count=tweet_data["retweets"],
                reply_count=tweet_data["replies"],
                bookmark_count=tweet_data["bookmarks"],
                engagement_score=engagement_score,
                processed=False
            )
            
            db.add(tweet)
            created_count += 1
            logger.info(f"Created tweet {i+1}: {tweet_data['text'][:50]}...")
        
        db.commit()
        logger.info(f"✅ Successfully created {created_count} test tweets!")
        
        # Show summary
        total_tweets = db.query(Tweet).count()
        logger.info(f"Total tweets in database: {total_tweets}")
        
    except Exception as e:
        logger.error(f"Error creating test data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()
