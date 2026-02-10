#!/usr/bin/env python3
"""
从文本文件导入账号
文件格式: username user_id (每行一个账号)
例如: swyx 1234567890
"""
import asyncio
import httpx
from pathlib import Path
from loguru import logger


async def add_account(username: str, user_id: str):
    """添加单个账号到系统"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "http://localhost:8000/api/accounts",
                json={
                    "user_id": user_id,
                    "username": username,
                    "display_name": username,
                    "is_active": True
                }
            )

            if response.status_code == 201:
                return "added"
            elif response.status_code == 400:
                error = response.json()
                if "already exists" in error.get('detail', '').lower():
                    return "exists"
                else:
                    logger.warning(f"错误: {error.get('detail', 'Unknown error')}")
                    return "error"
            else:
                logger.error(f"添加失败: {response.status_code}")
                return "error"
    except Exception as e:
        logger.error(f"添加 @{username} 出错: {e}")
        return "error"


async def check_api_server():
    """检查 API 服务器是否运行"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/api/health")
            return response.status_code == 200
    except:
        return False


async def main():
    """主函数"""
    print("\n" + "="*80)
    print("从文件导入 Twitter 账号")
    print("="*80 + "\n")

    # 检查 API 服务器
    if not await check_api_server():
        print("❌ 错误: API 服务器未运行!")
        print("\n请先启动服务器:")
        print("  cd /Users/pingxn7/Desktop/x/backend")
        print("  ./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return

    print("✓ API 服务器运行中\n")

    # 读取文件
    input_file = Path("scripts/user_ids_to_import.txt")

    if not input_file.exists():
        print(f"❌ 错误: 文件不存在: {input_file}")
        print("\n请创建文件 scripts/user_ids_to_import.txt")
        print("文件格式（每行一个账号）:")
        print("  username user_id")
        print("\n例如:")
        print("  swyx 1234567890")
        print("  karpathy 9876543210")
        print("\n如何获取 user_id:")
        print("  1. 访问 https://tweeterid.com/")
        print("  2. 输入 username")
        print("  3. 复制 user_id")
        print("  4. 粘贴到文件中")
        return

    # 解析文件
    accounts = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split()
            if len(parts) >= 2:
                username = parts[0]
                user_id = parts[1]
                accounts.append((username, user_id))
            else:
                logger.warning(f"第 {line_num} 行格式错误，已跳过: {line}")

    if not accounts:
        print("❌ 错误: 文件中没有有效的账号数据")
        return

    print(f"✓ 从文件中读取到 {len(accounts)} 个账号\n")
    print("="*80)
    print("正在添加账号...")
    print("="*80 + "\n")

    added = 0
    exists = 0
    errors = 0

    added_list = []
    exists_list = []
    errors_list = []

    for username, user_id in accounts:
        result = await add_account(username, user_id)

        if result == "added":
            added += 1
            added_list.append(username)
            print(f"  ✓ 成功添加 @{username} (ID: {user_id})")
        elif result == "exists":
            exists += 1
            exists_list.append(username)
            print(f"  ⊘ 已存在 @{username}")
        else:
            errors += 1
            errors_list.append(username)
            print(f"  ✗ 添加失败 @{username}")

        await asyncio.sleep(0.3)

    print("\n" + "="*80)
    print("导入结果:")
    print("="*80)
    print(f"✓ 新添加: {added}")
    print(f"⊘ 已存在: {exists}")
    print(f"✗ 失败: {errors}")
    print("="*80 + "\n")

    if added_list:
        print("成功添加的账号:")
        for username in added_list:
            print(f"  ✓ @{username}")
        print()

    # 显示当前监听的账号总数
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8000/api/accounts")
            accounts_list = response.json()
            print("="*80)
            print(f"当前监控账号总数: {len(accounts_list)}")
            print("="*80 + "\n")
    except:
        pass

    print("下一步:")
    print("  1. 查看状态: python scripts/check_status.py")
    print("  2. 手动收集推文: python scripts/manual_collect.py")
    print("  3. 等待下次自动收集（每 2 小时）")
    print()


if __name__ == "__main__":
    asyncio.run(main())
