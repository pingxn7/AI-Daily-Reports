#!/usr/bin/env python3
"""
Import accounts from JSON file with user_id already filled in.
"""
import asyncio
import httpx
import json
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


async def add_accounts_batch(accounts: list):
    """Add accounts in batch."""
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "http://localhost:8000/api/accounts/batch",
                json=accounts
            )

            if response.status_code == 200:
                return response.json()
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
    """Import accounts from JSON file."""
    print("\n" + "="*80)
    print("Import Twitter Accounts from JSON")
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

    # Load accounts from JSON
    json_file = Path(__file__).parent / "usernames_to_add.json"

    if not json_file.exists():
        print(f"❌ Error: {json_file} not found!")
        return

    with open(json_file, 'r', encoding='utf-8') as f:
        accounts = json.load(f)

    # Filter out accounts without user_id
    valid_accounts = [acc for acc in accounts if acc.get('user_id') and acc['user_id'] != '请填入']
    missing_accounts = [acc for acc in accounts if not acc.get('user_id') or acc['user_id'] == '请填入']

    print(f"Total accounts in file: {len(accounts)}")
    print(f"Valid accounts (with user_id): {len(valid_accounts)}")
    print(f"Missing user_id: {len(missing_accounts)}\n")

    if missing_accounts:
        print("Accounts missing user_id:")
        for acc in missing_accounts:
            print(f"  - @{acc['username']}")
        print()

    if not valid_accounts:
        print("❌ No valid accounts to add. Please fill in user_id in the JSON file.")
        return

    print(f"Adding {len(valid_accounts)} accounts...\n")

    # Add accounts in batch
    result = await add_accounts_batch(valid_accounts)

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
    else:
        print("❌ Failed to add accounts. Check the logs above for details.")


if __name__ == "__main__":
    asyncio.run(main())
