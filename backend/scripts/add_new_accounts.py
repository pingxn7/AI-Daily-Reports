"""
Script to add new monitored Twitter accounts.
Since we cannot automatically fetch user IDs, this script provides a template
for adding accounts. You need to manually find the Twitter user IDs.

To find a Twitter user ID:
1. Visit: https://tweeterid.com/
2. Enter the username (e.g., @karpathy)
3. Copy the numeric user ID

Or use the Twitter API if you have access.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal
from app.models.monitored_account import MonitoredAccount
from loguru import logger


# New accounts to add - YOU NEED TO FILL IN THE user_id VALUES
# Visit https://tweeterid.com/ to find user IDs
NEW_ACCOUNTS = [
    {
        "user_id": "17919972",  # Already known from original list
        "username": "karpathy",
        "display_name": "Andrej Karpathy",
    },
    {
        "user_id": "1603818258",  # Already known from original list
        "username": "AndrewYNg",
        "display_name": "Andrew Ng",
    },
    {
        "user_id": "15002544",  # Already known from original list
        "username": "fchollet",
        "display_name": "François Chollet",
    },
    {
        "user_id": "2735246778",  # Already known from original list
        "username": "demishassabis",
        "display_name": "Demis Hassabis",
    },
    # New accounts - NEED TO FIND user_id
    {
        "user_id": "NEED_TO_FIND",  # Visit https://tweeterid.com/
        "username": "aidangomez",
        "display_name": "Aidan Gomez",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "DarioAmodei",
        "display_name": "Dario Amodei",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "EpochAIResearch",
        "display_name": "Epoch AI Research",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "drfeifei",
        "display_name": "Fei-Fei Li",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "geoffreyhinton",
        "display_name": "Geoffrey Hinton",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "gdb",
        "display_name": "Greg Brockman",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "ilyasut",
        "display_name": "Ilya Sutskever",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "indigox",
        "display_name": "Indigo",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "jackclarkSF",
        "display_name": "Jack Clark",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "JeffDean",
        "display_name": "Jeff Dean",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "johnschulman2",
        "display_name": "John Schulman",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "mustafasuleyman",
        "display_name": "Mustafa Suleyman",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "NoamShazeer",
        "display_name": "Noam Shazeer",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "OriolVinyalsML",
        "display_name": "Oriol Vinyals",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "pabbeel",
        "display_name": "Pieter Abbeel",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "rasbt",
        "display_name": "Sebastian Raschka",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "SebastienBubeck",
        "display_name": "Sebastien Bubeck",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "soumithchintala",
        "display_name": "Soumith Chintala",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "woj_zaremba",
        "display_name": "Wojciech Zaremba",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "Yoshua_Bengio",
        "display_name": "Yoshua Bengio",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "zephyr_z9",
        "display_name": "Zephyr",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "_jasonwei",
        "display_name": "Jason Wei",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "lennysan",
        "display_name": "Lenny",
    },
    {
        "user_id": "NEED_TO_FIND",
        "username": "thinkymachines",
        "display_name": "Thinky Machines",
    },
]


def add_accounts():
    """Add new accounts to the database."""
    db = SessionLocal()

    try:
        logger.info("Starting to add new monitored accounts")

        added_count = 0
        skipped_count = 0
        missing_id_count = 0

        for account_data in NEW_ACCOUNTS:
            # Skip accounts without user_id
            if account_data["user_id"] == "NEED_TO_FIND":
                logger.warning(f"Skipping @{account_data['username']} - user_id not provided")
                missing_id_count += 1
                continue

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
            f"Complete: {added_count} added, {skipped_count} skipped, "
            f"{missing_id_count} missing user_id"
        )

        if missing_id_count > 0:
            logger.warning(
                f"\n{missing_id_count} accounts need user_id. "
                f"Visit https://tweeterid.com/ to find them."
            )

    except Exception as e:
        logger.error(f"Error adding accounts: {e}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    add_accounts()
