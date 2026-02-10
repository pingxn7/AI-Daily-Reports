#!/usr/bin/env python3
"""
手动生成 AI 行业日报
使用新的 AI Twitter Editor Agent 系统
"""
import asyncio
import sys
from pathlib import Path
from datetime import date, timedelta
from loguru import logger

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import get_db_context
from app.services.ai_report_editor import ai_report_editor


async def main():
    """Generate AI industry daily report."""
    print("\n" + "="*80)
    print("AI 行业日报生成器")
    print("="*80 + "\n")

    # Get date from command line or use yesterday
    if len(sys.argv) > 1:
        try:
            report_date = date.fromisoformat(sys.argv[1])
        except ValueError:
            print(f"❌ 错误: 无效的日期格式。请使用 YYYY-MM-DD 格式")
            print(f"   示例: python scripts/generate_daily_report.py 2026-02-08")
            return
    else:
        report_date = date.today() - timedelta(days=1)

    print(f"📅 生成日期: {report_date.strftime('%Y年%m月%d日')}\n")
    print("正在生成 AI 行业日报...\n")

    with get_db_context() as db:
        # Generate the report
        report = await ai_report_editor.generate_daily_report(db, report_date)

        if not report:
            print("❌ 错误: 没有找到相关推文数据或生成失败")
            return

        # Save to file
        output_dir = Path("reports")
        output_dir.mkdir(exist_ok=True)

        output_file = output_dir / f"ai_daily_report_{report_date.isoformat()}.md"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print("="*80)
        print("✅ 日报生成成功！")
        print("="*80)
        print(f"\n📄 报告已保存到: {output_file}")
        print(f"📊 报告长度: {len(report)} 字符\n")

        # Show preview
        print("="*80)
        print("报告预览（前 500 字符）:")
        print("="*80)
        print(report[:500])
        print("...\n")

        # Ask if user wants to update the summary
        print("="*80)
        print("是否要更新数据库中的每日摘要？")
        print("="*80)
        print("这将替换现有的简短摘要为完整的 AI 行业日报。")
        print("\n输入 'yes' 确认更新，或按 Enter 跳过:")

        try:
            response = input().strip().lower()
            if response == 'yes':
                # Find the summary for this date
                from app.models.daily_summary import DailySummary
                from sqlalchemy import func

                summary = db.query(DailySummary).filter(
                    func.date(DailySummary.date) == report_date
                ).first()

                if summary:
                    success = await ai_report_editor.update_summary_with_report(
                        db, summary.id, report
                    )
                    if success:
                        print("\n✅ 数据库已更新！")
                    else:
                        print("\n❌ 更新失败，请查看日志")
                else:
                    print(f"\n⚠️  未找到 {report_date} 的摘要记录")
                    print("请先运行 manual_summary.py 创建摘要")
        except KeyboardInterrupt:
            print("\n\n已取消")

    print("\n" + "="*80)
    print("完成！")
    print("="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
