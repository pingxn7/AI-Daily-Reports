# Twitter AI 新闻监听系统 - 账号管理

## 📊 当前状态

✅ **系统运行正常**
- 监听账号数：**17 个**
- 已收集推文：**15 条**
- AI 相关推文：**15 条** (100%)
- 下次收集时间：**2026-02-08 12:00**
- 下次摘要生成：**2026-02-09 08:00**

## 🎯 已监听的账号（17个）

### AI 公司和组织
- @OpenAI - OpenAI
- @AnthropicAI - Anthropic
- @DeepMind - Google DeepMind
- @GoogleAI - Google AI

### 公司领导者
- @sama - Sam Altman (OpenAI CEO)
- @DarioAmodei - Dario Amodei (Anthropic CEO) 🆕
- @elonmusk - Elon Musk (Tesla/xAI)

### 顶级研究者
- @ylecun - Yann LeCun (Meta, 图灵奖)
- @geoffreyhinton - ❌ 待添加
- @Yoshua_Bengio - ❌ 待添加
- @ilyasut - Ilya Sutskever (SSI) 🆕
- @JeffDean - Jeff Dean (Google) 🆕
- @karpathy - Andrej Karpathy (OpenAI)
- @AndrewYNg - Andrew Ng (DeepLearning.AI)
- @fchollet - François Chollet (Google)
- @goodfellow_ian - Ian Goodfellow (DeepMind)
- @demishassabis - Demis Hassabis (Google DeepMind)
- @hardmaru - hardmaru (Google)
- @arankomatsuzaki - Aran Komatsuzaki

## 🔴 高优先级待添加（8个）

| # | Username | Display Name | 为什么重要 | 操作 |
|---|----------|--------------|-----------|------|
| 1 | @geoffreyhinton | Geoffrey Hinton | 图灵奖得主，深度学习之父 | [获取 user_id](https://tweeterid.com/) |
| 2 | @Yoshua_Bengio | Yoshua Bengio | 图灵奖得主，深度学习先驱 | [获取 user_id](https://tweeterid.com/) |
| 3 | @aidangomez | Aidan Gomez | Cohere CEO，Transformer 作者 | [获取 user_id](https://tweeterid.com/) |
| 4 | @gdb | Greg Brockman | OpenAI 联合创始人 | [获取 user_id](https://tweeterid.com/) |
| 5 | @mustafasuleyman | Mustafa Suleyman | Microsoft AI CEO | [获取 user_id](https://tweeterid.com/) |
| 6 | @NoamShazeer | Noam Shazeer | Character.AI，Transformer 作者 | [获取 user_id](https://tweeterid.com/) |
| 7 | @jackclarkSF | Jack Clark | Anthropic 联合创始人 | [获取 user_id](https://tweeterid.com/) |
| 8 | @drfeifei | Fei-Fei Li | Stanford，ImageNet 创建者 | [获取 user_id](https://tweeterid.com/) |

## 🚀 快速添加账号

### 方法 1: 交互式工具（最简单）

```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python scripts/add_accounts_interactive.py
```

### 方法 2: 快速脚本

```bash
# 1. 访问 https://tweeterid.com/ 获取 user_id
# 2. 运行命令添加

cd /Users/pingxn7/Desktop/x/backend
./scripts/add_account.sh <username> <user_id> "<display_name>"

# 示例：
./scripts/add_account.sh geoffreyhinton 14498259 "Geoffrey Hinton"
```

### 方法 3: 使用 API

```bash
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "14498259",
    "username": "geoffreyhinton",
    "display_name": "Geoffrey Hinton",
    "is_active": true
  }'
```

## 📝 添加示例

假设您已经获取到以下 user_id：

```bash
cd /Users/pingxn7/Desktop/x/backend

# 添加 Geoffrey Hinton
./scripts/add_account.sh geoffreyhinton 14498259 "Geoffrey Hinton"

# 添加 Yoshua Bengio
./scripts/add_account.sh Yoshua_Bengio 18995815 "Yoshua Bengio"

# 添加 Aidan Gomez
./scripts/add_account.sh aidangomez 2420197951 "Aidan Gomez"

# 添加 Greg Brockman
./scripts/add_account.sh gdb 14344469 "Greg Brockman"

# 添加 Mustafa Suleyman
./scripts/add_account.sh mustafasuleyman 2841902084 "Mustafa Suleyman"
```

## 🔍 查看系统状态

```bash
# 查看所有账号
python scripts/add_accounts_interactive.py --list

# 查看系统指标
curl http://localhost:8000/api/metrics | python3 -m json.tool

# 查看系统健康状态
curl http://localhost:8000/api/health | python3 -m json.tool

# 查看 API 文档
open http://localhost:8000/docs
```

## 📚 完整文档

- **完整指南**: `COMPLETE_GUIDE.md` - 详细使用说明
- **快速开始**: `FINAL_GUIDE.md` - 快速开始指南
- **状态报告**: `STATUS_REPORT.md` - 系统状态详情
- **管理指南**: `docs/ACCOUNT_MANAGEMENT.md` - 账号管理详细说明

## ⚙️ 系统配置

```bash
# 推文收集：每 2 小时
SCHEDULE_TWEET_COLLECTION_CRON=0 */2 * * *

# 每日摘要：每天早上 8 点
SCHEDULE_DAILY_SUMMARY_CRON=0 8 * * *
```

## 🎉 系统已就绪

您的系统现在正在：
- ✅ 每 2 小时自动收集 17 个账号的推文
- ✅ 使用 Claude 分析推文的 AI 相关性
- ✅ 计算推文的重要性评分
- ✅ 每天生成 AI 新闻摘要

## 🚀 下一步

1. **添加高优先级账号**（建议至少添加前 3 个）
2. **等待自动收集**（下次收集时间：2026-02-08 12:00）
3. **查看收集结果**
4. **访问前端查看 AI 新闻摘要**

---

**需要帮助？** 运行 `python scripts/add_accounts_interactive.py` 获取交互式指导。
