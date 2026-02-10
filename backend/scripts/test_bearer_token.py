#!/usr/bin/env python3
"""
测试 Twitter Bearer Token 是否有效
"""
import asyncio
import httpx
import os
from loguru import logger


async def test_bearer_token(bearer_token: str):
    """测试 Bearer Token"""
    try:
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json"
        }

        # 测试查询一个已知存在的用户
        params = {
            "usernames": "elonmusk",
            "user.fields": "id,name,username"
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                "https://api.twitter.com/2/users/by",
                headers=headers,
                params=params
            )

            print("\n" + "="*80)
            print("Bearer Token 测试结果")
            print("="*80 + "\n")

            if response.status_code == 200:
                data = response.json()
                users = data.get("data", [])

                if users:
                    user = users[0]
                    print("✅ Bearer Token 有效！")
                    print(f"\n测试查询结果:")
                    print(f"  用户名: @{user['username']}")
                    print(f"  显示名: {user['name']}")
                    print(f"  User ID: {user['id']}")
                    print("\n✓ 您可以开始使用官方 API 获取账号信息了！")
                    print("\n下一步:")
                    print("  python scripts/fetch_with_official_api.py")
                    return True
                else:
                    print("⚠️  API 响应成功但未返回数据")
                    print(f"响应: {data}")
                    return False

            elif response.status_code == 401:
                print("❌ Bearer Token 无效或已过期")
                print("\n可能的原因:")
                print("  1. Token 复制错误（检查是否有多余空格）")
                print("  2. Token 已被撤销")
                print("  3. Token 格式不正确")
                print("\n解决方法:")
                print("  1. 重新检查 Token 是否完整复制")
                print("  2. 在 Developer Portal 重新生成 Token")
                print("  3. 确保 Token 以 'AAAAAAAAAA' 开头")
                print(f"\n详细错误: {response.text}")
                return False

            elif response.status_code == 403:
                print("❌ 权限不足")
                print("\n可能的原因:")
                print("  1. 应用权限设置不正确")
                print("  2. 账号被限制")
                print("\n解决方法:")
                print("  1. 检查应用的权限设置")
                print("  2. 确保应用有读取权限")
                print(f"\n详细错误: {response.text}")
                return False

            elif response.status_code == 429:
                print("⚠️  API 请求限制")
                print("请稍后再试（15分钟后）")
                return False

            else:
                print(f"❌ API 请求失败: HTTP {response.status_code}")
                print(f"\n响应内容: {response.text}")
                return False

    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False


async def main():
    """主函数"""
    print("\n" + "="*80)
    print("Twitter/X Bearer Token 测试工具")
    print("="*80 + "\n")

    # 从环境变量读取
    bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

    if not bearer_token:
        print("❌ 未找到 TWITTER_BEARER_TOKEN 环境变量")
        print("\n请按以下方式设置:")
        print("\n方法 1: 临时设置（当前终端）")
        print("  export TWITTER_BEARER_TOKEN='your-token-here'")
        print("\n方法 2: 添加到 .env 文件")
        print("  echo 'TWITTER_BEARER_TOKEN=your-token-here' >> .env")
        print("\n方法 3: 添加到 shell 配置文件")
        print("  echo 'export TWITTER_BEARER_TOKEN=\"your-token-here\"' >> ~/.zshrc")
        print("  source ~/.zshrc")
        print("\n获取 Bearer Token:")
        print("  1. 访问 https://developer.twitter.com/en/portal/dashboard")
        print("  2. 进入您的应用")
        print("  3. 点击 'Keys and tokens' 标签")
        print("  4. 生成或查看 Bearer Token")
        print("\n详细指南: 查看 HOW_TO_APPLY_X_API.md")
        print("="*80 + "\n")
        return

    print(f"✓ 找到 Bearer Token")
    print(f"  长度: {len(bearer_token)} 字符")
    print(f"  前缀: {bearer_token[:20]}...")
    print(f"\n正在测试...\n")

    success = await test_bearer_token(bearer_token)

    print("\n" + "="*80 + "\n")

    if not success:
        print("需要帮助？")
        print("  1. 查看详细指南: cat HOW_TO_APPLY_X_API.md")
        print("  2. 检查 Token 格式")
        print("  3. 重新生成 Token")


if __name__ == "__main__":
    asyncio.run(main())
