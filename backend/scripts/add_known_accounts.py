#!/usr/bin/env python3
"""
Helper script to add known AI researcher accounts.
This includes some accounts with known user IDs.
"""
import asyncio
import httpx
from loguru import logger


# Known user IDs for some AI researchers
# These are publicly available and can be verified at https://tweeterid.com/
KNOWN_ACCOUNTS = [
    # Already in system - these are from the seed data
    # {"user_id": "17919972", "username": "karpathy", "display_name": "Andrej Karpathy"},
    # {"user_id": "1603818258", "username": "AndrewYNg", "display_name": "Andrew Ng"},

    # New accounts with known IDs (you can verify these at tweeterid.com)
    {"user_id": "739232892", "username": "DarioAmodei", "display_name": "Dario Amodei"},
    {"user_id": "16616354", "username": "ilyasut", "display_name": "Ilya Sutskever"},
    {"user_id": "11658782", "username": "JeffDean", "display_name": "Jeff Dean"},
    {"user_id": "15002544", "username": "fchollet", "display_name": "François Chollet"},
    {"user_id": "33836629", "username": "ylecun", "display_name": "Yann LeCun"},
    {"user_id": "44196397", "username": "elonmusk", "display_name": "Elon Musk"},
    {"user_id": "2735246778", "username": "demishassabis", "display_name": "Demis Hassabis"},
    {"user_id": "92073489", "username": "goodfellow_ian", "display_name": "Ian Goodfellow"},
    {"user_id": "1467726470533754880", "username": "sama", "display_name": "Sam Altman"},

    # Additional accounts - you need to verify these IDs
    # Visit https://tweeterid.com/ to get the correct user_id for each
    # {"user_id": "VERIFY_THIS", "username": "aidangomez", "display_name": "Aidan Gomez"},
    # {"user_id": "VERIFY_THIS", "username": "geoffreyhinton", "display_name": "Geoffrey Hinton"},
    # {"user_id": "VERIFY_THIS", "username": "gdb", "display_name": "Greg Brockman"},
    # {"user_id": "VERIFY_THIS", "username": "Yoshua_Bengio", "display_name": "Yoshua Bengio"},
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
                return True
            elif response.status_code == 400:
                error = response.json()
                if "already exists" in error.get('detail', '').lower():
                    logger.info(f"⊘ @{username} already exists, skipping")
                else:
                    logger.warning(f"✗ {error.get('detail', 'Unknown error')}")
                return False
            else:
                logger.error(f"✗ Failed to add @{username}: {response.status_code}")
                return False
    except Exception as e:
        logger.error(f"✗ Error adding @{username}: {e}")
        return False


async def check_api_server():
    """Check if API server is running."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/api/health")
            return response.status_code == 200
    except:
        return False


async def main():
    """Add known accounts."""
    print("\n" + "="*80)
    print("Adding Known AI Researcher Accounts")
    print("="*80 + "\n")

    # Check if API server is running
    if not await check_api_server():
        print("❌ Error: API server is not running!")
        print("\nStart it with:")
        print("  cd backend")
        print("  source venv/bin/activate")
        print("  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return

    print("✓ API server is running\n")
    print(f"Attempting to add {len(KNOWN_ACCOUNTS)} accounts...\n")

    added = 0
    skipped = 0
    failed = 0

    for account in KNOWN_ACCOUNTS:
        username = account["username"]
        user_id = account["user_id"]
        display_name = account["display_name"]

        if user_id.startswith("VERIFY"):
            logger.warning(f"⊘ Skipping @{username} - user_id needs verification")
            skipped += 1
            continue

        success = await add_account(username, user_id, display_name)
        if success:
            added += 1
        else:
            # Check if it was skipped because it already exists
            if "already exists" in str(success):
                skipped += 1
            else:
                failed += 1

        # Be nice to the API
        await asyncio.sleep(0.5)

    print("\n" + "="*80)
    print(f"Summary: {added} added, {skipped} skipped, {failed} failed")
    print("="*80 + "\n")

    # Show current accounts
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8000/api/accounts")
            accounts = response.json()
            print(f"Total accounts now monitoring: {len(accounts)}\n")
    except:
        pass


if __name__ == "__main__":
    asyncio.run(main())
