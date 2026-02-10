"""
Script to import accounts from JSON file using the API.
"""
import json
import httpx
import asyncio
from pathlib import Path
from loguru import logger


async def import_accounts_from_json(json_file: str, api_url: str = "http://localhost:8000"):
    """
    Import accounts from JSON file using the batch API endpoint.

    Args:
        json_file: Path to JSON file containing accounts
        api_url: Base URL of the API
    """
    # Read JSON file
    file_path = Path(json_file)
    if not file_path.exists():
        logger.error(f"File not found: {json_file}")
        return

    with open(file_path, 'r') as f:
        accounts = json.load(f)

    # Filter out accounts with TODO user_id
    valid_accounts = [acc for acc in accounts if acc['user_id'] != 'TODO']
    skipped = len(accounts) - len(valid_accounts)

    if skipped > 0:
        logger.warning(f"Skipping {skipped} accounts with TODO user_id")

    if not valid_accounts:
        logger.error("No valid accounts to import")
        return

    logger.info(f"Importing {len(valid_accounts)} accounts...")

    # Call batch API endpoint
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                f"{api_url}/api/accounts/batch",
                json=valid_accounts
            )
            response.raise_for_status()
            result = response.json()

            logger.info(f"✓ Successfully added {result['added']} accounts")
            logger.info(f"  Skipped: {result['skipped']}")
            logger.info(f"  Errors: {result['errors']}")

            if result['details']['errors']:
                logger.error("Errors:")
                for error in result['details']['errors']:
                    logger.error(f"  - {error['username']}: {error['error']}")

            return result

        except httpx.HTTPError as e:
            logger.error(f"HTTP error: {e}")
            return None
        except Exception as e:
            logger.error(f"Error: {e}")
            return None


async def list_accounts(api_url: str = "http://localhost:8000"):
    """List all monitored accounts."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.get(f"{api_url}/api/accounts")
            response.raise_for_status()
            accounts = response.json()

            logger.info(f"\nCurrently monitoring {len(accounts)} accounts:")
            for acc in accounts:
                status = "✓" if acc['is_active'] else "✗"
                logger.info(f"  {status} @{acc['username']} - {acc['display_name']}")

            return accounts

        except Exception as e:
            logger.error(f"Error listing accounts: {e}")
            return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python import_accounts.py <json_file>  # Import accounts from JSON")
        print("  python import_accounts.py --list       # List current accounts")
        sys.exit(1)

    if sys.argv[1] == "--list":
        asyncio.run(list_accounts())
    else:
        json_file = sys.argv[1]
        asyncio.run(import_accounts_from_json(json_file))
        print("\nCurrent accounts:")
        asyncio.run(list_accounts())
