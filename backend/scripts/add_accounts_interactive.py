#!/usr/bin/env python3
"""
交互式添加账号工具
逐个输入 username 和 user_id
"""
import asyncio
import httpx
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
                return True, "成功添加"
            elif response.status_code == 400:
                error = response.json()
                if "already exists" in error.get('detail', '').lower():
                    return True, "已存在（跳过）"
                else:
                    return False, error.get('detail', 'Unknown error')
            else:
                return False, f"HTTP {response.status_code}"
    except Exception as e:
        return False, str(e)


async def check_api_server():
    """检查 API 服务器是否运行"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/api/health")
            return response.status_code == 200
    except:
        return False


async def get_accounts_count():
    """获取当前监控账号总数"""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/api/accounts")
            return len(response.json())
    except:
        return None


async def main():
    """主函数"""
    print("\n" + "="*80)
    print("交互式添加 Twitter 账号")
    print("="*80 + "\n")

    # 检查 API 服务器
    if not await check_api_server():
        print("❌ 错误: API 服务器未运行!")
        print("\n请先启动服务器:")
        print("  cd /Users/pingxn7/Desktop/x/backend")
        print("  ./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000")
        return

    print("✓ API 服务器运行中\n")

    # 显示当前账号数
    count = await get_accounts_count()
    if count is not None:
        print(f"当前监控账号数: {count}\n")

    print("使用说明:")
    print("  1. 访问 https://tweeterid.com/ 获取 user_id")
    print("  2. 输入 username 和 user_id")
    print("  3. 输入 'q' 或 'quit' 退出")
    print("  4. 输入 'skip' 跳过当前账号")
    print("\n" + "="*80 + "\n")

    added = 0
    skipped = 0
    errors = 0

    while True:
        try:
            # 输入 username
            print("请输入 username (不带@)，或输入 'q' 退出:")
            username = input("Username: ").strip()

            if username.lower() in ['q', 'quit', 'exit']:
                break

            if username.lower() == 'skip':
                continue

            if not username:
                print("❌ Username 不能为空\n")
                continue

            # 移除可能的 @ 符号
            username = username.lstrip('@')

            # 输入 user_id
            print(f"\n请输入 @{username} 的 user_id:")
            print(f"  提示: 访问 https://tweeterid.com/ 输入 '{username}' 获取")
            user_id = input("User ID: ").strip()

            if user_id.lower() in ['q', 'quit', 'exit']:
                break

            if user_id.lower() == 'skip':
                skipped += 1
                print(f"⊘ 跳过 @{username}\n")
                continue

            if not user_id:
                print("❌ User ID 不能为空\n")
                continue

            if not user_id.isdigit():
                print("❌ User ID 必须是纯数字\n")
                continue

            # 添加账号
            print(f"\n正在添加 @{username} (ID: {user_id})...")
            success, message = await add_account(username, user_id)

            if success:
                if "已存在" in message:
                    skipped += 1
                    print(f"⊘ {message}")
                else:
                    added += 1
                    print(f"✓ {message}")
            else:
                errors += 1
                print(f"✗ 添加失败: {message}")

            print()

        except KeyboardInterrupt:
            print("\n\n中断操作")
            break
        except Exception as e:
            print(f"\n✗ 错误: {e}\n")
            errors += 1

    # 显示总结
    print("\n" + "="*80)
    print("添加总结:")
    print("="*80)
    print(f"✓ 成功添加: {added}")
    print(f"⊘ 跳过: {skipped}")
    print(f"✗ 失败: {errors}")
    print("="*80 + "\n")

    # 显示最新账号数
    count = await get_accounts_count()
    if count is not None:
        print(f"当前监控账号总数: {count}\n")

    print("下一步:")
    print("  1. 查看状态: python scripts/check_status.py")
    print("  2. 手动收集推文: python scripts/manual_collect.py")
    print("  3. 等待自动收集（每 2 小时）")
    print()


if __name__ == "__main__":
    asyncio.run(main())
