#!/usr/bin/env python3
"""
批量添加剩余的 27 个账号
"""
import asyncio
import httpx

USERNAMES = [
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

async def add_account(username: str):
    """添加单个账号"""
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "http://localhost:8000/api/accounts",
                json={"username": username}
            )

            if response.status_code == 201:
                data = response.json()
                return "added", data
            elif response.status_code == 400:
                error = response.json()
                if "already exists" in error.get('detail', '').lower():
                    return "exists", None
                else:
                    return "error", error.get('detail')
            else:
                return "error", f"HTTP {response.status_code}"
    except Exception as e:
        return "error", str(e)

async def main():
    print("\n" + "="*80)
    print("批量添加 27 个账号")
    print("="*80 + "\n")

    added = []
    exists = []
    errors = []

    for i, username in enumerate(USERNAMES, 1):
        print(f"[{i}/{len(USERNAMES)}] 正在添加 @{username}...", end=" ")

        status, data = await add_account(username)

        if status == "added":
            added.append(username)
            print(f"✓ 成功 (ID: {data['user_id']})")
        elif status == "exists":
            exists.append(username)
            print("⊘ 已存在")
        else:
            errors.append((username, data))
            print(f"✗ 失败: {data}")

        await asyncio.sleep(0.5)

    print("\n" + "="*80)
    print("添加结果:")
    print("="*80)
    print(f"✓ 成功添加: {len(added)}")
    print(f"⊘ 已存在: {len(exists)}")
    print(f"✗ 失败: {len(errors)}")
    print("="*80 + "\n")

    if added:
        print("成功添加的账号:")
        for username in added:
            print(f"  ✓ @{username}")
        print()

    if errors:
        print("添加失败的账号:")
        for username, error in errors:
            print(f"  ✗ @{username}: {error}")
        print()

    # 显示总数
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("http://localhost:8000/api/accounts")
            accounts = response.json()
            print("="*80)
            print(f"当前监控账号总数: {len(accounts)}")
            print("="*80 + "\n")
    except:
        pass

if __name__ == "__main__":
    asyncio.run(main())
