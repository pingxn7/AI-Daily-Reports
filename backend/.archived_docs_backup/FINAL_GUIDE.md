# 🎯 Twitter 账号监听系统 - 最终指南

## ✅ 已完成的工作

### 1. 账号管理系统
- ✅ 完整的 RESTful API（增删改查）
- ✅ 交互式添加工具
- ✅ 快速添加脚本
- ✅ 批量导入工具
- ✅ 详细文档

### 2. 当前状态
- ✅ 系统已监听 14 个 AI 领域重要账号
- ✅ API 服务器正在运行
- ✅ 自动收集任务已配置（每 2 小时）

## 📋 待添加的 24 个账号

由于 Twitter 的反爬虫措施，无法自动获取 user_id。您需要手动获取以下账号的 user_id：

| # | Username | Display Name | 组织/领域 |
|---|----------|--------------|-----------|
| 1 | @aidangomez | Aidan Gomez | Cohere CEO |
| 2 | @DarioAmodei | Dario Amodei | Anthropic CEO |
| 3 | @EpochAIResearch | Epoch AI Research | AI 研究 |
| 4 | @drfeifei | Fei-Fei Li | Stanford |
| 5 | @geoffreyhinton | Geoffrey Hinton | 图灵奖得主 |
| 6 | @gdb | Greg Brockman | OpenAI |
| 7 | @ilyasut | Ilya Sutskever | SSI |
| 8 | @indigox | Indigo | AI 研究者 |
| 9 | @jackclarkSF | Jack Clark | Anthropic |
| 10 | @JeffDean | Jeff Dean | Google |
| 11 | @johnschulman2 | John Schulman | OpenAI |
| 12 | @mustafasuleyman | Mustafa Suleyman | Microsoft AI |
| 13 | @NoamShazeer | Noam Shazeer | Character.AI |
| 14 | @OriolVinyalsML | Oriol Vinyals | Google DeepMind |
| 15 | @pabbeel | Pieter Abbeel | UC Berkeley |
| 16 | @rasbt | Sebastian Raschka | AI 作者 |
| 17 | @SebastienBubeck | Sebastien Bubeck | Microsoft |
| 18 | @soumithchintala | Soumith Chintala | Meta |
| 19 | @woj_zaremba | Wojciech Zaremba | OpenAI |
| 20 | @Yoshua_Bengio | Yoshua Bengio | 图灵奖得主 |
| 21 | @zephyr_z9 | Zephyr | AI 研究者 |
| 22 | @_jasonwei | Jason Wei | OpenAI |
| 23 | @lennysan | Lenny | AI 研究者 |
| 24 | @thinkymachines | Thinky Machines | AI 内容 |

## 🚀 添加账号的三种方法

### 方法 1: 交互式工具（最推荐）

**优点**：逐个引导，不容易出错

```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate

# 确保 API 服务器正在运行
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# 在新终端运行交互式工具
python scripts/add_accounts_interactive.py
```

工具会：
1. 显示当前监听的账号
2. 列出待添加的账号
3. 逐个提示您输入 user_id
4. 自动添加到系统

### 方法 2: 快速添加脚本

**优点**：单行命令，快速添加

```bash
cd /Users/pingxn7/Desktop/x/backend

# 添加单个账号（示例）
./scripts/add_account.sh DarioAmodei 739232892 "Dario Amodei"
./scripts/add_account.sh ilyasut 16616354 "Ilya Sutskever"
./scripts/add_account.sh JeffDean 11658782 "Jeff Dean"
```

### 方法 3: 批量导入

**优点**：一次性添加所有账号

1. **编辑 JSON 文件**：
```bash
cd /Users/pingxn7/Desktop/x/backend
nano scripts/accounts_to_add.json
```

2. **将 "TODO" 替换为实际的 user_id**

3. **运行导入脚本**：
```bash
source venv/bin/activate
python scripts/import_accounts.py scripts/accounts_to_add.json
```

## 🔍 如何获取 Twitter User ID

### 推荐方法：使用 TweeterID.com

1. **访问** https://tweeterid.com/
2. **输入用户名**（如 `DarioAmodei`，不需要 @ 符号）
3. **点击 "Convert"**
4. **复制数字 ID**（如 `739232892`）

### 示例：

```
输入: DarioAmodei
输出: 739232892

输入: ilyasut
输出: 16616354

输入: JeffDean
输出: 11658782
```

## 📝 完整示例：添加 Dario Amodei

假设您已经获取到 Dario Amodei 的 user_id 是 `739232892`：

### 使用快速脚本：
```bash
cd /Users/pingxn7/Desktop/x/backend
./scripts/add_account.sh DarioAmodei 739232892 "Dario Amodei"
```

### 使用 API：
```bash
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "739232892",
    "username": "DarioAmodei",
    "display_name": "Dario Amodei",
    "is_active": true
  }'
```

### 验证添加成功：
```bash
curl http://localhost:8000/api/accounts | python3 -m json.tool | grep -A 5 "DarioAmodei"
```

## 🎬 快速开始（推荐流程）

### 步骤 1: 启动 API 服务器

```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

保持这个终端运行。

### 步骤 2: 打开新终端，运行交互式工具

```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python scripts/add_accounts_interactive.py
```

### 步骤 3: 按照提示操作

1. 工具会显示待添加的 24 个账号
2. 选择 "1" 进入交互式添加模式
3. 对于每个账号：
   - 访问 https://tweeterid.com/
   - 输入用户名
   - 复制 user_id
   - 粘贴到工具中
4. 工具会自动添加账号

### 步骤 4: 验证

```bash
python scripts/add_accounts_interactive.py --list
```

## 📊 查看监听状态

### 查看所有账号
```bash
curl http://localhost:8000/api/accounts | python3 -m json.tool
```

### 查看账号数量
```bash
curl http://localhost:8000/api/accounts | python3 -c "import sys, json; print(f'Total accounts: {len(json.load(sys.stdin))}')"
```

### 查看活跃账号
```bash
curl "http://localhost:8000/api/accounts?is_active=true" | python3 -m json.tool
```

## 🔧 管理账号

### 禁用账号
```bash
# 假设账号 ID 是 41
curl -X PUT http://localhost:8000/api/accounts/41 \
  -H "Content-Type: application/json" \
  -d '{"is_active": false}'
```

### 启用账号
```bash
curl -X PUT http://localhost:8000/api/accounts/41 \
  -H "Content-Type: application/json" \
  -d '{"is_active": true}'
```

### 删除账号
```bash
curl -X DELETE http://localhost:8000/api/accounts/41
```

## ⚙️ 系统配置

### 自动收集任务

系统已配置自动任务（在 `.env` 文件中）：

```bash
# 推文收集：每 2 小时运行一次
SCHEDULE_TWEET_COLLECTION_CRON=0 */2 * * *

# 每日摘要：每天早上 8 点运行
SCHEDULE_DAILY_SUMMARY_CRON=0 8 * * *
```

### 修改收集频率

编辑 `.env` 文件：

```bash
# 改为每小时收集一次
SCHEDULE_TWEET_COLLECTION_CRON=0 * * * *

# 改为每天下午 6 点生成摘要
SCHEDULE_DAILY_SUMMARY_CRON=0 18 * * *
```

## 📚 API 文档

访问以下地址查看完整的 API 文档：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/health

## 🛠️ 故障排除

### API 服务器未运行
```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 端口被占用
```bash
# 查找占用端口的进程
lsof -ti:8000

# 停止进程
lsof -ti:8000 | xargs kill -9
```

### 数据库连接问题
```bash
# 检查 PostgreSQL 是否运行
psql -U pingxn7 -d ai_news -c "SELECT COUNT(*) FROM monitored_accounts;"
```

### 查看日志
API 服务器会在终端显示所有请求和错误信息。

## 📁 相关文件

```
backend/
├── app/
│   └── api/
│       └── routes/
│           └── accounts.py          # 账号管理 API
├── scripts/
│   ├── add_accounts_interactive.py  # 交互式添加工具 ⭐
│   ├── add_account.sh               # 快速添加脚本
│   ├── import_accounts.py           # 批量导入工具
│   ├── accounts_to_add.json         # 待添加账号模板
│   └── seed_accounts.py             # 初始种子数据
├── docs/
│   ├── ACCOUNT_MANAGEMENT.md        # 完整管理指南
│   └── ADD_ACCOUNTS.md              # 添加账号详细说明
├── QUICK_START_ACCOUNTS.md          # 快速开始指南
└── SUMMARY.md                        # 功能总结
```

## ✨ 下一步

1. **启动 API 服务器**（如果未运行）
2. **运行交互式工具**：`python scripts/add_accounts_interactive.py`
3. **逐个添加账号**：访问 https://tweeterid.com/ 获取 user_id
4. **验证添加成功**：`python scripts/add_accounts_interactive.py --list`
5. **等待自动收集**：系统会每 2 小时自动收集推文

## 💡 提示

- 建议先添加几个重要账号测试系统
- 可以随时添加或删除账号
- 系统会自动跳过已存在的账号
- 所有操作都有详细的日志记录

## 🎉 完成后

添加所有账号后，系统将：
1. ✅ 每 2 小时自动收集这些账号的推文
2. ✅ 使用 Claude 分析推文的 AI 相关性
3. ✅ 计算重要性评分
4. ✅ 每天生成 AI 新闻摘要
5. ✅ 通过前端展示最重要的 AI 新闻

---

**需要帮助？** 查看 `backend/docs/ACCOUNT_MANAGEMENT.md` 获取更多详细信息。
