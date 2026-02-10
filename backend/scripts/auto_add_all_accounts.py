#!/usr/bin/env python3
"""
使用 twitterapi.io 自动获取 user_id 并添加账号
"""
import asyncio
import httpx
from loguru import logger


# 需要添加的 21 个账号
ACCOUNTS_TO_ADD = [
    {"username": "aidangomez", "display_name": "Aidan Gomez"},
    {"username": "EpochAIResearch", "display_name": "Epoch AI Research"},
    {"username": "drfeifei", "display_name": "Fei-Fei Li"},
    {"username": "geoffreyhinton", "display_name": "Geoffrey Hinton"},
    {"username": "gdb", "display_name": "Greg Brockman"},
    {"username": "indigox", "display_name": "Indigo"},
    {"username": "jackclarkSF", "display_name": "Jack Clark"},
    {"username": "johnschulman2", "display_name": "John Schulman"},
    {"username": "mustafasuleyman", "display_name": "Mustafa Suleyman"},
    {"username": "NoamShazeer", "display_name": "Noam Shazeer"},
    {"username": "OriolVinyalsML", "display_name": "Oriol Vinyals"},
    {"username": "pabbeel", "display_name": "Pieter Abbeel"},
    {"username": "rasbt", "display_name": "Sebastian Raschka"},
    {"username": "SebastienBubeck", "display_name": "Sebastien Bubeck"},
    {"username": "soumithchintala", "display_name": "Soumith Chintala"},
    {"username": "woj_zaremba", "display_name": "Wojciech Zaremba"},
    {"username": "Yoshua_Bengio", "display_name": "Yoshua Bengio"},
    {"username": "zephyr_z9", "display_name": "Zephyr"},
    {"username": "_jasonwei", "display_name": "Jason Wei"},
    {"username": "lennysan", "display_name": "Lenny"},
    {"username": "thinkymachines", "display_name": "Thinky Machines"},
]

API_KEY = "new1_7590bc837c4d4104ada0ef3419ab7d6c"


async def fetch_user_id_from_api(username: str) -> dict:
    """
    使用 twitterapi.io 获取用户信息

    Args:
        username: Twitter username

    Returns:
        包含 user_id, username, display_name 的字典，失败返回 None
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"https://api.twitterapi.io/twitter/user/last_tweets?userName={username}",
                headers={"x-api-key": API_KEY}
            )

            if response.status_code == 200:
                data = response.json()

                if data.get("status") == "success":
                    tweets = data.get("data", {}).get("tweets", [])

                    if tweets and len(tweets) > 0:
                        author = tweets[0].get("author", {})

                        return {
                            "user_id": author.get("id"),
                            "username": author.get("userName"),
                            "display_name": author.get("name"),
                        }
                    else:
                        logger.warning(f"@{username}: 没有找到推文数据")
                        return None
                else:
                    logger.error(f"@{username}: API 返回错误 - {data.get('msg')}")
                    return None
            else:
                logger.error(f"@{username}: HTTP {response.status_code}")
                return None

    except Exception as e:
        logger.error(f"@{username}: 请求出错 - {e}")
        return None


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
                    logger.warning(f"✗ @{username}: {error.get('detail')}")
                    return "error"
            else:
                logger.error(f"✗ @{username}: HTTP {response.status_code}")
                return "error"
    except Exception as e:
        logger.error(f"✗ @{username}: {e}")
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
    print("🚀 自动获取 User IDs 并添加账号")
    print("="*80 + "\n")

    # 检查 API 服务器
    if not await check_api_server():
        print("❌ 错误: API 服务器未运行!")
        print("\n请先启动服务器:")
        print("  cd /Users/pingxn7/Desktop/x/backend")
        print("  source venv/bin/activate")
        print("  python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return

    print("✓ API 服务器运行中")
    print(f"✓ 准备添加 {len(ACCOUNTS_TO_ADD)} 个账号\n")
    print("="*80 + "\n")

    added_count = 0
    exists_count = 0
    failed_count = 0

    results = []

    for i, account in enumerate(ACCOUNTS_TO_ADD, 1):
        username = account["username"]
        display_name = account["display_name"]

        print(f"[{i}/{len(ACCOUNTS_TO_ADD)}] 正在处理 @{username}...")

        # 获取 user_id
        user_info = await fetch_user_id_from_api(username)

        if user_info:
            user_id = user_info["user_id"]
            actual_username = user_info["username"]
            actual_display_name = user_info["display_name"]

            print(f"  ✓ 获取到 user_id: {user_id}")

            # 添加到系统
            result = await add_account_to_system(
                actual_username,
                user_id,
                actual_display_name
            )

            if result == "added":
                added_count += 1
                results.append({
                    "username": actual_username,
                    "user_id": user_id,
                    "display_name": actual_display_name,
                    "status": "added"
                })
            elif result == "exists":
                exists_count += 1
                results.append({
                    "username": actual_username,
                    "user_id": user_id,
                    "display_name": actual_display_name,
                    "status": "exists"
                })
            else:
                failed_count += 1
                results.append({
                    "username": username,
                    "status": "failed_to_add"
                })
        else:
            print(f"  ✗ 无法获取 user_id")
            failed_count += 1
            results.append({
                "username": username,
                "status": "failed_to_fetch"
            })

        # 避免请求过快
        await asyncio.sleep(1)
        print()

    # 显示结果
    print("="*80)
    print("完成！")
    print("="*80)
    print(f"✓ 成功添加: {added_count} 个")
    print(f"⊘ 已存在: {exists_count} 个")
    print(f"✗ 失败: {failed_count} 个")
    print("="*80 + "\n")

    # 显示成功添加的账号
    if added_count > 0:
        print("成功添加的账号:")
        for r in results:
            if r.get("status") == "added":
                print(f"  ✓ @{r['username']} (ID: {r['user_id']}) - {r['display_name']}")
        print()

    # 显示已存在的账号
    if exists_count > 0:
        print("已存在的账号:")
        for r in results:
            if r.get("status") == "exists":
                print(f"  ⊘ @{r['username']}")
        print()

    # 显示失败的账号
    if failed_count > 0:
        print("失败的账号:")
        for r in results:
            if r.get("status") in ["failed_to_fetch", "failed_to_add"]:
                print(f"  ✗ @{r['username']}")
        print()

    # 显示当前监听的账号总数
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8000/api/accounts")
            accounts = response.json()
            print("="*80)
            print(f"当前监听账号总数: {len(accounts)} 个")
            print("="*80 + "\n")
    except:
        pass

    print("🎉 完成！您的系统现在正在监听所有添加的账号。")
    print()


if __name__ == "__main__":
    asyncio.run(main())
