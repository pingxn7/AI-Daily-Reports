#!/usr/bin/env python3
"""
每日报告预览工具 - 查看即将发送的日报内容
"""
import sys
from pathlib import Path
from datetime import date, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.models.daily_summary import DailySummary
from app.models.processed_tweet import ProcessedTweet


def preview_daily_report(report_date: date = None):
    """预览指定日期的日报"""

    if report_date is None:
        report_date = date.today() - timedelta(days=1)

    print("\n" + "="*80)
    print(f"AI 行业日报预览 - {report_date.strftime('%Y年%m月%d日')}")
    print("="*80 + "\n")

    db = SessionLocal()
    try:
        # 查询日报
        summary = db.query(DailySummary).filter(
            DailySummary.date == report_date
        ).first()

        if not summary:
            print(f"❌ 未找到 {report_date} 的日报")
            print("   请先运行: ./venv/bin/python scripts/manual_summary.py")
            return

        # 显示基本信息
        print("📊 基本信息")
        print("-" * 80)
        print(f"日期: {summary.date}")
        print(f"推文总数: {summary.tweet_count}")
        print(f"精选推文: {summary.top_tweets_count}")
        print(f"邮件状态: {'✅ 已发送' if summary.email_sent_at else '⏳ 未发送'}")
        if summary.email_sent_at:
            print(f"发送时间: {summary.email_sent_at}")
            print(f"收件人: {summary.email_recipient}")
        print()

        # 显示热门话题
        if summary.topics:
            print("🏷️  热门话题")
            print("-" * 80)
            for i, topic in enumerate(summary.topics[:10], 1):
                print(f"{i:2d}. {topic}")
            print()

        # 显示摘要内容
        print("📝 日报摘要")
        print("-" * 80)
        print(summary.highlights_summary)
        print()

        # 获取精选推文
        highlights = db.query(ProcessedTweet).join(
            ProcessedTweet.summary_links
        ).filter(
            ProcessedTweet.summary_links.any(summary_id=summary.id)
        ).order_by(
            ProcessedTweet.importance_score.desc()
        ).limit(10).all()

        if highlights:
            print("📌 精选推文")
            print("-" * 80)
            for i, pt in enumerate(highlights, 1):
                tweet = pt.tweet
                account = tweet.account
                print(f"\n{i}. @{account.username}")
                print(f"   {tweet.text[:100]}{'...' if len(tweet.text) > 100 else ''}")
                print(f"   👍 {tweet.like_count:,} | 🔁 {tweet.retweet_count:,} | 💬 {tweet.reply_count:,}")
                if pt.translation:
                    print(f"   翻译: {pt.translation[:80]}{'...' if len(pt.translation) > 80 else ''}")

        print("\n" + "="*80)
        print("预览完成")
        print("="*80 + "\n")

        if not summary.email_sent_at:
            print("💡 提示:")
            print(f"   要发送此日报，运行: ./venv/bin/python scripts/send_daily_report.py {report_date}")
            print()

    finally:
        db.close()


if __name__ == "__main__":
    report_date = None
    if len(sys.argv) > 1:
        try:
            report_date = date.fromisoformat(sys.argv[1])
        except ValueError:
            print("❌ 错误: 无效的日期格式")
            print("   使用方法: python scripts/preview_report.py [YYYY-MM-DD]")
            print("   示例: python scripts/preview_report.py 2026-02-08")
            sys.exit(1)

    preview_daily_report(report_date)
