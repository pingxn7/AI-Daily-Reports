#!/usr/bin/env python3
"""
手动添加账号 - 只需提供 username，user_id 可选
如果不提供 user_id，请访问 https://tweeterid.com/ 手动查找
"""
import asyncio
import httpx
from loguru import logger


# 要添加的账号列表
# 格式: {"username": "user_id"} 或 {"username": None}（稍后手动填写）
ACCOUNTS = {
    "swyx": None,
    "gregisenberg": None,
    "joshwoodward": None,
    "kevinweil": None,
    "petergyang": None,
    "thenanyu": None,
    "realmadhuguru": None,
    "mckaywrigley": None,
    "stevenbjohnson": None,
    "amandaaskell": None,
    "_catwu": None,
    "trq212": None,
    "GoogleLabs": None,
    "george__mack": None,
    "raizamrtn": None,
    "amasad": None,
    "rauchg": None,
    "rileybrown": None,
    "alexalbert__": None,
    "hamelhusain": None,
    "levie": None,
    "garrytan": None,
    "lulumeservey": None,
    "venturetwins": None,
    "attturck": None,
    "joulee": None,
    "PJaccetturo": None,
    "zarazhangrui": None,
}


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
    print("手动批量添加 Twitter 账号")
    print("="*80 + "\n")

    # 检查 API 服务器
    if not await check_api_server():
        print("❌ 错误: API 服务器未运行!")
        print("\n请先启动服务器:")
        print("  cd /Users/pingxn7/Desktop/x/backend")
        print("  ./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return

    print("✓ API 服务器运行中\n")

    # 统计需要查找 user_id 的账号
    need_user_id = [u for u, uid in ACCOUNTS.items() if uid is None]

    if need_user_id:
        print("="*80)
        print(f"需要手动查找 {len(need_user_id)} 个账号的 user_id")
        print("="*80 + "\n")
        print("请访问以下网站查找 user_id:")
        print("  • https://tweeterid.com/")
        print("  • https://www.tweetbinder.com/blog/twitter-id/")
        print("\n或者使用浏览器开发者工具:")
        print("  1. 访问 https://twitter.com/username")
        print("  2. 打开开发者工具 (F12)")
        print("  3. 在 Network 标签中查找包含 user_id 的请求\n")

        print("需要查找的账号:")
        print("-" * 80)
        for username in need_user_id:
            print(f"  @{username}")
        print()

        print("找到 user_id 后，请编辑此脚本文件:")
        print(f"  {__file__}")
        print("\n将 ACCOUNTS 字典中的 None 替换为对应的 user_id")
        print("例如: \"swyx\": \"1234567890\"")
        print("\n然后重新运行此脚本")
        print("="*80 + "\n")

        # 询问是否继续添加已有 user_id 的账号
        has_user_id = [u for u, uid in ACCOUNTS.items() if uid is not None]
        if has_user_id:
            print(f"发现 {len(has_user_id)} 个账号已有 user_id，是否先添加这些账号？")
            print("按 Enter 继续，或 Ctrl+C 取消...")
            try:
                input()
            except KeyboardInterrupt:
                print("\n已取消")
                return
        else:
            print("所有账号都需要 user_id，请先查找后再运行此脚本")
            return

    # 添加已有 user_id 的账号
    to_add = [(u, uid) for u, uid in ACCOUNTS.items() if uid is not None]

    if not to_add:
        print("没有可添加的账号")
        return

    print("\n" + "="*80)
    print(f"正在添加 {len(to_add)} 个账号...")
    print("="*80 + "\n")

    added = 0
    exists = 0
    errors = 0

    added_list = []
    exists_list = []
    errors_list = []

    for username, user_id in to_add:
        result = await add_account(username, user_id)

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
            errors_list.append(username)
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

    print("下一步:")
    print("  1. 查看状态: python scripts/check_status.py")
    print("  2. 手动收集推文: python scripts/manual_collect.py")
    print("  3. 等待下次自动收集（每 2 小时）")
    print()


if __name__ == "__main__":
    asyncio.run(main())
