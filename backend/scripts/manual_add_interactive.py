#!/usr/bin/env python3
"""
手动添加账号 - 交互式脚本
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


async def add_account(username: str, user_id: str, display_name: str):
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
                return True
            elif response.status_code == 400:
                error = response.json()
                if "already exists" in error.get('detail', '').lower():
                    logger.info(f"⊘ @{username} 已存在")
                    return True
                else:
                    logger.error(f"✗ {error.get('detail', 'Unknown error')}")
                    return False
            else:
                logger.error(f"✗ 添加 @{username} 失败: {response.status_code}")
                return False
    except Exception as e:
        logger.error(f"✗ 添加 @{username} 出错: {e}")
        return False


async def main():
    """交互式添加账号"""
    print("\n" + "="*80)
    print("手动添加 Twitter 账号 - 交互式模式")
    print("="*80 + "\n")

    print(f"需要添加 {len(ACCOUNTS_TO_ADD)} 个账号\n")
    print("请按照以下步骤操作：")
    print("1. 访问 https://tweeterid.com/")
    print("2. 输入 username 查询 user_id")
    print("3. 将 user_id 粘贴到这里\n")
    print("="*80 + "\n")

    added_count = 0
    skipped_count = 0

    for i, account in enumerate(ACCOUNTS_TO_ADD, 1):
        username = account["username"]
        display_name = account["display_name"]

        print(f"\n[{i}/{len(ACCOUNTS_TO_ADD)}] @{username} - {display_name}")
        print("-" * 80)

        # 提示用户输入 user_id
        user_id = input(f"请输入 @{username} 的 user_id (输入 's' 跳过, 'q' 退出): ").strip()

        if user_id.lower() == 'q':
            print("\n用户取消操作")
            break
        elif user_id.lower() == 's':
            print(f"跳过 @{username}")
            skipped_count += 1
            continue
        elif not user_id or not user_id.isdigit():
            print(f"⚠️  无效的 user_id，跳过 @{username}")
            skipped_count += 1
            continue

        # 添加账号
        success = await add_account(username, user_id, display_name)
        if success:
            added_count += 1
        else:
            skipped_count += 1

    print("\n" + "="*80)
    print("完成！")
    print("="*80)
    print(f"✓ 成功添加: {added_count} 个")
    print(f"⊘ 跳过: {skipped_count} 个")
    print("="*80 + "\n")

    # 显示当前监听的账号总数
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8000/api/accounts")
            accounts = response.json()
            print(f"当前监听账号总数: {len(accounts)} 个\n")
    except:
        pass


if __name__ == "__main__":
    asyncio.run(main())
