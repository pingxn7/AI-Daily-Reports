#!/usr/bin/env python3
"""
使用官方 Twitter API 批量添加新账号
"""
import asyncio
import httpx
import os
from loguru import logger


# 要添加的账号列表
USERNAMES = [
    "swyx",
    "gregisenberg",
    "joshwoodward",
    "kevinweil",
    "petergyang",
    "thenanyu",
    "realmadhuguru",
    "mckaywrigley",
    "stevenbjohnson",
    "amandaaskell",
    "_catwu",
    "trq212",
    "GoogleLabs",
    "george__mack",
    "raizamrtn",
    "amasad",
    "rauchg",
    "rileybrown",
    "alexalbert__",
    "hamelhusain",
    "levie",
    "garrytan",
    "lulumeservey",
    "venturetwins",
    "attturck",
    "joulee",
    "PJaccetturo",
    "zarazhangrui",
]


async def fetch_users_batch(usernames: list, bearer_token: str) -> list:
    """
    使用官方 Twitter API v2 批量获取用户信息

    API 文档: https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by
    """
    try:
        usernames_str = ",".join(usernames)

        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }

        params = {
            "usernames": usernames_str,
            "user.fields": "id,name,username"
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://api.twitter.com/2/users/by",
                headers=headers,
                params=params
            )

            if response.status_code == 200:
                data = response.json()
                users = data.get("data", [])
                errors = data.get("errors", [])

                if errors:
                    logger.warning(f"API 返回了一些错误:")
                    for error in errors:
                        logger.warning(f"  - {error.get('title')}: {error.get('detail')}")

                return users
            elif response.status_code == 401:
                logger.error("认证失败！请检查 Bearer Token 是否正确")
                logger.error(f"响应: {response.text}")
                return []
            elif response.status_code == 429:
                logger.error("API 请求限制！请稍后再试")
                return []
            else:
                logger.error(f"API 请求失败: {response.status_code}")
                logger.error(f"响应: {response.text}")
                return []

    except Exception as e:
        logger.error(f"请求出错: {e}")
        return []


async def add_account_to_system(username: str, user_id: str, display_name: str):
    """添加账号到系统"""
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
                return "added"
            elif response.status_code == 400:
                error = response.json()
                if "already exists" in error.get('detail', '').lower():
                    return "exists"
                else:
                    logger.warning(f"✗ {error.get('detail', 'Unknown error')}")
                    return "error"
            else:
                logger.error(f"✗ 添加 @{username} 失败: {response.status_code}")
                return "error"
    except Exception as e:
        logger.error(f"✗ 添加 @{username} 出错: {e}")
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
    print("使用官方 Twitter API 批量添加账号")
    print("="*80 + "\n")

    # 从环境变量读取 Bearer Token
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

    if not bearer_token:
        print("❌ 错误: 未找到 TWITTER_BEARER_TOKEN 环境变量")
        print("\n请设置环境变量:")
        print("  export TWITTER_BEARER_TOKEN='your-bearer-token-here'")
        print("\n或者添加到 .env 文件:")
        print("  echo 'TWITTER_BEARER_TOKEN=your-bearer-token-here' >> .env")
        return

    # 检查 API 服务器
    if not await check_api_server():
        print("❌ 错误: API 服务器未运行!")
        print("\n请先启动服务器:")
        print("  cd /Users/pingxn7/Desktop/x/backend")
        print("  ./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return

    print("✓ API 服务器运行中")
    print(f"✓ Bearer Token 已配置 (长度: {len(bearer_token)})")
    print(f"✓ 准备添加 {len(USERNAMES)} 个账号\n")
    print("="*80 + "\n")

    # 批量获取用户信息（Twitter API v2 支持一次查询最多100个用户）
    batch_size = 100
    all_users = []

    for i in range(0, len(USERNAMES), batch_size):
        batch = USERNAMES[i:i + batch_size]
        print(f"正在从 Twitter API 获取第 {i+1}-{min(i+batch_size, len(USERNAMES))} 个账号信息...")

        users = await fetch_users_batch(batch, bearer_token)
        all_users.extend(users)

        # API 限流保护
        if i + batch_size < len(USERNAMES):
            await asyncio.sleep(1)

    print("\n" + "="*80)
    print("获取结果:")
    print("="*80)
    print(f"✓ 成功获取: {len(all_users)}/{len(USERNAMES)}\n")

    if all_users:
        print("获取到的用户信息:")
        print("-" * 80)
        for user in all_users:
            print(f"@{user['username']:<25} ID: {user['id']:<20} {user['name']}")
        print()

        # 添加到系统
        print("="*80)
        print("正在添加账号到监控系统...")
        print("="*80 + "\n")

        added = 0
        exists = 0
        errors = 0

        added_list = []
        exists_list = []
        errors_list = []

        for user in all_users:
            result = await add_account_to_system(
                user['username'],
                user['id'],
                user['name']
            )

            if result == "added":
                added += 1
                added_list.append(user['username'])
                print(f"  ✓ 成功添加 @{user['username']}")
            elif result == "exists":
                exists += 1
                exists_list.append(user['username'])
                print(f"  ⊘ 已存在 @{user['username']}")
            else:
                errors += 1
                errors_list.append(user['username'])
                print(f"  ✗ 添加失败 @{user['username']}")

            await asyncio.sleep(0.3)

        print("\n" + "="*80)
        print("添加结果:")
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
                accounts = response.json()
                print("="*80)
                print(f"当前监控账号总数: {len(accounts)}")
                print("="*80 + "\n")
        except:
            pass

    # 显示未找到的账号
    found_usernames = {user['username'] for user in all_users}
    not_found = [u for u in USERNAMES if u not in found_usernames]

    if not_found:
        print("未找到的账号（可能用户名不存在或已更改）:")
        for username in not_found:
            print(f"  ✗ @{username}")
        print()

    print("下一步:")
    print("  1. 查看状态: python scripts/check_status.py")
    print("  2. 手动收集推文: python scripts/manual_collect.py")
    print("  3. 等待下次自动收集（每 2 小时）")
    print()


if __name__ == "__main__":
    asyncio.run(main())
