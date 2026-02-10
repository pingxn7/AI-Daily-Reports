"""
Script to extract Twitter usernames from URLs and add them to monitoring.
"""
import asyncio
import httpx
import re
from loguru import logger


# Twitter URLs provided by user
TWITTER_URLS = [
    "https://x.com/aidangomez",
    "https://x.com/karpathy",
    "https://x.com/DarioAmodei",
    "https://x.com/demishassabis",
    "https://x.com/EpochAIResearch",
    "https://x.com/drfeifei",
    "https://x.com/fchollet",
    "https://x.com/geoffreyhinton",
    "https://x.com/gdb",
    "https://x.com/ilyasut",
    "https://x.com/indigox",
    "https://x.com/jackclarkSF",
    "https://x.com/JeffDean",
    "https://x.com/johnschulman2",
    "https://x.com/mustafasuleyman",
    "https://x.com/NoamShazeer",
    "https://x.com/OriolVinyalsML",
    "https://x.com/pabbeel",
    "https://x.com/rasbt",
    "https://x.com/SebastienBubeck",
    "https://x.com/soumithchintala",
    "https://x.com/woj_zaremba",
    "https://x.com/Yoshua_Bengio",
    "https://x.com/zephyr_z9",
    "https://x.com/AndrewYNg",
    "https://x.com/_jasonwei",
    "https://x.com/lennysan",
    "https://x.com/thinkymachines",
]


def extract_username(url: str) -> str:
    """Extract username from Twitter URL."""
    # Remove trailing slash if present
    url = url.rstrip('/')
    # Extract username (last part of URL)
    username = url.split('/')[-1]
    return username


async def check_if_exists(username: str) -> bool:
    """Check if account already exists in the system."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8000/api/accounts")
            if response.status_code == 200:
                accounts = response.json()
                existing_usernames = [acc['username'].lower() for acc in accounts]
                return username.lower() in existing_usernames
    except:
        pass
    return False


async def fetch_user_id_from_page(username: str) -> str:
    """Try to fetch user ID from Twitter profile page."""
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(
                f"https://twitter.com/{username}",
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
                }
            )

            if response.status_code == 200:
                content = response.text

                # Try multiple patterns to find user ID
                patterns = [
                    r'"userId":"(\d+)"',
                    r'"rest_id":"(\d+)"',
                    r'"id_str":"(\d+)"',
                    r'data-user-id="(\d+)"',
                ]

                for pattern in patterns:
                    match = re.search(pattern, content)
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
    """Process all Twitter URLs."""
    print("\n" + "="*80)
    print("Processing Twitter URLs")
    print("="*80 + "\n")

    # Extract usernames
    usernames = [extract_username(url) for url in TWITTER_URLS]
    print(f"Extracted {len(usernames)} usernames from URLs\n")

    # Check which accounts already exist
    print("Checking which accounts already exist...")
    existing = []
    new_accounts = []

    for username in usernames:
        exists = await check_if_exists(username)
        if exists:
            existing.append(username)
            print(f"✓ @{username} - Already in system")
        else:
            new_accounts.append(username)
            print(f"○ @{username} - Need to add")

    print(f"\n" + "="*80)
    print(f"Summary:")
    print(f"  Already in system: {len(existing)}")
    print(f"  Need to add: {len(new_accounts)}")
    print("="*80 + "\n")

    if not new_accounts:
        print("All accounts are already in the system!")
        return

    # Try to fetch user IDs for new accounts
    print("Attempting to fetch user IDs for new accounts...")
    print("Note: This may not work due to Twitter's anti-scraping measures\n")

    accounts_with_ids = []
    accounts_without_ids = []

    for username in new_accounts:
        print(f"Fetching @{username}...")
        user_id = await fetch_user_id_from_page(username)

        if user_id:
            accounts_with_ids.append({
                "username": username,
                "user_id": user_id
            })
            print(f"  ✓ Found user_id: {user_id}")
        else:
            accounts_without_ids.append(username)
            print(f"  ✗ Could not fetch user_id")

        # Be nice to Twitter's servers
        await asyncio.sleep(2)

    # Print results
    print("\n" + "="*80)
    print("Results")
    print("="*80 + "\n")

    if accounts_with_ids:
        print(f"✓ Successfully found {len(accounts_with_ids)} user IDs:")
        print("\nYou can add these accounts with:")
        print("-" * 80)
        for acc in accounts_with_ids:
            print(f'./scripts/add_account.sh {acc["username"]} {acc["user_id"]} "{acc["username"]}"')
        print("-" * 80)

    if accounts_without_ids:
        print(f"\n✗ Could not find {len(accounts_without_ids)} user IDs:")
        print("\nPlease visit https://tweeterid.com/ to find user IDs for:")
        print("-" * 80)
        for username in accounts_without_ids:
            print(f"  - {username}")
        print("-" * 80)
        print("\nThen add them with:")
        print("  ./scripts/add_account.sh <username> <user_id> \"<display_name>\"")

    print("\n" + "="*80)


if __name__ == "__main__":
    asyncio.run(main())
