"""
AI Daily Report Editor Service - Professional AI industry daily report generation.
Uses the AI Twitter Editor Agent system prompt for high-quality editorial content.
"""
from typing import List, Dict, Optional
from datetime import datetime, date, timedelta
from loguru import logger
from sqlalchemy.orm import Session
from sqlalchemy import func
import anthropic

from app.config import settings
from app.models.processed_tweet import ProcessedTweet
from app.models.daily_summary import DailySummary
from app.models.tweet import Tweet


class AIReportEditorService:
    """Service to generate professional AI industry daily reports."""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        """Load the AI Twitter Editor system prompt from external file."""
        # Try to load from project prompts directory first
        prompt_file = "prompts/ai_twitter_editor_system_prompt.md"
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.info(f"Loaded system prompt from {prompt_file}")
                return content
        except FileNotFoundError:
            logger.warning(f"Prompt file not found at {prompt_file}, trying Desktop location")
            # Try Desktop location
            desktop_prompt = "/Users/pingxn7/Desktop/AI_Twitter_Editor_System_Prompt_v2_FULL.md"
            try:
                with open(desktop_prompt, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "# Daily Run Prompt" in content:
                        content = content.split("# Daily Run Prompt")[0].strip()
                    return content
            except FileNotFoundError:
                logger.warning(f"Prompt file not found at {desktop_prompt}, using embedded prompt")
                # Fallback to embedded prompt
            return """# AI Twitter Editor Agent --- System Prompt v2

## ROLE

你是 **AI 行业媒体的主编（Editor-in-chief）**。
你的任务不是总结推文，而是每天产出一份： **面向 AI 从业者的专业 AI 行业日报（基于 Twitter/X）**

读者包括： - AI 产品经理 - 创业者 - 投资人 - 工程负责人

目标：让读者只看这一份日报，就不会错过 AI 行业关键变化。

------------------------------------------------------------------------

# 🌏 语言与引用（最高优先级）

## 全文中文

所有分析、解读、趋势必须使用中文撰写。 Twitter 原文引用必须保留英文原文，不可翻译。

## 每个事件必须包含 Twitter 原文引用

必须包含： - 作者 username - 英文原文逐字引用 - 👍 Likes / 🔁 Reposts / 💬 Replies / 🔖 Bookmarks / 👀 Views - 原推文链接

引用格式：

作者：@username

原文： "tweet 原文引用"

互动数据： 👍 Likes: xxxx 🔁 Reposts: xxxx 💬 Replies: xxxx 🔖 Bookmarks: xxxx 👀 Views: xxxx

链接： https://x.com/...

中文分析 → 英文证据 → 中文解读

------------------------------------------------------------------------

# 🎯 编辑原则

## Signal > Noise

仅保留： 1. 新模型 / benchmark 2. 大厂战略 3. Agent / Robotics / Infra 4. AI真实行业影响 5. 安全 / 对齐 / 开源重大事件 6. 多人讨论议题 7. 高互动推文

目标：数百推文 → 5--10 个关键事件

## Insight > Summary

禁止逐条总结推文，必须跨作者综合。

## Why it matters

解释行业意义与影响。

## For Builders

必须给出：产品 / 技术 / 商业 / 职业启示。

------------------------------------------------------------------------

# 🧾 输出结构

## 🤖 AI 行业日报 | {date}

### 🔥 今日最重要的 3 件事

新闻头条风格，每条 ≤2 行。

### 🧠 关键事件深度解读（5--8 个）

每个事件结构：

#### 发生了什么

#### 🔎 Twitter 原文引用

（严格按格式）

#### 关键细节

#### 行业解读

#### 对 AI 从业者的启示

-   产品
-   技术
-   商业
-   职业

### 📈 今日趋势

总结 3--5 个跨事件趋势。

### 🧭 值得关注的信号

Bullet list。

### 💡 编辑点评（Daily Take）

如果今天只能记住一件事。

------------------------------------------------------------------------

# ✍️ 写作风格

-   专业媒体风格
-   高信息密度
-   中文撰写
-   禁止社媒口语
-   禁止逐条复述推文

------------------------------------------------------------------------"""

    def _prepare_tweets_data(self, tweets: List[ProcessedTweet]) -> str:
        """
        Prepare tweets data for the editor prompt.
        Format optimized for editorial analysis.

        Args:
            tweets: List of ProcessedTweet objects

        Returns:
            Formatted tweets data string
        """
        tweets_data = []

        for i, processed_tweet in enumerate(tweets, 1):
            tweet = processed_tweet.tweet
            account = tweet.account

            tweet_info = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tweet {i}

作者：@{account.username}{f' ({account.display_name})' if account.display_name else ''}

原文：
"{tweet.text}"

互动数据：
👍 Likes: {tweet.like_count:,}
🔁 Reposts: {tweet.retweet_count:,}
💬 Replies: {tweet.reply_count:,}
🔖 Bookmarks: {tweet.bookmark_count:,}

链接：{tweet.tweet_url}

重要性评分：{processed_tweet.importance_score:.1f}/10
主题标签：{', '.join(processed_tweet.topics) if processed_tweet.topics else 'N/A'}
AI 初步分析：{processed_tweet.summary}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            tweets_data.append(tweet_info)

        return "\n".join(tweets_data)

    async def generate_daily_report(
        self,
        db: Session,
        report_date: Optional[date] = None
    ) -> Optional[str]:
        """
        Generate professional AI industry daily report.

        Args:
            db: Database session
            report_date: Date for report (defaults to yesterday)

        Returns:
            Generated report in markdown format or None if error
        """
        if report_date is None:
            report_date = date.today() - timedelta(days=1)

        logger.info(f"Generating AI industry daily report for {report_date}")

        # Get all AI-related tweets for the day
        start_datetime = datetime.combine(report_date, datetime.min.time())
        end_datetime = datetime.combine(report_date, datetime.max.time())

        ai_tweets = db.query(ProcessedTweet).join(ProcessedTweet.tweet).filter(
            ProcessedTweet.is_ai_related == True,
            ProcessedTweet.processed_at >= start_datetime,
            ProcessedTweet.processed_at <= end_datetime
        ).order_by(ProcessedTweet.importance_score.desc()).all()

        if not ai_tweets:
            logger.info(f"No AI-related tweets found for {report_date}")
            return None

        logger.info(f"Found {len(ai_tweets)} AI-related tweets for {report_date}")

        # Prepare tweets data
        tweets_data = self._prepare_tweets_data(ai_tweets)

        # Create the prompt
        user_prompt = f"""请基于今天采集到的 AI Twitter 数据，按照新的简化格式生成今日 AI 日报。

日期：{report_date.strftime('%Y年%m月%d日')}
目标：帮助 AI 从业者 3-5 分钟快速了解行业关键变化。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
今日采集到的推文数据（共 {len(ai_tweets)} 条）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{tweets_data}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
编辑要求
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请严格按照系统提示中的新输出结构生成日报，确保：

1. **输出结构**（必须严格遵守）

   ### 🔥 今日关键信息
   - 【标签】一句话关键信息（3-5 条）

   ### 📰 今日精选事件
   #### 事件标题
   事件概要（2-3 句话）
   #### 关键信息
   - **@username (Display Name)** - 中文摘要
     👍 Likes | 🔁 Reposts | 💬 Replies | 🔖 Bookmarks
     [查看原文](url)

2. **语言要求**（最高优先级）
   - 全部使用中文，包括推文摘要
   - 推文摘要必须用中文概括（≤50 字）
   - 不展示英文原文

3. **内容要求**
   - 今日关键信息：3-5 条，带标签【产品】【模型】【市场】等
   - 今日精选事件：3-6 个事件
   - 每个事件包含：标题、概要、关键信息（1-3 条推文）
   - 不包含：深度解读、行业分析、启示等冗长内容

4. **格式要求**
   - 事件标题：简明扼要，≤20 字
   - 事件概要：2-3 句话说明核心内容和影响
   - 推文摘要：用中文概括，≤50 字
   - 互动数据：完整显示 Likes, Reposts, Replies, Bookmarks
   - 原文链接：提供查看原文链接

5. **编辑原则**
   - Signal > Noise：从 {len(ai_tweets)} 条推文中提炼 3-6 个关键事件
   - 事件聚合：跨作者综合，按事件组织
   - 简洁高效：目标 3-5 分钟快速阅读

开始生成日报："""

        try:
            message = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=8000,  # Longer output for detailed report
                system=self.system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )

            report = message.content[0].text.strip()
            logger.info(f"Generated AI industry daily report for {report_date}")
            return report

        except Exception as e:
            logger.error(f"Error generating daily report: {e}")
            return None

    async def update_summary_with_report(
        self,
        db: Session,
        summary_id: int,
        report: str
    ) -> bool:
        """
        Update existing DailySummary with the generated report.

        Args:
            db: Database session
            summary_id: DailySummary ID
            report: Generated report content

        Returns:
            True if successful, False otherwise
        """
        try:
            summary = db.query(DailySummary).filter(
                DailySummary.id == summary_id
            ).first()

            if not summary:
                logger.error(f"Summary {summary_id} not found")
                return False

            # Update the highlights_summary with the full report
            summary.highlights_summary = report
            summary.summary_text = f"AI 行业日报 | {summary.date.strftime('%Y年%m月%d日')}"

            db.commit()
            logger.info(f"Updated summary {summary_id} with AI industry report")
            return True

        except Exception as e:
            logger.error(f"Error updating summary with report: {e}")
            db.rollback()
            return False


# Global instance
ai_report_editor = AIReportEditorService()
