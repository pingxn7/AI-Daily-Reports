"""
Seed script to populate initial monitored Twitter accounts.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal
from app.models.monitored_account import MonitoredAccount
from loguru import logger


# List of AI-focused Twitter accounts to monitor
ACCOUNTS_TO_MONITOR = [
    {
        "user_id": "44196397",
        "username": "elonmusk",
        "display_name": "Elon Musk",
    },
    {
        "user_id": "33836629",
        "username": "ylecun",
        "display_name": "Yann LeCun",
    },
    {
        "user_id": "1603818258",
        "username": "AndrewYNg",
        "display_name": "Andrew Ng",
    },
    {
        "user_id": "2861417424",
        "username": "OpenAI",
        "display_name": "OpenAI",
    },
    {
        "user_id": "1603818258",
        "username": "AnthropicAI",
        "display_name": "Anthropic",
    },
    {
        "user_id": "1467726470533754880",
        "username": "sama",
        "display_name": "Sam Altman",
    },
    {
        "user_id": "17919972",
        "username": "karpathy",
        "display_name": "Andrej Karpathy",
    },
    {
        "user_id": "2735246778",
        "username": "demishassabis",
        "display_name": "Demis Hassabis",
    },
    {
        "user_id": "92073489",
        "username": "goodfellow_ian",
        "display_name": "Ian Goodfellow",
    },
    {
        "user_id": "15002544",
        "username": "fchollet",
        "display_name": "François Chollet",
    },
    {
        "user_id": "2861417424",
        "username": "GoogleAI",
        "display_name": "Google AI",
    },
    {
        "user_id": "1526228120",
        "username": "DeepMind",
        "display_name": "Google DeepMind",
    },
    {
        "user_id": "50393960",
        "username": "OpenAI",
        "display_name": "OpenAI",
    },
    {
        "user_id": "1159274324",
        "username": "hardmaru",
        "display_name": "hardmaru",
    },
    {
        "user_id": "2284730917",
        "username": "arankomatsuzaki",
        "display_name": "Aran Komatsuzaki",
    },
]


def seed_accounts():
    """Seed the database with monitored accounts."""
    db = SessionLocal()

    try:
        logger.info("Starting to seed monitored accounts")

        added_count = 0
        skipped_count = 0

        for account_data in ACCOUNTS_TO_MONITOR:
            # Check if account already exists
            existing = db.query(MonitoredAccount).filter(
                MonitoredAccount.username == account_data["username"]
            ).first()

            if existing:
                logger.info(f"Account @{account_data['username']} already exists, skipping")
                skipped_count += 1
                continue

            # Create new account
            account = MonitoredAccount(
                user_id=account_data["user_id"],
                username=account_data["username"],
                display_name=account_data["display_name"],
                is_active=True
            )

            db.add(account)
            added_count += 1
            logger.info(f"Added account @{account_data['username']}")

        db.commit()

        logger.info(
            f"Seeding complete: {added_count} accounts added, "
            f"{skipped_count} accounts skipped"
        )

    except Exception as e:
        logger.error(f"Error seeding accounts: {e}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_accounts()
