# 完整使用流程 - 添加 Twitter 账号到监听系统

## 📋 概述

本指南将帮助您完成从申请 X Developer API 到添加所有账号的完整流程。

## 🎯 目标

添加 21 个 AI 领域重要账号到监听系统：
- aidangomez, EpochAIResearch, drfeifei, geoffreyhinton, gdb, indigox, jackclarkSF, johnschulman2, mustafasuleyman, NoamShazeer, OriolVinyalsML, pabbeel, rasbt, SebastienBubeck, soumithchintala, woj_zaremba, Yoshua_Bengio, zephyr_z9, _jasonwei, lennysan, thinkymachines

## 📝 完整步骤

### 步骤 1: 申请 X Developer API（10-15 分钟）

1. **访问 X Developer Portal**
   ```
   https://developer.twitter.com/
   ```

2. **申请开发者账号**
   - 点击 "Sign up" 或 "Apply for access"
   - 使用您的 Twitter 账号登录
   - 填写申请表单（选择 "Hobbyist" 或 "Academic"）
   - 说明用途: "Monitor AI researchers' tweets for personal news aggregation"

3. **创建项目和应用**
   - 项目名称: "AI News Collector"
   - 应用名称: "ai-news-monitor"

4. **获取 Bearer Token**
   - 进入应用设置 → "Keys and tokens"
   - 点击 "Generate" 生成 Bearer Token
   - **立即复制保存**（只显示一次！）

📖 **详细指南**: 查看 `HOW_TO_APPLY_X_API.md`

### 步骤 2: 配置 Bearer Token（1 分钟）

**方法 A: 添加到 .env 文件（推荐）**

```bash
cd /Users/pingxn7/Desktop/x/backend
echo 'TWITTER_BEARER_TOKEN=你的Bearer-Token' >> .env
```

**方法 B: 设置环境变量**

```bash
export TWITTER_BEARER_TOKEN='你的Bearer-Token'
```

### 步骤 3: 测试 Bearer Token（30 秒）

```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python scripts/test_bearer_token.py
```

**预期输出:**
```
✅ Bearer Token 有效！

测试查询结果:
  用户名: @elonmusk
  显示名: Elon Musk
  User ID: 44196397

✓ 您可以开始使用官方 API 获取账号信息了！
```

### 步骤 4: 获取所有账号的 User IDs（1 分钟）

```bash
python scripts/fetch_with_official_api.py
```

**脚本会自动:**
1. ✅ 使用官方 API 批量获取 21 个账号的 user_id
2. ✅ 保存结果到 `scripts/user_ids_official.txt` 和 `scripts/user_ids_official.json`
3. ✅ 自动添加所有账号到监听系统

**预期输出:**
```
================================================================================
使用官方 X Developer API 获取 User IDs
================================================================================

✓ 找到 Bearer Token (长度: 110)
✓ 准备获取 21 个账号的信息

正在获取第 1-21 个账号...

================================================================================
获取结果:
================================================================================

✓ 成功获取: 21/21

获取到的用户信息:
--------------------------------------------------------------------------------
aidangomez                123456789            Aidan Gomez
geoffreyhinton            987654321            Geoffrey Hinton
...

✓ 已保存到 scripts/user_ids_official.txt
✓ 已保存到 scripts/user_ids_official.json

正在添加账号到系统...

================================================================================
添加结果:
================================================================================
✓ 新添加: 21
⊘ 已存在: 0
✗ 失败: 0
================================================================================

当前监听账号总数: 28
```

### 步骤 5: 验证结果（30 秒）

```bash
# 查看所有监听的账号
curl http://localhost:8000/api/accounts | jq

# 或使用脚本
./scripts/check_status.sh
```

## ✅ 完成！

现在您的系统正在监听 28 个 AI 领域的重要账号：

**已添加的账号（28个）:**
- 7 个之前已添加
- 21 个刚刚通过官方 API 添加

**系统功能:**
- ✅ 每 2 小时自动收集推文
- ✅ 使用 Claude 分析 AI 相关性
- ✅ 计算重要性评分
- ✅ 生成每日摘要

## 🔧 故障排除

### 问题 1: Bearer Token 测试失败

**错误**: `❌ Bearer Token 无效或已过期`

**解决方法:**
1. 检查 Token 是否完整复制（没有多余空格）
2. 在 Developer Portal 重新生成 Token
3. 确保 Token 格式正确（通常以 'AAAAAAAAAA' 开头）

### 问题 2: API 请求限制

**错误**: `⚠️ API 请求限制`

**解决方法:**
- 等待 15 分钟后重试
- 免费层级限制: 300 次/15分钟

### 问题 3: 某些账号未找到

**可能原因:**
- 账号名拼写错误
- 账号已被删除或暂停
- 账号设置为私密

**解决方法:**
- 检查账号名是否正确
- 在 Twitter 上手动搜索确认账号存在
- 使用 tweeterid.com 手动查询

### 问题 4: API 服务器未运行

**错误**: `⚠️ API 服务器未运行，无法自动添加`

**解决方法:**
```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 📚 相关文件

- `HOW_TO_APPLY_X_API.md` - X Developer API 申请详细指南
- `scripts/test_bearer_token.py` - Bearer Token 测试工具
- `scripts/fetch_with_official_api.py` - 获取 user_id 并添加账号
- `scripts/user_ids_official.txt` - 获取到的 user_id 列表
- `scripts/user_ids_official.json` - 获取到的完整用户信息

## 🎉 下一步

系统已经配置完成，您可以：

1. **查看收集的推文**
   ```bash
   curl http://localhost:8000/api/tweets | jq
   ```

2. **查看每日摘要**
   ```bash
   curl http://localhost:8000/api/summaries | jq
   ```

3. **访问 API 文档**
   ```
   http://localhost:8000/docs
   ```

4. **等待自动收集**
   - 系统每 2 小时自动收集一次推文
   - 每天早上 8 点生成摘要

## 💡 提示

- Bearer Token 是敏感信息，不要分享或提交到 Git
- 免费 API 限制足够个人使用
- 如需更多账号，可以随时添加
- 定期检查系统状态: `./scripts/check_status.sh`

需要帮助？查看其他文档或检查日志文件。
