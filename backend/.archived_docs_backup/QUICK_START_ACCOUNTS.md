# 快速开始：添加 Twitter 监听账号

## 当前状态

✅ 账号管理 API 已创建并运行
✅ 当前监听 14 个默认账号
✅ 待添加 24 个新账号

## 最简单的添加方法

### 步骤 1: 启动 API 服务器（如果未运行）

```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 步骤 2: 使用交互式工具添加账号

在新终端窗口中：

```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python scripts/add_accounts_interactive.py
```

这个工具会：
- 显示当前监听的账号
- 列出待添加的 24 个账号
- 引导您逐个添加账号

### 步骤 3: 获取 Twitter User ID

对于每个账号：
1. 访问 https://tweeterid.com/
2. 输入用户名（如 `DarioAmodei`）
3. 复制显示的数字 ID
4. 粘贴到交互式工具中

## 快速添加单个账号

如果您已经知道 user_id：

```bash
cd /Users/pingxn7/Desktop/x/backend
./scripts/add_account.sh <username> <user_id> "<display_name>"

# 例如：
./scripts/add_account.sh DarioAmodei 123456789 "Dario Amodei"
```

## 批量添加账号

1. 编辑 `backend/scripts/accounts_to_add.json`
2. 将所有 "TODO" 替换为实际的 user_id
3. 运行：

```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python scripts/import_accounts.py scripts/accounts_to_add.json
```

## 待添加的 24 个账号

| # | Username | Display Name | User ID |
|---|----------|--------------|---------|
| 1 | @aidangomez | Aidan Gomez | 需要获取 |
| 2 | @DarioAmodei | Dario Amodei | 需要获取 |
| 3 | @EpochAIResearch | Epoch AI Research | 需要获取 |
| 4 | @drfeifei | Fei-Fei Li | 需要获取 |
| 5 | @geoffreyhinton | Geoffrey Hinton | 需要获取 |
| 6 | @gdb | Greg Brockman | 需要获取 |
| 7 | @ilyasut | Ilya Sutskever | 需要获取 |
| 8 | @indigox | Indigo | 需要获取 |
| 9 | @jackclarkSF | Jack Clark | 需要获取 |
| 10 | @JeffDean | Jeff Dean | 需要获取 |
| 11 | @johnschulman2 | John Schulman | 需要获取 |
| 12 | @mustafasuleyman | Mustafa Suleyman | 需要获取 |
| 13 | @NoamShazeer | Noam Shazeer | 需要获取 |
| 14 | @OriolVinyalsML | Oriol Vinyals | 需要获取 |
| 15 | @pabbeel | Pieter Abbeel | 需要获取 |
| 16 | @rasbt | Sebastian Raschka | 需要获取 |
| 17 | @SebastienBubeck | Sebastien Bubeck | 需要获取 |
| 18 | @soumithchintala | Soumith Chintala | 需要获取 |
| 19 | @woj_zaremba | Wojciech Zaremba | 需要获取 |
| 20 | @Yoshua_Bengio | Yoshua Bengio | 需要获取 |
| 21 | @zephyr_z9 | Zephyr | 需要获取 |
| 22 | @_jasonwei | Jason Wei | 需要获取 |
| 23 | @lennysan | Lenny | 需要获取 |
| 24 | @thinkymachines | Thinky Machines | 需要获取 |

## 查看当前监听的账号

```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python scripts/add_accounts_interactive.py --list
```

或使用 API：

```bash
curl http://localhost:8000/api/accounts | python3 -m json.tool
```

## API 文档

访问 http://localhost:8000/docs 查看完整的 API 文档

## 常用命令

```bash
# 查看所有账号
curl http://localhost:8000/api/accounts | python3 -m json.tool

# 查看活跃账号
curl "http://localhost:8000/api/accounts?is_active=true" | python3 -m json.tool

# 添加账号
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"user_id": "123456", "username": "example", "display_name": "Example User", "is_active": true}'

# 禁用账号（ID 为 41）
curl -X PUT http://localhost:8000/api/accounts/41 \
  -H "Content-Type: application/json" \
  -d '{"is_active": false}'

# 删除账号（ID 为 41）
curl -X DELETE http://localhost:8000/api/accounts/41
```

## 自动收集推文

系统已配置自动任务：
- **推文收集**: 每 2 小时运行一次
- **每日摘要**: 每天早上 8 点运行

添加账号后，系统会自动开始收集这些账号的推文。

## 需要帮助？

查看详细文档：
- `backend/docs/ACCOUNT_MANAGEMENT.md` - 完整的账号管理指南
- `backend/docs/ADD_ACCOUNTS.md` - 添加账号详细说明
- http://localhost:8000/docs - API 文档
