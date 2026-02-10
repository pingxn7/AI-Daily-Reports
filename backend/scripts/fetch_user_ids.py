"""
Script to fetch Twitter user IDs for given usernames.
"""
import httpx
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings
from loguru import logger


# List of usernames to fetch
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


async def fetch_user_id(username: str) -> dict:
    """
    Fetch user ID and display name for a given username.

    Args:
        username: Twitter username (without @)

    Returns:
        Dictionary with user_id, username, and display_name
    """
    headers = {
        "x-api-key": settings.twitter_api_key,
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{settings.twitter_api_base_url}/users/by/username/{username}",
                headers=headers,
                params={"user.fields": "name,username"}
            )
            response.raise_for_status()
            data = response.json()

            user_data = data.get("data", {})
            return {
                "user_id": user_data.get("id"),
                "username": user_data.get("username"),
                "display_name": user_data.get("name"),
            }
    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching user {username}: {e}")
        return None
    except Exception as e:
        logger.error(f"Error fetching user {username}: {e}")
        return None


async def main():
    """Fetch all user IDs and print them in Python dict format."""
    logger.info(f"Fetching user IDs for {len(USERNAMES)} accounts")

    results = []
    for username in USERNAMES:
        logger.info(f"Fetching {username}...")
        user_data = await fetch_user_id(username)

        if user_data:
            results.append(user_data)
            logger.info(f"✓ {username}: {user_data['user_id']}")
        else:
            logger.warning(f"✗ Failed to fetch {username}")

        # Rate limiting - wait a bit between requests
        await asyncio.sleep(0.5)

    # Print results in Python format
    print("\n" + "="*80)
    print("ACCOUNTS_TO_MONITOR = [")
    for user in results:
        print(f'    {{')
        print(f'        "user_id": "{user["user_id"]}",')
        print(f'        "username": "{user["username"]}",')
        print(f'        "display_name": "{user["display_name"]}",')
        print(f'    }},')
    print("]")
    print("="*80)

    logger.info(f"\nSuccessfully fetched {len(results)}/{len(USERNAMES)} accounts")


if __name__ == "__main__":
    asyncio.run(main())
