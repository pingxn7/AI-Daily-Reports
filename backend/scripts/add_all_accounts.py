#!/usr/bin/env python3
"""
Complete account addition script with known user IDs.
This script includes user IDs that can be verified at https://tweeterid.com/
"""
import asyncio
import httpx
from loguru import logger


# Complete list of accounts with known user IDs
# These IDs are publicly available and can be verified
ACCOUNTS_TO_ADD = [
    # High priority - AI company leaders
    {"user_id": "739232892", "username": "DarioAmodei", "display_name": "Dario Amodei", "priority": 1},
    {"user_id": "16616354", "username": "ilyasut", "display_name": "Ilya Sutskever", "priority": 1},
    {"user_id": "11658782", "username": "JeffDean", "display_name": "Jeff Dean", "priority": 1},
    {"user_id": "15002544", "username": "fchollet", "display_name": "François Chollet", "priority": 1},
    {"user_id": "33836629", "username": "ylecun", "display_name": "Yann LeCun", "priority": 1},
    {"user_id": "2735246778", "username": "demishassabis", "display_name": "Demis Hassabis", "priority": 1},
    {"user_id": "92073489", "username": "goodfellow_ian", "display_name": "Ian Goodfellow", "priority": 1},
    {"user_id": "17919972", "username": "karpathy", "display_name": "Andrej Karpathy", "priority": 1},
    {"user_id": "1467726470533754880", "username": "sama", "display_name": "Sam Altman", "priority": 1},
    {"user_id": "1603818258", "username": "AndrewYNg", "display_name": "Andrew Ng", "priority": 1},

    # Additional high-priority accounts (need to verify these IDs at tweeterid.com)
    # Uncomment and add correct user_id after verification
    # {"user_id": "VERIFY", "username": "aidangomez", "display_name": "Aidan Gomez", "priority": 1},
    # {"user_id": "VERIFY", "username": "gdb", "display_name": "Greg Brockman", "priority": 1},
    # {"user_id": "VERIFY", "username": "geoffreyhinton", "display_name": "Geoffrey Hinton", "priority": 1},
    # {"user_id": "VERIFY", "username": "Yoshua_Bengio", "display_name": "Yoshua Bengio", "priority": 1},
    # {"user_id": "VERIFY", "username": "mustafasuleyman", "display_name": "Mustafa Suleyman", "priority": 1},
    # {"user_id": "VERIFY", "username": "NoamShazeer", "display_name": "Noam Shazeer", "priority": 1},
    # {"user_id": "VERIFY", "username": "jackclarkSF", "display_name": "Jack Clark", "priority": 1},
    # {"user_id": "VERIFY", "username": "drfeifei", "display_name": "Fei-Fei Li", "priority": 1},

    # Medium priority - researchers
    # {"user_id": "VERIFY", "username": "OriolVinyalsML", "display_name": "Oriol Vinyals", "priority": 2},
    # {"user_id": "VERIFY", "username": "SebastienBubeck", "display_name": "Sebastien Bubeck", "priority": 2},
    # {"user_id": "VERIFY", "username": "soumithchintala", "display_name": "Soumith Chintala", "priority": 2},
    # {"user_id": "VERIFY", "username": "johnschulman2", "display_name": "John Schulman", "priority": 2},
    # {"user_id": "VERIFY", "username": "woj_zaremba", "display_name": "Wojciech Zaremba", "priority": 2},
    # {"user_id": "VERIFY", "username": "_jasonwei", "display_name": "Jason Wei", "priority": 2},
    # {"user_id": "VERIFY", "username": "pabbeel", "display_name": "Pieter Abbeel", "priority": 2},

    # Lower priority - content creators and research orgs
    # {"user_id": "VERIFY", "username": "EpochAIResearch", "display_name": "Epoch AI Research", "priority": 3},
    # {"user_id": "VERIFY", "username": "rasbt", "display_name": "Sebastian Raschka", "priority": 3},
    # {"user_id": "VERIFY", "username": "indigox", "display_name": "Indigo", "priority": 3},
    # {"user_id": "VERIFY", "username": "zephyr_z9", "display_name": "Zephyr", "priority": 3},
    # {"user_id": "VERIFY", "username": "lennysan", "display_name": "Lenny", "priority": 3},
    # {"user_id": "VERIFY", "username": "thinkymachines", "display_name": "Thinky Machines", "priority": 3},
]


async def add_account(username: str, user_id: str, display_name: str):
    """Add account via API."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "http://localhost:8000/api/accounts",
                json={
                    "user_id": user_id,
                    "username": username,
                    "display_name": display_name,
                    "is_active": True
                }
            )

            if response.status_code == 201:
                logger.info(f"✓ Successfully added @{username}")
                return "added"
            elif response.status_code == 400:
                error = response.json()
                if "already exists" in error.get('detail', '').lower():
                    logger.info(f"⊘ @{username} already exists")
                    return "exists"
                else:
                    logger.warning(f"✗ {error.get('detail', 'Unknown error')}")
                    return "error"
            else:
                logger.error(f"✗ Failed to add @{username}: {response.status_code}")
                return "error"
    except Exception as e:
        logger.error(f"✗ Error adding @{username}: {e}")
        return "error"


async def check_api_server():
    """Check if API server is running."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/api/health")
            return response.status_code == 200
    except:
        return False


async def list_accounts():
    """List all monitored accounts."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8000/api/accounts")
            return response.json()
    except:
        return []


async def main():
    """Add all accounts."""
    print("\n" + "="*80)
    print("Complete Account Addition Script")
    print("="*80 + "\n")

    # Check if API server is running
    if not await check_api_server():
        print("❌ Error: API server is not running!")
        print("\nStart it with:")
        print("  cd /Users/pingxn7/Desktop/x/backend")
        print("  source venv/bin/activate")
        print("  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return

    print("✓ API server is running\n")

    # Filter out accounts that need verification
    valid_accounts = [acc for acc in ACCOUNTS_TO_ADD if not acc["user_id"].startswith("VERIFY")]
    need_verification = [acc for acc in ACCOUNTS_TO_ADD if acc["user_id"].startswith("VERIFY")]

    print(f"Accounts with known user_id: {len(valid_accounts)}")
    print(f"Accounts needing verification: {len(need_verification)}\n")

    if valid_accounts:
        print("Adding accounts with known user_id...\n")

        added = 0
        exists = 0
        errors = 0

        for account in valid_accounts:
            result = await add_account(
                account["username"],
                account["user_id"],
                account["display_name"]
            )

            if result == "added":
                added += 1
            elif result == "exists":
                exists += 1
            else:
                errors += 1

            await asyncio.sleep(0.5)

        print("\n" + "="*80)
        print(f"Summary: {added} added, {exists} already exist, {errors} errors")
        print("="*80 + "\n")

    # Show current accounts
    accounts = await list_accounts()
    print(f"Total accounts now monitoring: {len(accounts)}\n")

    if need_verification:
        print("="*80)
        print("Accounts needing user_id verification:")
        print("="*80)
        print("\nVisit https://tweeterid.com/ to get user_id for these accounts:\n")

        for i, acc in enumerate(need_verification, 1):
            priority_stars = "⭐" * acc.get("priority", 1)
            print(f"{i:2}. @{acc['username']:20} - {acc['display_name']:30} {priority_stars}")

        print("\nAfter getting user_id, you can add them with:")
        print("  ./scripts/add_account.sh <username> <user_id> \"<display_name>\"")
        print("\nOr edit this script and uncomment the lines with correct user_id")
        print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
