#!/usr/bin/env python3
"""
测试定时任务配置
"""
import sys
from pathlib import Path
from datetime import datetime
import pytz

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
from apscheduler.triggers.cron import CronTrigger


def test_scheduler_config():
    """测试定时任务配置"""
    print("\n" + "="*80)
    print("定时任务配置测试")
    print("="*80 + "\n")

    # 显示配置
    print("📋 当前配置:")
    print(f"  时区: {settings.schedule_timezone}")
    print(f"  推文收集: {settings.schedule_tweet_collection_cron}")
    print(f"  日报生成: {settings.schedule_daily_summary_cron}")
    print(f"  邮件功能: {'启用' if settings.enable_email else '禁用'}")
    print(f"  收件人: {settings.email_to}")
    print()

    # 解析 cron 表达式
    print("="*80)
    print("📅 定时任务时间表")
    print("="*80 + "\n")

    tz = pytz.timezone(settings.schedule_timezone)
    now = datetime.now(tz)

    # 推文收集任务
    print("1. 推文收集任务")
    print(f"   Cron: {settings.schedule_tweet_collection_cron}")
    tweet_trigger = CronTrigger.from_crontab(
        settings.schedule_tweet_collection_cron,
        timezone=settings.schedule_timezone
    )
    next_tweet = tweet_trigger.get_next_fire_time(None, now)
    print(f"   下次运行: {next_tweet.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print()

    # 日报任务
    print("2. 日报生成与发送任务")
    print(f"   Cron: {settings.schedule_daily_summary_cron}")
    summary_trigger = CronTrigger.from_crontab(
        settings.schedule_daily_summary_cron,
        timezone=settings.schedule_timezone
    )
    next_summary = summary_trigger.get_next_fire_time(None, now)
    print(f"   下次运行: {next_summary.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"   说明: 每天北京时间早上 8:00 自动生成并发送日报")
    print()

    print("="*80)
    print("当前时间")
    print("="*80)
    print(f"  北京时间: {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"  UTC 时间: {datetime.now(pytz.UTC).strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print()

    print("="*80)
    print("✅ 配置检查完成")
    print("="*80)
    print("\n提示:")
    print("  - 定时任务会在 FastAPI 应用启动时自动运行")
    print("  - 使用 'uvicorn app.main:app' 启动应用")
    print("  - 日报将自动发送到: " + settings.email_to)
    print()


if __name__ == "__main__":
    test_scheduler_config()
