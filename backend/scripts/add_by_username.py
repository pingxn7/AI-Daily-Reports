#!/usr/bin/env python3
"""
Add Twitter accounts by username only - no need to provide user_id!
The system will automatically fetch user_id and display_name from Twitter API.
"""
import asyncio
import httpx
from loguru import logger


# List of usernames to add
USERNAMES = [
    "aidangomez",
    "karpathy",
    "DarioAmodei",
    "demishassabis",
    "EpochAIResearch",
    "drfeifei",
    "fchollet",
    "geoffreyhinton",
    "gdb",
    "ilyasut",
    "indigox",
    "jackclarkSF",
    "JeffDean",
    "johnschulman2",
    "mustafasuleyman",
    "NoamShazeer",
    "OriolVinyalsML",
    "pabbeel",
    "rasbt",
    "SebastienBubeck",
    "soumithchintala",
    "woj_zaremba",
    "Yoshua_Bengio",
    "zephyr_z9",
    "AndrewYNg",
    "_jasonwei",
    "lennysan",
    "thinkymachines",
]


async def check_api_server():
    """Check if API server is running."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/api/health")
            return response.status_code == 200
    except:
        return False


async def add_accounts_batch(usernames: list):
    """Add accounts in batch by username only."""
    try:
        # Prepare account data - only username is required!
        accounts = [{"username": username} for username in usernames]

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "http://localhost:8000/api/accounts/batch",
                json=accounts
            )

            if response.status_code == 200:
                result = response.json()
                return result
            else:
                logger.error(f"Failed to add accounts: {response.status_code}")
                logger.error(response.text)
                return None
    except Exception as e:
        logger.error(f"Error adding accounts: {e}")
        return None


async def list_accounts():
    """List all monitored accounts."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8000/api/accounts")
            return response.json()
    except:
        return []


async def main():
    """Add all accounts by username."""
    print("\n" + "="*80)
    print("Add Twitter Accounts by Username")
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
    print(f"Adding {len(USERNAMES)} accounts...\n")
    print("The system will automatically:")
    print("  1. Fetch user_id from Twitter API")
    print("  2. Fetch display_name from Twitter API")
    print("  3. Add the account to monitoring list\n")
    print("="*80 + "\n")

    # Add accounts in batch
    result = await add_accounts_batch(USERNAMES)

    if result:
        print("\n" + "="*80)
        print("Results:")
        print("="*80)
        print(f"✓ Added: {result['added']}")
        print(f"⊘ Skipped (already exist): {result['skipped']}")
        print(f"✗ Errors: {result['errors']}")
        print("="*80 + "\n")

        if result['details']['added']:
            print("Successfully added:")
            for username in result['details']['added']:
                print(f"  ✓ @{username}")
            print()

        if result['details']['skipped']:
            print("Skipped (already exist):")
            for item in result['details']['skipped']:
                print(f"  ⊘ @{item['username']}: {item['reason']}")
            print()

        if result['details']['errors']:
            print("Errors:")
            for item in result['details']['errors']:
                print(f"  ✗ @{item['username']}: {item['error']}")
            print()

        # Show current accounts
        accounts = await list_accounts()
        print("="*80)
        print(f"Total accounts now monitoring: {len(accounts)}")
        print("="*80 + "\n")

        print("Next steps:")
        print("  1. Check status: ./scripts/check_status.sh")
        print("  2. View API docs: http://localhost:8000/docs")
        print("  3. Wait for next collection cycle (every 2 hours)")
        print()
    else:
        print("❌ Failed to add accounts. Check the logs above for details.")


if __name__ == "__main__":
    asyncio.run(main())
