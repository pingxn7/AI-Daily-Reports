#!/usr/bin/env python3
"""
批量添加账号 - 从用户提供的 user_id 列表
"""
import asyncio
import httpx
from loguru import logger
import sys


async def add_account(username: str, user_id: str, display_name: str = None):
    """添加账号到系统"""
    if not display_name:
        display_name = username

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "http://localhost:8000/api/accounts",
                json={
                    "user_id": user_id,
                    "username": username,
                    "display_name": display_name,
                    "is_active": True
                }
            )

            if response.status_code == 201:
                print(f"✓ 成功添加 @{username}")
                return True
            elif response.status_code == 400:
                error = response.json()
                if "already exists" in error.get('detail', '').lower():
                    print(f"⊘ @{username} 已存在")
                    return True
                else:
                    print(f"✗ @{username}: {error.get('detail', 'Unknown error')}")
                    return False
            else:
                print(f"✗ 添加 @{username} 失败: {response.status_code}")
                return False
    except Exception as e:
        print(f"✗ 添加 @{username} 出错: {e}")
        return False


async def main():
    """批量添加账号"""
    if len(sys.argv) < 2:
        print("用法: python scripts/batch_add.py username1:user_id1 username2:user_id2 ...")
        print("示例: python scripts/batch_add.py geoffreyhinton:123456789 Yoshua_Bengio:987654321")
        return

    accounts = []
    for arg in sys.argv[1:]:
        if ':' in arg:
            username, user_id = arg.split(':', 1)
            accounts.append({'username': username, 'user_id': user_id})

    if not accounts:
        print("❌ 没有有效的账号信息")
        return

    print(f"\n准备添加 {len(accounts)} 个账号...\n")

    added = 0
    for account in accounts:
        success = await add_account(account['username'], account['user_id'])
        if success:
            added += 1
        await asyncio.sleep(0.3)

    print(f"\n完成！成功添加 {added}/{len(accounts)} 个账号\n")

    # 显示当前监听的账号总数
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8000/api/accounts")
            all_accounts = response.json()
            print(f"当前监听账号总数: {len(all_accounts)} 个\n")
    except:
        pass


if __name__ == "__main__":
    asyncio.run(main())
