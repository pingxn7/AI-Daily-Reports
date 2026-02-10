#!/usr/bin/env python3
"""
快速测试定时任务功能
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.tasks.scheduler import start_scheduler, stop_scheduler, get_scheduler_status
from loguru import logger


async def test_scheduler():
    """测试调度器启动和状态"""
    print("\n" + "="*80)
    print("定时任务功能测试")
    print("="*80 + "\n")

    try:
        # 启动调度器
        print("1. 启动调度器...")
        start_scheduler()
        print("   ✓ 调度器启动成功\n")

        # 等待一下让调度器初始化
        await asyncio.sleep(1)

        # 获取状态
        print("2. 获取调度器状态...")
        status = get_scheduler_status()
        print(f"   运行状态: {'运行中' if status['running'] else '已停止'}")
        print(f"   任务数量: {len(status['jobs'])}\n")

        # 显示任务详情
        print("3. 任务详情:")
        print("   " + "-"*76)
        for job in status['jobs']:
            print(f"   任务ID: {job['id']}")
            print(f"   名称: {job['name']}")
            print(f"   下次运行: {job['next_run']}")
            print(f"   触发器: {job['trigger']}")
            print("   " + "-"*76)

        print("\n✅ 测试完成！\n")

        # 停止调度器
        print("4. 停止调度器...")
        stop_scheduler()
        print("   ✓ 调度器已停止\n")

    except Exception as e:
        print(f"\n❌ 错误: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_scheduler())
