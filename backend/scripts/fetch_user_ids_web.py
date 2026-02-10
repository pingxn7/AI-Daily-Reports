"""
Script to fetch Twitter user IDs using web scraping as fallback.
Since the Twitter API endpoint for username lookup is not working,
we'll try to extract user IDs from Twitter profile pages.
"""
import httpx
import asyncio
import re
from loguru import logger


USERNAMES = [
    "aidangomez",
    "DarioAmodei",
    "EpochAIResearch",
    "drfeifei",
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
    "_jasonwei",
    "lennysan",
    "thinkymachines",
]


async def fetch_user_id_from_web(username: str) -> str:
    """
    Try to fetch user ID from Twitter profile page.
    This is a fallback method when API is not available.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            # Try to fetch the profile page
            response = await client.get(
                f"https://twitter.com/{username}",
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                }
            )

            if response.status_code == 200:
                # Try to find user ID in the page content
                # Twitter embeds user ID in various places in the HTML
                content = response.text

                # Look for patterns like "userId":"123456789"
                match = re.search(r'"userId":"(\d+)"', content)
                if match:
                    return match.group(1)

                # Look for rest_id pattern
                match = re.search(r'"rest_id":"(\d+)"', content)
                if match:
                    return match.group(1)

                logger.warning(f"Could not extract user ID from page for @{username}")
                return None
            else:
                logger.error(f"Failed to fetch profile for @{username}: {response.status_code}")
                return None

    except Exception as e:
        logger.error(f"Error fetching @{username}: {e}")
        return None


async def main():
    """Fetch user IDs for all usernames."""
    logger.info(f"Attempting to fetch user IDs for {len(USERNAMES)} accounts")
    logger.info("Note: This method may not work due to Twitter's anti-scraping measures")
    logger.info("You may need to manually find user IDs at https://tweeterid.com/\n")

    results = {}

    for username in USERNAMES:
        logger.info(f"Fetching @{username}...")
        user_id = await fetch_user_id_from_web(username)

        if user_id:
            results[username] = user_id
            logger.info(f"✓ @{username}: {user_id}")
        else:
            results[username] = "NEED_TO_FIND"
            logger.warning(f"✗ @{username}: Could not fetch")

        # Be nice to Twitter's servers
        await asyncio.sleep(2)

    # Print results
    print("\n" + "="*80)
    print("Results (copy these to accounts_to_add.json):")
    print("="*80)
    for username, user_id in results.items():
        print(f'  "{username}": "{user_id}",')
    print("="*80)

    found = sum(1 for uid in results.values() if uid != "NEED_TO_FIND")
    logger.info(f"\nFound {found}/{len(USERNAMES)} user IDs")

    if found < len(USERNAMES):
        logger.warning(
            f"\nCould not find {len(USERNAMES) - found} user IDs automatically."
            f"\nPlease visit https://tweeterid.com/ to find them manually."
        )


if __name__ == "__main__":
    asyncio.run(main())
