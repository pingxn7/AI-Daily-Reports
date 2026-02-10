#!/usr/bin/env python3
"""
批量添加新账号到监控列表
"""
import asyncio
import httpx
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


async def check_api_server():
    """检查 API 服务是否运行"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/api/health")
            return response.status_code == 200
    except:
        return False


async def add_accounts_batch(usernames: list):
    """批量添加账号（只需要 username，系统会自动获取 user_id）"""
    try:
        accounts = [{"username": username} for username in usernames]

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "http://localhost:8000/api/accounts/batch",
                json=accounts
            )

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"添加账号失败: {response.status_code}")
                logger.error(response.text)
                return None
    except Exception as e:
        logger.error(f"添加账号出错: {e}")
        return None


async def list_accounts():
    """列出所有监控账号"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8000/api/accounts")
            return response.json()
    except:
        return []


async def main():
    """批量添加账号"""
    print("\n" + "="*80)
    print("批量添加 Twitter 账号到监控列表")
    print("="*80 + "\n")

    # 检查 API 服务是否运行
    if not await check_api_server():
        print("❌ 错误: API 服务未运行!")
        print("\n请先启动服务:")
        print("  cd /Users/pingxn7/Desktop/x/backend")
        print("  ./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return

    print("✓ API 服务运行中\n")
    print(f"准备添加 {len(USERNAMES)} 个账号...\n")
    print("系统将自动:")
    print("  1. 从 Twitter API 获取 user_id")
    print("  2. 从 Twitter API 获取 display_name")
    print("  3. 添加账号到监控列表\n")
    print("="*80 + "\n")

    # 批量添加账号
    result = await add_accounts_batch(USERNAMES)

    if result:
        print("\n" + "="*80)
        print("添加结果:")
        print("="*80)
        print(f"✓ 成功添加: {result['added']}")
        print(f"⊘ 跳过（已存在）: {result['skipped']}")
        print(f"✗ 错误: {result['errors']}")
        print("="*80 + "\n")

        if result['details']['added']:
            print("成功添加的账号:")
            for username in result['details']['added']:
                print(f"  ✓ @{username}")
            print()

        if result['details']['skipped']:
            print("跳过的账号（已存在）:")
            for item in result['details']['skipped']:
                print(f"  ⊘ @{item['username']}: {item['reason']}")
            print()

        if result['details']['errors']:
            print("添加失败的账号:")
            for item in result['details']['errors']:
                print(f"  ✗ @{item['username']}: {item['error']}")
            print()

        # 显示当前监控的账号总数
        accounts = await list_accounts()
        print("="*80)
        print(f"当前监控账号总数: {len(accounts)}")
        print("="*80 + "\n")

        print("下一步:")
        print("  1. 查看状态: python scripts/check_status.py")
        print("  2. 手动收集推文: python scripts/manual_collect.py")
        print("  3. 等待下次自动收集（每 2 小时）")
        print()
    else:
        print("❌ 添加账号失败。请查看上面的日志了解详情。")


if __name__ == "__main__":
    asyncio.run(main())
