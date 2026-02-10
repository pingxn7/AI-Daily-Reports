#!/usr/bin/env python3
"""
使用官方 Twitter/X API v2 获取 user IDs
需要 X Developer Bearer Token
"""
import asyncio
import httpx
import json
from pathlib import Path
from loguru import logger
import os


# 需要获取 user_id 的账号列表
USERNAMES = [
    "aidangomez",
    "EpochAIResearch",
    "drfeifei",
    "geoffreyhinton",
    "gdb",
    "indigox",
    "jackclarkSF",
    "johnschulman2",
    "mustafasuleyman",
    "NoamShazeer",
    "OriolVinyalsML",
    "pabbeel",
    "rasbt",
    "SebastienBubeck",
    "soumithchintala",
    "woj_zaremba",
    "Yoshua_Bengio",
    "zephyr_z9",
    "_jasonwei",
    "lennysan",
    "thinkymachines",
]


async def fetch_users_batch(usernames: list, bearer_token: str) -> list:
    """
    使用官方 Twitter API v2 批量获取用户信息

    API 文档: https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users-by

    Args:
        usernames: 用户名列表（最多100个）
        bearer_token: Twitter Bearer Token

    Returns:
        用户信息列表
    """
    try:
        # 构建查询参数
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
                logger.info(f"✓ 成功添加 @{username}")
                return "added"
            elif response.status_code == 400:
                error = response.json()
                if "already exists" in error.get('detail', '').lower():
                    logger.info(f"⊘ @{username} 已存在")
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
    print("使用官方 X Developer API 获取 User IDs")
    print("="*80 + "\n")

    # 从环境变量或配置文件读取 Bearer Token
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

    if not bearer_token:
        print("❌ 错误: 未找到 TWITTER_BEARER_TOKEN 环境变量")
        print("\n请按以下步骤操作:")
        print("\n1. 申请 X Developer 账号:")
        print("   访问: https://developer.twitter.com/")
        print("   点击 'Sign up' 或 'Apply for access'")
        print("\n2. 创建项目和应用:")
        print("   - 登录后进入 Developer Portal")
        print("   - 创建一个新项目 (Project)")
        print("   - 在项目下创建一个应用 (App)")
        print("\n3. 获取 Bearer Token:")
        print("   - 进入应用设置")
        print("   - 找到 'Keys and tokens' 标签")
        print("   - 生成 'Bearer Token'")
        print("   - 复制 Bearer Token")
        print("\n4. 设置环境变量:")
        print("   export TWITTER_BEARER_TOKEN='your-bearer-token-here'")
        print("\n5. 或者添加到 .env 文件:")
        print("   echo 'TWITTER_BEARER_TOKEN=your-bearer-token-here' >> .env")
        print("\n然后重新运行此脚本")
        print("="*80 + "\n")
        return

    print(f"✓ 找到 Bearer Token (长度: {len(bearer_token)})")
    print(f"✓ 准备获取 {len(USERNAMES)} 个账号的信息\n")

    # 批量获取用户信息（Twitter API v2 支持一次查询最多100个用户）
    batch_size = 100
    all_users = []

    for i in range(0, len(USERNAMES), batch_size):
        batch = USERNAMES[i:i + batch_size]
        logger.info(f"正在获取第 {i+1}-{min(i+batch_size, len(USERNAMES))} 个账号...")

        users = await fetch_users_batch(batch, bearer_token)
        all_users.extend(users)

        # API 限流保护
        if i + batch_size < len(USERNAMES):
            await asyncio.sleep(1)

    print("\n" + "="*80)
    print("获取结果:")
    print("="*80 + "\n")

    print(f"✓ 成功获取: {len(all_users)}/{len(USERNAMES)}")

    if all_users:
        print("\n获取到的用户信息:")
        print("-" * 80)
        for user in all_users:
            print(f"{user['username']:<25} {user['id']:<20} {user['name']}")
        print()

        # 保存到文件
        output_txt = Path("scripts/user_ids_official.txt")
        with open(output_txt, 'w', encoding='utf-8') as f:
            for user in all_users:
                f.write(f"{user['username']} {user['id']}\n")
        print(f"✓ 已保存到 {output_txt}")

        output_json = Path("scripts/user_ids_official.json")
        with open(output_json, 'w', encoding='utf-8') as f:
            json.dump(all_users, f, indent=2, ensure_ascii=False)
        print(f"✓ 已保存到 {output_json}")
        print()

        # 询问是否立即添加到系统
        print("="*80)
        print("是否立即添加这些账号到监听系统？")
        print("="*80)

        # 检查 API 服务器
        if not await check_api_server():
            print("\n⚠️  API 服务器未运行，无法自动添加")
            print("请先启动服务器:")
            print("  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
            print("\n然后运行:")
            print("  python scripts/add_from_txt.py")
            return

        print("\n正在添加账号到系统...\n")

        added = 0
        exists = 0
        errors = 0

        for user in all_users:
            result = await add_account_to_system(
                user['username'],
                user['id'],
                user['name']
            )

            if result == "added":
                added += 1
            elif result == "exists":
                exists += 1
            else:
                errors += 1

            await asyncio.sleep(0.3)

        print("\n" + "="*80)
        print("添加结果:")
        print("="*80)
        print(f"✓ 新添加: {added}")
        print(f"⊘ 已存在: {exists}")
        print(f"✗ 失败: {errors}")
        print("="*80 + "\n")

        # 显示当前监听的账号总数
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get("http://localhost:8000/api/accounts")
                accounts = response.json()
                print(f"当前监听账号总数: {len(accounts)}\n")
        except:
            pass

    # 显示未找到的账号
    found_usernames = {user['username'] for user in all_users}
    not_found = [u for u in USERNAMES if u not in found_usernames]

    if not_found:
        print("未找到的账号:")
        for username in not_found:
            print(f"  ✗ @{username}")
        print()


if __name__ == "__main__":
    asyncio.run(main())
