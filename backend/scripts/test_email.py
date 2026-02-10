"""
测试邮件发送脚本
用于验证邮件配置是否正确，并查看邮件效果
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.database import SessionLocal
from app.services.email_service import email_service
from app.models.daily_summary import DailySummary
from app.models.processed_tweet import ProcessedTweet
from app.config import settings
from loguru import logger


async def test_email():
    """测试邮件发送功能"""
    print("\n" + "="*80)
    print("邮件发送测试")
    print("="*80 + "\n")

    # 检查邮件配置
    print("检查邮件配置...")
    print(f"  邮件功能启用: {settings.enable_email}")
    print(f"  Resend API Key: {'已配置' if settings.resend_api_key and settings.resend_api_key != 'your-resend-api-key-here' else '未配置'}")
    print(f"  发件人: {settings.email_from}")
    print(f"  收件人: {settings.email_to}")
    print()

    if not settings.enable_email:
        print("❌ 邮件功能未启用")
        print("   请在 .env 文件中设置 ENABLE_EMAIL=True")
        return

    if not settings.resend_api_key or settings.resend_api_key == 'your-resend-api-key-here':
        print("❌ Resend API Key 未配置")
        print("   请在 .env 文件中设置 RESEND_API_KEY")
        print("\n配置步骤：")
        print("1. 访问 https://resend.com/ 注册账号")
        print("2. 获取 API Key")
        print("3. 在 .env 文件中设置：")
        print("   RESEND_API_KEY=re_your_api_key")
        print("   EMAIL_FROM=onboarding@resend.dev")
        print("   EMAIL_TO=your-email@example.com")
        return

    if settings.email_to == 'your-email@example.com':
        print("❌ 收件人邮箱未配置")
        print("   请在 .env 文件中设置 EMAIL_TO 为您的邮箱地址")
        return

    print("✓ 邮件配置检查通过\n")

    # 查询数据库中的摘要和推文
    db = SessionLocal()
    try:
        print("查询数据库中的摘要...")

        # 获取最新的摘要
        summary = db.query(DailySummary).order_by(
            DailySummary.date.desc()
        ).first()

        if not summary:
            print("❌ 数据库中没有摘要数据")
            print("   系统会在每天早上 8 点（UTC）自动生成摘要")
            print("   或者等待收集足够的推文后手动生成摘要")
            print("\n创建测试摘要...")

            # 创建一个测试摘要
            summary = create_test_summary(db)
            if not summary:
                print("❌ 无法创建测试摘要（可能没有推文数据）")
                return

        print(f"✓ 找到摘要: {summary.date}")
        print(f"  推文总数: {summary.tweet_count}")
        print(f"  精选推文: {summary.top_tweets_count}")
        print()

        # 获取精选推文
        print("获取精选推文...")
        highlights = db.query(ProcessedTweet).join(
            ProcessedTweet.summary_links
        ).filter(
            ProcessedTweet.summary_links.any(summary_id=summary.id)
        ).order_by(
            ProcessedTweet.importance_score.desc()
        ).limit(10).all()

        print(f"✓ 找到 {len(highlights)} 条精选推文\n")

        if not highlights:
            print("❌ 没有精选推文数据")
            return

        # 发送测试邮件
        print("="*80)
        print("发送测试邮件...")
        print("="*80 + "\n")

        print(f"发件人: {settings.email_from}")
        print(f"收件人: {settings.email_to}")
        print(f"主题: AI News Digest - {summary.date.strftime('%Y-%m-%d')} | 今日精选{len(highlights)}条")
        print()

        success = await email_service.send_daily_digest(
            summary=summary,
            highlights=highlights
        )

        print()
        print("="*80)
        if success:
            print("✓ 邮件发送成功！")
            print()
            print("请检查您的邮箱：", settings.email_to)
            print("如果没有收到，请检查垃圾邮件文件夹")
        else:
            print("✗ 邮件发送失败")
            print("请检查日志获取详细错误信息")
        print("="*80 + "\n")

    except Exception as e:
        logger.error(f"测试邮件发送时出错: {e}")
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def create_test_summary(db):
    """创建一个测试摘要"""
    from app.models.daily_summary import DailySummary
    from datetime import date

    # 检查是否有推文数据
    tweet_count = db.query(ProcessedTweet).filter(
        ProcessedTweet.is_ai_related == True
    ).count()

    if tweet_count == 0:
        return None

    # 创建测试摘要
    test_summary = DailySummary(
        date=date.today(),
        url_slug=f"test-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        tweet_count=tweet_count,
        top_tweets_count=min(10, tweet_count),
        other_tweets_count=max(0, tweet_count - 10),
        topics=["AI Research", "Machine Learning", "Deep Learning"],
        highlights_summary="这是一个测试摘要，用于验证邮件发送功能。",
        summary_text="测试摘要内容"
    )

    db.add(test_summary)
    db.commit()
    db.refresh(test_summary)

    return test_summary


if __name__ == "__main__":
    print("\n" + "="*80)
    print("AI News Collector - 邮件发送测试")
    print("="*80)
    print("\n此脚本将：")
    print("1. 检查邮件配置")
    print("2. 查询数据库中的摘要和推文")
    print("3. 发送测试邮件到您的邮箱")
    print("\n按 Ctrl+C 取消\n")

    try:
        asyncio.run(test_email())
    except KeyboardInterrupt:
        print("\n\n已取消")
