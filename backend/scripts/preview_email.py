#!/usr/bin/env python3
"""
Preview email template with sample data.
Generates an HTML file that can be opened in a browser.
"""
import sys
import os
from datetime import datetime, date

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.email_service_v2 import EmailService
from app.models.daily_summary import DailySummary
from app.models.processed_tweet import ProcessedTweet
from app.models.tweet import Tweet
from app.models.monitored_account import MonitoredAccount


def create_sample_data():
    """Create sample data for email preview."""

    # Create sample account
    account = MonitoredAccount(
        id=1,
        user_id="123456789",
        username="elonmusk",
        display_name="Elon Musk",
        is_active=True,
        created_at=datetime.now()
    )

    # Create sample tweet
    tweet = Tweet(
        id=1,
        tweet_id="1234567890",
        user_id=1,
        account=account,
        text="Excited to announce Grok 3 - our most advanced AI model yet! It can now understand images, code, and complex reasoning tasks. Available to all X Premium subscribers starting today. 🚀",
        created_at=datetime.now(),
        like_count=50000,
        retweet_count=12000,
        reply_count=3000,
        bookmark_count=8000,
        engagement_score=85.5,
        tweet_url="https://twitter.com/elonmusk/status/1234567890",
        processed=True
    )

    # Create sample processed tweet
    processed_tweet = ProcessedTweet(
        id=1,
        tweet_id=1,
        tweet=tweet,
        is_ai_related=True,
        importance_score=85.5,
        summary="Elon Musk announces Grok 3, xAI's latest AI model with multimodal capabilities",
        translation="Elon Musk 宣布 Grok 3，xAI 最新的多模态 AI 模型",
        topics=["AI Models", "xAI", "Grok"],
        screenshot_url=None,
        processed_at=datetime.now()
    )

    # Create sample summary with new event-based format
    summary = DailySummary(
        id=1,
        date=date.today(),
        url_slug="2026-02-10",
        tweet_count=150,
        top_tweets_count=5,
        other_tweets_count=25,
        topics=["AI Models", "OpenAI", "Anthropic", "Google", "xAI", "LLM", "AGI", "Robotics"],
        highlights_summary="""## 🤖 AI 行业日报 | 2026年02月10日

### 🔥 今日关键信息

- 【产品】OpenAI 发布 GPT-5 预览版，推理能力显著提升
- 【模型】xAI 推出 Grok 3 多模态模型，支持图像理解和代码生成
- 【市场】Anthropic 获得新一轮融资，估值达 300 亿美元
- 【技术】Google DeepMind RT-3 机器人展示更强泛化能力

### 📰 今日精选事件

#### OpenAI 推出 GPT-5 预览版

OpenAI 向部分合作伙伴开放 GPT-5 预览版，在推理能力和代码生成方面有显著提升，引入新的"思维链"可视化功能，预计下月正式发布。

#### 关键信息

- **@sama (Sam Altman)** - 宣布 GPT-5 预览版现已向部分合作伙伴开放，推理和代码生成能力显著改进
  👍 45000 | 🔁 10000 | 💬 2500 | 🔖 7000
  [查看原文](https://twitter.com/sama/status/1234567890)

- **@gdb (Greg Brockman)** - 展示了 GPT-5 的"思维链"可视化功能，可以看到模型的推理过程
  👍 38000 | 🔁 8500 | 💬 2000 | 🔖 6200
  [查看原文](https://twitter.com/gdb/status/1234567891)

#### xAI 发布 Grok 3 多模态模型

Elon Musk 宣布 Grok 3 正式发布，支持图像理解、代码生成和复杂推理，面向所有 X Premium 订阅用户开放，社区反响热烈。

#### 关键信息

- **@elonmusk (Elon Musk)** - 宣布 Grok 3 正式发布，这是 xAI 最先进的 AI 模型，支持多模态能力
  👍 50000 | 🔁 12000 | 💬 3000 | 🔖 8000
  [查看原文](https://twitter.com/elonmusk/status/1234567890)

- **@xai (xAI)** - 详细介绍 Grok 3 的技术特性，包括图像理解、代码生成和复杂推理能力
  👍 28000 | 🔁 6500 | 💬 1500 | 🔖 4200
  [查看原文](https://twitter.com/xai/status/1234567892)

#### Anthropic 获得新一轮融资

Anthropic 完成新一轮融资，估值达到 300 亿美元，将用于扩大 Claude 模型的训练规模，并计划在亚洲市场扩张。

#### 关键信息

- **@AnthropicAI (Anthropic)** - 宣布完成新一轮融资，估值达 300 亿美元，将加速 Claude 模型开发
  👍 32000 | 🔁 7200 | 💬 1800 | 🔖 5500
  [查看原文](https://twitter.com/AnthropicAI/status/1234567893)

#### Google DeepMind 发布机器人新进展

Google DeepMind 发布 RT-3 机器人模型，展示了更强的泛化能力，可以理解自然语言指令并执行复杂任务，在家庭场景测试中表现出色。

#### 关键信息

- **@GoogleDeepMind (Google DeepMind)** - 发布 RT-3 机器人模型，展示在家庭场景中的强大泛化能力
  👍 35000 | 🔁 8000 | 💬 2200 | 🔖 6000
  [查看原文](https://twitter.com/GoogleDeepMind/status/1234567894)

#### AI 芯片需求持续旺盛

NVIDIA H100 供不应求，多家云服务商宣布扩大 GPU 集群规模，AI 基础设施投资持续增长。

#### 关键信息

- **@nvidia (NVIDIA)** - 宣布 H100 产能持续提升，但仍无法满足市场需求
  👍 25000 | 🔁 5500 | 💬 1200 | 🔖 3800
  [查看原文](https://twitter.com/nvidia/status/1234567895)""",
        summary_text="AI 行业日报 | 2026年02月10日",
        created_at=datetime.now(),
        email_sent_at=None
    )

    return summary, [processed_tweet]


def main():
    """Generate email preview HTML."""
    print("🔍 Generating email preview...")

    # Create sample data
    summary, highlights = create_sample_data()

    # Create email service
    email_service = EmailService()

    # Generate HTML
    html_content = email_service._create_report_email_html(summary, highlights)

    # Save to file
    output_file = "/Users/pingxn7/Desktop/x/backend/email_preview.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Email preview generated: {output_file}")
    print(f"📖 Open this file in your browser to preview the email")
    print(f"\n🔗 Detail page URL: http://localhost:3000/summary/{summary.url_slug}")
    print(f"🔗 History page URL: http://localhost:3000")


if __name__ == "__main__":
    main()
