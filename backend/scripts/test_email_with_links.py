#!/usr/bin/env python3
"""
Test email sending with detail page links.
Sends a test email to verify the "View Details" functionality.
"""
import sys
import os
import asyncio
from datetime import datetime, date

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.email_service_v2 import EmailService
from app.models.daily_summary import DailySummary
from app.models.processed_tweet import ProcessedTweet
from app.models.tweet import Tweet
from app.models.monitored_account import MonitoredAccount
from app.config import settings


def create_test_data():
    """Create test data for email."""

    # Create sample accounts
    accounts = [
        MonitoredAccount(
            id=1,
            user_id="44196397",
            username="elonmusk",
            display_name="Elon Musk",
            is_active=True,
            created_at=datetime.now()
        ),
        MonitoredAccount(
            id=2,
            user_id="12345678",
            username="sama",
            display_name="Sam Altman",
            is_active=True,
            created_at=datetime.now()
        ),
        MonitoredAccount(
            id=3,
            user_id="87654321",
            username="demishassabis",
            display_name="Demis Hassabis",
            is_active=True,
            created_at=datetime.now()
        )
    ]

    # Create sample tweets
    tweets_data = [
        {
            "account": accounts[0],
            "text": "Excited to announce Grok 3 - our most advanced AI model yet! It can now understand images, code, and complex reasoning tasks. Available to all X Premium subscribers starting today. 🚀",
            "likes": 50000,
            "retweets": 12000,
            "replies": 3000,
            "bookmarks": 8000,
            "summary": "xAI 发布 Grok 3 多模态 AI 模型",
            "translation": "Elon Musk 宣布 Grok 3 正式发布，这是 xAI 最先进的 AI 模型，支持图像理解、代码生成和复杂推理任务。"
        },
        {
            "account": accounts[1],
            "text": "GPT-5 preview is now available to select partners. The improvements in reasoning and code generation are remarkable. Full release coming next month. Stay tuned!",
            "likes": 45000,
            "retweets": 10000,
            "replies": 2500,
            "bookmarks": 7000,
            "summary": "OpenAI 推出 GPT-5 预览版",
            "translation": "Sam Altman 宣布 GPT-5 预览版现已向部分合作伙伴开放，在推理和代码生成方面有显著改进。"
        },
        {
            "account": accounts[2],
            "text": "Thrilled to share our latest breakthrough in robotics! RT-3 can now understand natural language instructions and perform complex household tasks with unprecedented accuracy. The future is here! 🤖",
            "likes": 38000,
            "retweets": 9000,
            "replies": 2000,
            "bookmarks": 6500,
            "summary": "Google DeepMind 发布机器人新进展",
            "translation": "Demis Hassabis 分享了 DeepMind 在机器人领域的最新突破，RT-3 模型可以理解自然语言指令并执行复杂的家庭任务。"
        }
    ]

    processed_tweets = []
    for i, tweet_data in enumerate(tweets_data):
        tweet = Tweet(
            id=i+1,
            tweet_id=f"123456789{i}",
            user_id=tweet_data["account"].id,
            account=tweet_data["account"],
            text=tweet_data["text"],
            created_at=datetime.now(),
            like_count=tweet_data["likes"],
            retweet_count=tweet_data["retweets"],
            reply_count=tweet_data["replies"],
            bookmark_count=tweet_data["bookmarks"],
            engagement_score=85.5 - i*5,
            tweet_url=f"https://twitter.com/{tweet_data['account'].username}/status/123456789{i}",
            processed=True
        )

        processed_tweet = ProcessedTweet(
            id=i+1,
            tweet_id=i+1,
            tweet=tweet,
            is_ai_related=True,
            importance_score=85.5 - i*5,
            summary=tweet_data["summary"],
            translation=tweet_data["translation"],
            topics=["AI Models", "Technology", "Innovation"],
            screenshot_url=None,
            processed_at=datetime.now()
        )
        processed_tweets.append(processed_tweet)

    # Create summary
    summary = DailySummary(
        id=1,
        date=date.today(),
        url_slug=date.today().strftime("%Y-%m-%d"),
        tweet_count=150,
        top_tweets_count=10,
        other_tweets_count=25,
        topics=["AI Models", "OpenAI", "Anthropic", "Google DeepMind", "xAI", "LLM", "Robotics", "AGI"],
        highlights_summary="""# 今日 AI 行业要闻

## 🔥 重大发布

**xAI 发布 Grok 3 多模态模型**
- Elon Musk 宣布 Grok 3 正式发布，支持图像理解、代码生成和复杂推理
- 面向所有 X Premium 订阅用户开放
- 社区反响热烈，被认为是 GPT-4 的有力竞争者

**OpenAI 推出 GPT-5 预览版**
- 在推理能力和代码生成方面有显著提升
- 引入新的"思维链"可视化功能
- 预计下月正式发布

## 💡 行业动态

**Google DeepMind 发布机器人新进展**
- RT-3 机器人模型展示了更强的泛化能力
- 可以理解自然语言指令并执行复杂任务
- 在家庭场景测试中表现出色

**Anthropic 获得新一轮融资**
- 估值达到 300 亿美元
- 将用于扩大 Claude 模型的训练规模
- 计划在亚洲市场扩张

## 📊 市场观察

AI 芯片需求持续旺盛，NVIDIA H100 供不应求。多家云服务商宣布扩大 GPU 集群规模，预计 2026 年 AI 基础设施投资将超过 500 亿美元。""",
        summary_text="Today's AI news highlights major releases from xAI, OpenAI, and Google DeepMind...",
        created_at=datetime.now(),
        email_sent_at=None
    )

    return summary, processed_tweets


async def main():
    """Send test email."""
    print("=" * 60)
    print("📧 测试日报邮件发送（包含查看详情链接）")
    print("=" * 60)
    print()

    # Check configuration
    print("🔍 检查配置...")
    print(f"   Frontend URL: {settings.frontend_url}")
    print(f"   Email From: {settings.email_from}")
    print(f"   Email To: {settings.email_to}")
    print(f"   Email Enabled: {settings.enable_email}")
    print(f"   Resend API Key: {'✓ 已配置' if settings.resend_api_key else '✗ 未配置'}")
    print()

    if not settings.resend_api_key:
        print("❌ 错误: RESEND_API_KEY 未配置")
        print("   请在 .env 文件中设置 RESEND_API_KEY")
        return

    if not settings.enable_email:
        print("⚠️  警告: 邮件发送已禁用")
        print("   请在 .env 文件中设置 ENABLE_EMAIL=True")
        return

    # Create test data
    print("📝 创建测试数据...")
    summary, highlights = create_test_data()
    print(f"   日期: {summary.date}")
    print(f"   URL Slug: {summary.url_slug}")
    print(f"   推文数量: {summary.tweet_count}")
    print(f"   重点推文: {len(highlights)}")
    print()

    # Generate detail page URL
    detail_url = f"{settings.frontend_url}/summary/{summary.url_slug}"
    history_url = settings.frontend_url

    print("🔗 生成的链接:")
    print(f"   详情页: {detail_url}")
    print(f"   历史页: {history_url}")
    print()

    # Send email
    print("📤 发送测试邮件...")
    email_service = EmailService()

    try:
        success = await email_service.send_daily_digest(
            summary=summary,
            highlights=highlights,
            recipient=settings.email_to
        )

        if success:
            print("✅ 邮件发送成功!")
            print()
            print("📋 请检查以下内容:")
            print("   1. 邮件是否收到")
            print("   2. 头部是否有 '📖 查看完整详情' 按钮")
            print("   3. 底部是否有 '🌐 在线查看完整报告' 按钮")
            print("   4. 底部是否有 '📚 浏览历史日报' 链接")
            print("   5. 点击链接是否能正确跳转")
            print()
            print("🌐 测试链接:")
            print(f"   详情页: {detail_url}")
            print(f"   历史页: {history_url}")
        else:
            print("❌ 邮件发送失败")
            print("   请检查日志获取详细错误信息")

    except Exception as e:
        print(f"❌ 发送邮件时出错: {e}")
        import traceback
        traceback.print_exc()

    print()
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
