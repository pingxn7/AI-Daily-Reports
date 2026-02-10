#!/usr/bin/env python3
"""
Add accounts from simple text file format.
File format: username user_id (one per line)
"""
import asyncio
import httpx
from pathlib import Path
from loguru import logger


async def check_api_server():
    """Check if API server is running."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/api/health")
            return response.status_code == 200
    except:
        return False


async def add_account(username: str, user_id: str):
    """Add a single account."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "http://localhost:8000/api/accounts",
                json={
                    "user_id": user_id,
                    "username": username,
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


async def list_accounts():
    """List all monitored accounts."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8000/api/accounts")
            return response.json()
    except:
        return []


async def main():
    """Add accounts from text file."""
    print("\n" + "="*80)
    print("Add Twitter Accounts from Text File")
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

    # Load accounts from text file
    txt_file = Path(__file__).parent / "user_ids.txt"

    if not txt_file.exists():
        print(f"❌ Error: {txt_file} not found!")
        return

    accounts_to_add = []
    missing_ids = []

    with open(txt_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()

            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue

            parts = line.split()

            if len(parts) < 2:
                username = parts[0] if parts else ''
                if username:
                    missing_ids.append(username)
                continue

            username = parts[0]
            user_id = parts[1]

            accounts_to_add.append({
                'username': username,
                'user_id': user_id
            })

    print(f"Total accounts to add: {len(accounts_to_add)}")
    print(f"Missing user_id: {len(missing_ids)}\n")

    if missing_ids:
        print("⚠️  Accounts missing user_id (will be skipped):")
        for username in missing_ids:
            print(f"  - @{username}")
        print()

    if not accounts_to_add:
        print("❌ No valid accounts to add. Please fill in user_id in user_ids.txt")
        print("\nFormat: username user_id")
        print("Example: karpathy 17919972")
        return

    print(f"Adding {len(accounts_to_add)} accounts...\n")

    added = 0
    exists = 0
    errors = 0

    for account in accounts_to_add:
        result = await add_account(account['username'], account['user_id'])

        if result == "added":
            added += 1
        elif result == "exists":
            exists += 1
        else:
            errors += 1

        await asyncio.sleep(0.3)

    print("\n" + "="*80)
    print("Results:")
    print("="*80)
    print(f"✓ Added: {added}")
    print(f"⊘ Already exist: {exists}")
    print(f"✗ Errors: {errors}")
    print("="*80 + "\n")

    # Show current accounts
    accounts = await list_accounts()
    print(f"Total accounts now monitoring: {len(accounts)}\n")

    print("Next steps:")
    print("  1. Check status: ./scripts/check_status.sh")
    print("  2. View accounts: curl http://localhost:8000/api/accounts")
    print("  3. Wait for next collection cycle (every 2 hours)")
    print()


if __name__ == "__main__":
    asyncio.run(main())
