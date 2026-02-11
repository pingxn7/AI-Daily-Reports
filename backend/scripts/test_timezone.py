#!/usr/bin/env python3
"""
Test script to verify scheduler timezone configuration.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import datetime
from apscheduler.triggers.cron import CronTrigger
from app.config import settings

def test_timezone_config():
    """Test timezone configuration and next run times."""
    print("=" * 60)
    print("Scheduler Timezone Configuration Test")
    print("=" * 60)
    print()

    # Display current configuration
    print("📋 Current Configuration:")
    print(f"  Timezone: {settings.schedule_timezone}")
    print(f"  Daily Summary Cron: {settings.schedule_daily_summary_cron}")
    print(f"  Tweet Collection Cron: {settings.schedule_tweet_collection_cron}")
    print()

    # Test daily summary trigger
    print("📅 Daily Summary Schedule:")
    daily_trigger = CronTrigger.from_crontab(
        settings.schedule_daily_summary_cron,
        timezone=settings.schedule_timezone
    )

    now = datetime.now()
    next_runs = []
    for i in range(3):
        next_run = daily_trigger.get_next_fire_time(None, now if i == 0 else next_runs[-1])
        if next_run:
            next_runs.append(next_run)

    print(f"  Current time: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"  Next 3 runs:")
    for i, run_time in enumerate(next_runs, 1):
        print(f"    {i}. {run_time.strftime('%Y-%m-%d %H:%M:%S %Z')} ({run_time.tzname()})")
    print()

    # Test tweet collection trigger
    print("🐦 Tweet Collection Schedule:")
    collection_trigger = CronTrigger.from_crontab(
        settings.schedule_tweet_collection_cron,
        timezone=settings.schedule_timezone
    )

    next_runs = []
    for i in range(3):
        next_run = collection_trigger.get_next_fire_time(None, now if i == 0 else next_runs[-1])
        if next_run:
            next_runs.append(next_run)

    print(f"  Next 3 runs:")
    for i, run_time in enumerate(next_runs, 1):
        print(f"    {i}. {run_time.strftime('%Y-%m-%d %H:%M:%S %Z')} ({run_time.tzname()})")
    print()

    # Verify timezone
    print("✅ Verification:")
    if settings.schedule_timezone == "Asia/Shanghai":
        print("  ✓ Timezone is set to Asia/Shanghai (Beijing Time)")
        print("  ✓ Daily summary will run at 8:00 AM Beijing Time")
    elif settings.schedule_timezone == "UTC":
        print("  ⚠ Timezone is set to UTC")
        print("  ⚠ Daily summary will run at 8:00 AM UTC (4:00 PM Beijing Time)")
    else:
        print(f"  ℹ Timezone is set to {settings.schedule_timezone}")
    print()
    print("=" * 60)

if __name__ == "__main__":
    test_timezone_config()
