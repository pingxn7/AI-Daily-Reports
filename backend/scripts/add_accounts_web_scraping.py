#!/usr/bin/env python3
"""
通过网页抓取获取 Twitter user IDs
"""
import httpx
import asyncio
import re
from loguru import logger


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


async def fetch_user_id_from_web(username: str) -> tuple:
    """
    从 Twitter 个人主页抓取 user ID
    返回: (user_id, display_name) 或 (None, None)
    """
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(
                f"https://twitter.com/{username}",
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                }
            )

            if response.status_code == 200:
                content = response.text

                # 查找 user ID
                user_id = None
                match = re.search(r'"userId":"(\d+)"', content)
                if match:
                    user_id = match.group(1)
                else:
                    match = re.search(r'"rest_id":"(\d+)"', content)
                    if match:
                        user_id = match.group(1)

                # 查找 display name
                display_name = None
                match = re.search(r'<title>([^(]+)\s*\(@' + username + r'\)', content)
                if match:
                    display_name = match.group(1).strip()

                return (user_id, display_name)
            else:
                logger.error(f"无法访问 @{username} 的主页: {response.status_code}")
                return (None, None)

    except Exception as e:
        logger.error(f"抓取 @{username} 出错: {e}")
        return (None, None)


async def add_account_to_system(username: str, user_id: str, display_name: str):
    """添加账号到系统"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                "http://localhost:8000/api/accounts",
                json={
                    "user_id": user_id,
                    "username": username,
                    "display_name": display_name or username,
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
                    return "error"
            else:
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
    print("通过网页抓取批量添加 Twitter 账号")
    print("="*80 + "\n")

    # 检查 API 服务器
    if not await check_api_server():
        print("❌ 错误: API 服务器未运行!")
        print("\n请先启动服务器:")
        print("  cd /Users/pingxn7/Desktop/x/backend")
        print("  ./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return

    print("✓ API 服务器运行中")
    print(f"✓ 准备添加 {len(USERNAMES)} 个账号")
    print("\n注意: 网页抓取可能受到 Twitter 反爬虫限制")
    print("如果失败，可以访问 https://tweeterid.com/ 手动查找 user ID\n")
    print("="*80 + "\n")

    results = {}
    found_count = 0

    for i, username in enumerate(USERNAMES, 1):
        print(f"[{i}/{len(USERNAMES)}] 正在获取 @{username}...")

        user_id, display_name = await fetch_user_id_from_web(username)

        if user_id:
            results[username] = {
                "user_id": user_id,
                "display_name": display_name or username,
                "status": "found"
            }
            found_count += 1
            print(f"  ✓ 找到: ID={user_id}, 名称={display_name}")
        else:
            results[username] = {
                "user_id": None,
                "display_name": None,
                "status": "not_found"
            }
            print(f"  ✗ 未找到")

        # 避免请求过快
        await asyncio.sleep(2)

    print("\n" + "="*80)
    print("获取结果:")
    print("="*80)
    print(f"✓ 成功获取: {found_count}/{len(USERNAMES)}\n")

    if found_count > 0:
        print("="*80)
        print("正在添加账号到监控系统...")
        print("="*80 + "\n")

        added = 0
        exists = 0
        errors = 0

        added_list = []
        exists_list = []

        for username, data in results.items():
            if data["status"] == "found":
                result = await add_account_to_system(
                    username,
                    data["user_id"],
                    data["display_name"]
                )

                if result == "added":
                    added += 1
                    added_list.append(username)
                    print(f"  ✓ 成功添加 @{username}")
                elif result == "exists":
                    exists += 1
                    exists_list.append(username)
                    print(f"  ⊘ 已存在 @{username}")
                else:
                    errors += 1
                    print(f"  ✗ 添加失败 @{username}")

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
    not_found = [u for u, d in results.items() if d["status"] == "not_found"]

    if not_found:
        print("未找到的账号（需要手动查找）:")
        print("-" * 80)
        for username in not_found:
            print(f"  ✗ @{username}")
            print(f"     手动查找: https://tweeterid.com/")
            print(f"     或访问: https://twitter.com/{username}")
        print()

    print("下一步:")
    print("  1. 查看状态: python scripts/check_status.py")
    print("  2. 手动收集推文: python scripts/manual_collect.py")
    print("  3. 等待下次自动收集（每 2 小时）")
    print()


if __name__ == "__main__":
    asyncio.run(main())
