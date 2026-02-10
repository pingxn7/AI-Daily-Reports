#!/usr/bin/env python3
"""
发送 AI 行业日报邮件
"""
import asyncio
import sys
from pathlib import Path
from datetime import date, datetime, timedelta
from loguru import logger

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import SessionLocal
from app.services.email_service_v2 import email_service
from app.models.daily_summary import DailySummary
from app.models.processed_tweet import ProcessedTweet


async def send_daily_report(report_date: date = None):
    """发送指定日期的日报邮件"""

    if report_date is None:
        report_date = date.today() - timedelta(days=1)

    print("\n" + "="*80)
    print("AI 行业日报邮件发送")
    print("="*80 + "\n")
    print(f"📅 日期: {report_date.strftime('%Y年%m月%d日')}\n")

    db = SessionLocal()
    try:
        # 查询日报摘要
        summary = db.query(DailySummary).filter(
            DailySummary.date == report_date
        ).first()

        if not summary:
            print(f"❌ 未找到 {report_date} 的日报摘要")
            print("   请先运行 manual_summary.py 生成摘要")
            return False

        print(f"✓ 找到日报摘要")
        print(f"  推文总数: {summary.tweet_count}")
        print(f"  精选推文: {summary.top_tweets_count}")
        print(f"  摘要长度: {len(summary.highlights_summary)} 字符\n")

        # 检查是否已发送
        if summary.email_sent_at:
            print(f"⚠️  该日报已于 {summary.email_sent_at} 发送")
            print(f"   收件人: {summary.email_recipient}")
            print("\n是否要重新发送？(输入 'yes' 确认)")
            response = input().strip().lower()
            if response != 'yes':
                print("已取消")
                return False
            print()

        # 获取精选推文
        highlights = db.query(ProcessedTweet).join(
            ProcessedTweet.summary_links
        ).filter(
            ProcessedTweet.summary_links.any(summary_id=summary.id)
        ).order_by(
            ProcessedTweet.importance_score.desc()
        ).limit(10).all()

        if not highlights:
            print("❌ 未找到精选推文")
            return False

        print(f"✓ 找到 {len(highlights)} 条精选推文\n")

        # 发送邮件
        print("="*80)
        print("正在发送邮件...")
        print("="*80 + "\n")

        success = await email_service.send_daily_digest(
            summary=summary,
            highlights=highlights
        )

        if success:
            # 更新数据库
            summary.email_sent_at = datetime.now()
            from app.config import settings
            summary.email_recipient = settings.email_to
            db.commit()

            print("\n" + "="*80)
            print("✅ 日报邮件发送成功！")
            print("="*80)
            print(f"\n📧 收件人: {summary.email_recipient}")
            print(f"⏰ 发送时间: {summary.email_sent_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print("\n请检查您的邮箱，如果没有收到请查看垃圾邮件文件夹。\n")
            return True
        else:
            print("\n" + "="*80)
            print("❌ 邮件发送失败")
            print("="*80)
            print("\n请检查日志获取详细错误信息\n")
            return False

    except Exception as e:
        logger.error(f"发送日报邮件时出错: {e}")
        print(f"\n❌ 错误: {e}\n")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


if __name__ == "__main__":
    # 从命令行参数获取日期
    report_date = None
    if len(sys.argv) > 1:
        try:
            report_date = date.fromisoformat(sys.argv[1])
        except ValueError:
            print(f"❌ 错误: 无效的日期格式")
            print(f"   使用方法: python scripts/send_daily_report.py [YYYY-MM-DD]")
            print(f"   示例: python scripts/send_daily_report.py 2026-02-08")
            sys.exit(1)

    asyncio.run(send_daily_report(report_date))
