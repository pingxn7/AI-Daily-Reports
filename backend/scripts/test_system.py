#!/usr/bin/env python3
"""
完整系统测试 - 验证所有组件是否正常工作
"""
import asyncio
import sys
from pathlib import Path
from datetime import date, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.config import settings
from app.models.daily_summary import DailySummary
from app.models.monitored_account import MonitoredAccount
from app.models.processed_tweet import ProcessedTweet


def test_database():
    """测试数据库连接"""
    print("\n1️⃣  数据库连接测试")
    print("   " + "-"*60)
    try:
        from sqlalchemy import text
        db = SessionLocal()
        db.execute(text('SELECT 1'))

        # 统计数据
        accounts = db.query(MonitoredAccount).count()
        tweets = db.query(ProcessedTweet).count()
        summaries = db.query(DailySummary).count()

        print(f"   ✓ 数据库连接正常")
        print(f"   • 监控账号: {accounts}")
        print(f"   • 已处理推文: {tweets}")
        print(f"   • 日报摘要: {summaries}")

        db.close()
        return True
    except Exception as e:
        print(f"   ✗ 数据库连接失败: {e}")
        return False


def test_config():
    """测试配置"""
    print("\n2️⃣  配置检查")
    print("   " + "-"*60)

    checks = {
        "数据库URL": bool(settings.database_url),
        "Twitter API Key": bool(settings.twitter_api_key and settings.twitter_api_key != "your-twitterapi-io-key-here"),
        "Claude API Key": bool(settings.anthropic_api_key and settings.anthropic_api_key != "your-anthropic-api-key-here"),
        "Resend API Key": bool(settings.resend_api_key and settings.resend_api_key != "your-resend-api-key-here"),
        "邮件功能": settings.enable_email,
        "收件人邮箱": bool(settings.email_to and settings.email_to != "your-email@example.com"),
    }

    all_ok = True
    for name, status in checks.items():
        symbol = "✓" if status else "✗"
        print(f"   {symbol} {name}")
        if not status:
            all_ok = False

    print(f"\n   时区: {settings.schedule_timezone}")
    print(f"   推文收集: {settings.schedule_tweet_collection_cron}")
    print(f"   日报发送: {settings.schedule_daily_summary_cron}")
    print(f"   收件人: {settings.email_to}")

    return all_ok


def test_scheduler():
    """测试调度器"""
    print("\n3️⃣  调度器测试")
    print("   " + "-"*60)
    try:
        from app.tasks.scheduler import start_scheduler, stop_scheduler, get_scheduler_status

        # 启动调度器
        start_scheduler()

        # 获取状态
        status = get_scheduler_status()

        print(f"   ✓ 调度器启动成功")
        print(f"   • 运行状态: {'运行中' if status['running'] else '已停止'}")
        print(f"   • 任务数量: {len(status['jobs'])}")

        for job in status['jobs']:
            print(f"\n   任务: {job['name']}")
            print(f"   • ID: {job['id']}")
            print(f"   • 下次运行: {job['next_run']}")

        # 停止调度器
        stop_scheduler()

        return True
    except Exception as e:
        print(f"   ✗ 调度器测试失败: {e}")
        return False


def test_email_service():
    """测试邮件服务"""
    print("\n4️⃣  邮件服务测试")
    print("   " + "-"*60)
    try:
        from app.services.email_service_v2 import email_service

        if not settings.enable_email:
            print("   ⚠️  邮件功能未启用")
            return False

        if not settings.resend_api_key or settings.resend_api_key == "your-resend-api-key-here":
            print("   ✗ Resend API Key 未配置")
            return False

        print(f"   ✓ 邮件服务配置正常")
        print(f"   • 发件人: {settings.email_from}")
        print(f"   • 收件人: {settings.email_to}")
        print(f"   • API Key: 已配置")

        return True
    except Exception as e:
        print(f"   ✗ 邮件服务测试失败: {e}")
        return False


def test_daily_report():
    """测试日报数据"""
    print("\n5️⃣  日报数据测试")
    print("   " + "-"*60)
    try:
        db = SessionLocal()

        # 查找最新的日报
        summary = db.query(DailySummary).order_by(DailySummary.date.desc()).first()

        if not summary:
            print("   ⚠️  暂无日报数据")
            db.close()
            return False

        print(f"   ✓ 找到日报数据")
        print(f"   • 日期: {summary.date}")
        print(f"   • 推文数: {summary.tweet_count}")
        print(f"   • 精选数: {summary.top_tweets_count}")
        print(f"   • 邮件状态: {'已发送' if summary.email_sent_at else '未发送'}")
        if summary.email_sent_at:
            print(f"   • 发送时间: {summary.email_sent_at}")
            print(f"   • 收件人: {summary.email_recipient}")

        db.close()
        return True
    except Exception as e:
        print(f"   ✗ 日报数据测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("\n" + "="*70)
    print("AI News Collector - 系统完整性测试")
    print("="*70)

    results = {
        "数据库": test_database(),
        "配置": test_config(),
        "调度器": test_scheduler(),
        "邮件服务": test_email_service(),
        "日报数据": test_daily_report(),
    }

    print("\n" + "="*70)
    print("测试结果汇总")
    print("="*70)

    for name, result in results.items():
        symbol = "✅" if result else "❌"
        print(f"   {symbol} {name}")

    all_passed = all(results.values())

    print("\n" + "="*70)
    if all_passed:
        print("🎉 所有测试通过！系统已准备就绪。")
        print("\n下一步:")
        print("   1. 启动服务: ./scripts/start.sh")
        print("   2. 查看状态: ./scripts/check_service.sh")
        print("   3. 等待明天早上8点自动发送日报")
    else:
        print("⚠️  部分测试未通过，请检查配置。")
        print("\n建议:")
        print("   1. 检查 .env 文件配置")
        print("   2. 确认数据库连接")
        print("   3. 验证 API Keys")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
