"""
Enhanced email service with optimized AI industry daily report format.
Follows professional editorial standards with Chinese analysis and English evidence.
"""
from typing import Optional
from datetime import datetime
from loguru import logger
import resend
import re

from app.config import settings
from app.models.daily_summary import DailySummary
from app.models.processed_tweet import ProcessedTweet


class EmailService:
    """Service to send email notifications."""

    def __init__(self):
        if settings.resend_api_key:
            resend.api_key = settings.resend_api_key

    def _format_tweet_reference(self, tweet: ProcessedTweet) -> str:
        """
        Format a single tweet as a reference block (Chinese analysis + English evidence).
        Follows the editorial standard: 中文分析 → 英文证据 → 中文解读
        """
        t = tweet.tweet
        account = t.account

        html = f"""
        <div style="margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #667eea;">
            <!-- Author -->
            <div style="margin-bottom: 12px;">
                <strong style="color: #667eea; font-size: 15px;">作者：@{account.username}</strong>
                {f'<span style="color: #666; margin-left: 8px;">({account.display_name})</span>' if account.display_name else ''}
            </div>

            <!-- Original Tweet (English) -->
            <div style="margin: 12px 0; padding: 15px; background: white; border-radius: 6px; border: 1px solid #e0e0e0;">
                <div style="color: #999; font-size: 12px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">原文</div>
                <p style="margin: 0; color: #333; line-height: 1.7; font-size: 15px; white-space: pre-wrap; font-style: italic;">"{t.text}"</p>
            </div>

            <!-- Engagement Data -->
            <div style="margin: 12px 0; padding: 10px; background: white; border-radius: 6px;">
                <div style="color: #999; font-size: 12px; margin-bottom: 6px;">互动数据</div>
                <div style="color: #666; font-size: 14px; display: flex; flex-wrap: wrap; gap: 15px;">
                    <span>👍 Likes: {t.like_count:,}</span>
                    <span>🔁 Reposts: {t.retweet_count:,}</span>
                    <span>💬 Replies: {t.reply_count:,}</span>
                    <span>🔖 Bookmarks: {t.bookmark_count:,}</span>
                </div>
            </div>

            <!-- Link -->
            <div style="margin-top: 12px;">
                <a href="{t.tweet_url}" style="color: #667eea; text-decoration: none; font-size: 14px; font-weight: 500;">🔗 查看原推文 →</a>
            </div>
        </div>
        """
        return html

    def _parse_event_based_report(self, markdown_text: str) -> dict:
        """
        Parse event-based report format from AI-generated markdown.

        The AI generates format like:
        ## 📰 今日精选事件
        ### Event Title
        Event summary
        #### 关键信息
        - **@username (Name)** - summary
          👍 Likes | 🔁 Reposts | ...
          [查看原文](url)

        But the ### splits create alternating blocks of titles and "关键信息" sections.

        Returns:
            {
                'key_highlights': [{'tag': '产品', 'text': '...'}],
                'events': [...]
            }
        """
        result = {
            'key_highlights': [],
            'events': []
        }

        # Parse key highlights
        highlights_match = re.search(r'##\s*🔥\s*今日关键信息(.*?)(?=##|$)', markdown_text, re.DOTALL)
        if highlights_match:
            highlights_text = highlights_match.group(1)
            for line in highlights_text.split('\n'):
                line = line.strip()
                match = re.match(r'^-\s*【(.+?)】\s*(.+)$', line)
                if match:
                    result['key_highlights'].append({
                        'tag': match.group(1),
                        'text': match.group(2)
                    })

        # Parse events section
        events_match = re.search(r'##\s*📰\s*今日精选事件(.*?)$', markdown_text, re.DOTALL)
        if not events_match:
            return result

        events_text = events_match.group(1)

        # Split by ### to get blocks
        blocks = re.split(r'###\s+', events_text)

        # Process blocks in pairs: title/summary block + 关键信息 block
        i = 0
        while i < len(blocks):
            block = blocks[i].strip()
            if not block:
                i += 1
                continue

            # Check if this is a title/summary block (not starting with "关键信息")
            if not block.startswith('关键信息'):
                # This is a title/summary block
                lines = block.split('\n', 1)
                title = lines[0].strip()
                summary = lines[1].strip() if len(lines) > 1 else ''

                # Remove any "####" markers from summary
                summary = re.sub(r'####.*$', '', summary, flags=re.DOTALL).strip()

                # Look for the next block which should be "关键信息"
                tweets = []
                if i + 1 < len(blocks):
                    next_block = blocks[i + 1].strip()
                    if next_block.startswith('关键信息'):
                        # Parse tweets from this block
                        tweet_pattern = r'-\s*\*\*(@\w+)\s*\(([^)]+)\)\*\*\s*-\s*([^\n]+)\n\s*👍\s*([\d,]+)\s*\|\s*🔁\s*([\d,]+)\s*\|\s*💬\s*([\d,]+)\s*\|\s*🔖\s*([\d,]+)\s*\n\s*\[查看原文\]\(([^)]+)\)'

                        for tweet_match in re.finditer(tweet_pattern, next_block):
                            tweets.append({
                                'author': f'{tweet_match.group(1)} ({tweet_match.group(2)})',
                                'summary': tweet_match.group(3).strip(),
                                'metrics': {
                                    'likes': int(tweet_match.group(4).replace(',', '')),
                                    'retweets': int(tweet_match.group(5).replace(',', '')),
                                    'replies': int(tweet_match.group(6).replace(',', '')),
                                    'bookmarks': int(tweet_match.group(7).replace(',', ''))
                                },
                                'url': tweet_match.group(8)
                            })

                        i += 1  # Skip the next block since we processed it

                # Add event
                result['events'].append({
                    'title': title,
                    'summary': summary,
                    'tweets': tweets
                })

            i += 1

        return result

    def _format_key_highlights(self, highlights: list) -> str:
        """Format key highlights section as HTML."""
        if not highlights:
            return ''

        html = '<div style="margin: 30px 0; padding: 25px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 12px;">'
        html += '<h2 style="margin: 0 0 20px 0; color: #333; font-size: 24px; font-weight: 700;">🔥 今日关键信息</h2>'
        html += '<ul style="margin: 0; padding: 0; list-style: none;">'

        for item in highlights:
            tag = item['tag']
            text = item['text']
            html += f'''
            <li style="margin: 12px 0; line-height: 1.7; font-size: 15px;">
                <span style="display: inline-block; padding: 4px 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 4px; font-size: 12px; font-weight: 600; margin-right: 10px;">{tag}</span>
                <span style="color: #333;">{text}</span>
            </li>
            '''

        html += '</ul></div>'
        return html

    def _format_events(self, events: list) -> str:
        """Format events section as HTML."""
        if not events:
            return ''

        html = '<div style="margin: 30px 0;">'
        html += '<h2 style="margin: 0 0 25px 0; color: #333; font-size: 24px; font-weight: 700; border-bottom: 3px solid #667eea; padding-bottom: 10px;">📰 今日精选事件</h2>'

        for i, event in enumerate(events, 1):
            html += f'''
            <div style="margin: 30px 0; padding: 25px; background: #ffffff; border-radius: 12px; border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <h3 style="margin: 0 0 15px 0; color: #333; font-size: 20px; font-weight: 600;">事件 {i}: {event['title']}</h3>

                <div style="margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 3px solid #667eea;">
                    <div style="color: #999; font-size: 12px; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">事件概要</div>
                    <p style="margin: 0; color: #333; line-height: 1.7; font-size: 15px;">{event['summary']}</p>
                </div>

                <div style="margin-top: 20px;">
                    <h4 style="margin: 0 0 15px 0; color: #667eea; font-size: 16px; font-weight: 600;">关键信息</h4>
            '''

            # Format tweets
            for tweet in event['tweets']:
                metrics = tweet['metrics']
                metrics_str = ' | '.join([
                    f"👍 {metrics.get('likes', 0):,}",
                    f"🔁 {metrics.get('retweets', 0):,}",
                    f"💬 {metrics.get('replies', 0):,}",
                    f"🔖 {metrics.get('bookmarks', 0):,}"
                ])

                html += f'''
                <div style="margin: 15px 0; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 3px solid #667eea;">
                    <div style="color: #667eea; font-weight: 600; font-size: 14px; margin-bottom: 8px;">{tweet['author']}</div>
                    <div style="color: #333; line-height: 1.6; margin-bottom: 10px; font-size: 14px;">{tweet['summary']}</div>
                    <div style="color: #666; font-size: 13px; margin-bottom: 8px;">{metrics_str}</div>
                    <a href="{tweet['url']}" style="color: #667eea; text-decoration: none; font-size: 13px; font-weight: 500;">🔗 查看原文 →</a>
                </div>
                '''

            html += '</div></div>'

        html += '</div>'
        return html

    def _create_report_email_html(
        self,
        summary: DailySummary,
        highlights: list[ProcessedTweet]
    ) -> str:
        """Create HTML email with optimized event-based format."""

        # Format date
        date_str = summary.date.strftime('%Y年%m月%d日')

        # Build detail page URL
        detail_url = f"{settings.frontend_url}/summary/{summary.url_slug}"

        # Parse event-based report
        parsed_report = self._parse_event_based_report(summary.highlights_summary)

        # Format key highlights
        key_highlights_html = self._format_key_highlights(parsed_report['key_highlights'])

        # Format events
        events_html = self._format_events(parsed_report['events'])

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        @media only screen and (max-width: 600px) {{
            .content {{ padding: 20px 15px !important; }}
            h1 {{ font-size: 24px !important; }}
            h2 {{ font-size: 20px !important; }}
            h3 {{ font-size: 18px !important; }}
        }}
    </style>
</head>
<body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, 'PingFang SC', 'Microsoft YaHei', sans-serif; background-color: #f5f5f5;">
    <div style="max-width: 800px; margin: 0 auto; background-color: white;">

        <!-- Header -->
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 50px 30px; text-align: center;">
            <h1 style="margin: 0; color: white; font-size: 36px; font-weight: 700; letter-spacing: -0.5px;">
                🤖 AI 行业日报
            </h1>
            <p style="margin: 15px 0 0 0; color: rgba(255,255,255,0.95); font-size: 18px; font-weight: 400;">
                {date_str}
            </p>
            <p style="margin: 8px 0 0 0; color: rgba(255,255,255,0.8); font-size: 14px;">
                3 分钟了解 AI 行业关键变化
            </p>

            <!-- View Details Button -->
            <div style="margin-top: 25px;">
                <a href="{detail_url}" style="display: inline-block; padding: 14px 32px; background: white; color: #667eea; text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); transition: all 0.3s;">
                    📖 查看完整详情
                </a>
            </div>
            <p style="margin: 12px 0 0 0; color: rgba(255,255,255,0.7); font-size: 13px;">
                在线查看完整报告 · 浏览历史日报
            </p>
        </div>

        <!-- Main Content -->
        <div class="content" style="padding: 40px 30px;">

            <!-- Key Highlights -->
            {key_highlights_html}

            <!-- Events -->
            {events_html}

            <!-- Statistics -->
            <div style="margin-top: 50px; padding: 25px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 12px;">
                <h3 style="margin: 0 0 20px 0; color: #333; font-size: 18px; font-weight: 600;">📊 今日数据</h3>
                <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px;">
                    <div style="text-align: center;">
                        <div style="color: #666; font-size: 14px; margin-bottom: 5px;">监控推文</div>
                        <div style="color: #667eea; font-size: 32px; font-weight: 700;">{summary.tweet_count}</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="color: #666; font-size: 14px; margin-bottom: 5px;">关键事件</div>
                        <div style="color: #764ba2; font-size: 32px; font-weight: 700;">{summary.top_tweets_count}</div>
                    </div>
                </div>
            </div>

            <!-- Topics -->
            {f'''
            <div style="margin-top: 30px;">
                <h3 style="color: #333; font-size: 18px; margin-bottom: 15px; font-weight: 600;">🏷️ 热门话题</h3>
                <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                    {"".join([f'<span style="display: inline-block; padding: 8px 16px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 20px; font-size: 13px; font-weight: 500;">#{topic}</span>' for topic in summary.topics[:10]])}
                </div>
            </div>
            ''' if summary.topics else ''}

        </div>

        <!-- Footer -->
        <div style="background: #2d3748; padding: 40px 30px; text-align: center; color: white;">
            <p style="margin: 0 0 15px 0; font-size: 16px; font-weight: 500;">
                🤖 由 Claude AI 自动生成
            </p>
            <p style="margin: 0 0 10px 0; color: rgba(255,255,255,0.7); font-size: 14px;">
                基于 {summary.tweet_count} 条推文 · 精选 {summary.top_tweets_count} 个关键事件
            </p>

            <!-- View Details Link -->
            <div style="margin: 25px 0;">
                <a href="{detail_url}" style="display: inline-block; padding: 12px 28px; background: rgba(255,255,255,0.1); color: white; text-decoration: none; border-radius: 6px; font-weight: 500; font-size: 15px; border: 1px solid rgba(255,255,255,0.2); transition: all 0.3;">
                    🌐 在线查看完整报告
                </a>
            </div>

            <!-- Browse History Link -->
            <div style="margin: 15px 0;">
                <a href="{settings.frontend_url}" style="color: rgba(255,255,255,0.6); text-decoration: none; font-size: 14px; border-bottom: 1px solid rgba(255,255,255,0.3);">
                    📚 浏览历史日报
                </a>
            </div>

            <p style="margin: 20px 0 0 0; color: rgba(255,255,255,0.5); font-size: 12px;">
                简洁高效 · 事件聚合
            </p>
        </div>

    </div>
</body>
</html>
        """
        return html

    async def send_daily_digest(
        self,
        summary: DailySummary,
        highlights: list[ProcessedTweet],
        recipient: Optional[str] = None
    ) -> bool:
        """
        Send daily digest email with AI industry report.

        Args:
            summary: DailySummary object
            highlights: List of highlight ProcessedTweet objects
            recipient: Email recipient (defaults to settings.email_to)

        Returns:
            True if sent successfully, False otherwise
        """
        if not settings.enable_email:
            logger.info("Email sending is disabled")
            return False

        if not settings.resend_api_key:
            logger.error("Resend API key not configured")
            return False

        recipient = recipient or settings.email_to
        date_str = summary.date.strftime('%Y年%m月%d日')

        try:
            html_content = self._create_report_email_html(summary, highlights)

            params = {
                "from": settings.email_from,
                "to": [recipient],
                "subject": f"🤖 AI 行业日报 | {date_str}",
                "html": html_content,
            }

            email = resend.Emails.send(params)
            logger.info(f"Daily digest email sent to {recipient}: {email}")
            return True

        except Exception as e:
            logger.error(f"Error sending daily digest email: {e}")
            return False


# Global email service instance
email_service = EmailService()
