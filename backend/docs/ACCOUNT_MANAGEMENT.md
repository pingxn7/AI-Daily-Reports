# Twitter 账号监听系统 - 完整指南

## 系统概述

该系统已经配置了账号管理 API，可以方便地添加、删除和管理需要监听的 Twitter 账号。

## 当前已监听的账号（14个）

✓ @elonmusk - Elon Musk
✓ @ylecun - Yann LeCun
✓ @AndrewYNg - Andrew Ng
✓ @OpenAI - OpenAI
✓ @AnthropicAI - Anthropic
✓ @sama - Sam Altman
✓ @karpathy - Andrej Karpathy
✓ @demishassabis - Demis Hassabis
✓ @goodfellow_ian - Ian Goodfellow
✓ @fchollet - François Chollet
✓ @GoogleAI - Google AI
✓ @DeepMind - Google DeepMind
✓ @hardmaru - hardmaru
✓ @arankomatsuzaki - Aran Komatsuzaki

## 待添加的账号（24个）

以下是您提供的账号列表，需要获取它们的 Twitter User ID：

1. @aidangomez - Aidan Gomez (Cohere CEO)
2. @DarioAmodei - Dario Amodei (Anthropic CEO)
3. @EpochAIResearch - Epoch AI Research
4. @drfeifei - Fei-Fei Li
5. @geoffreyhinton - Geoffrey Hinton
6. @gdb - Greg Brockman (OpenAI)
7. @ilyasut - Ilya Sutskever
8. @indigox - Indigo
9. @jackclarkSF - Jack Clark (Anthropic)
10. @JeffDean - Jeff Dean (Google)
11. @johnschulman2 - John Schulman (OpenAI)
12. @mustafasuleyman - Mustafa Suleyman (Microsoft AI)
13. @NoamShazeer - Noam Shazeer (Character.AI)
14. @OriolVinyalsML - Oriol Vinyals (Google DeepMind)
15. @pabbeel - Pieter Abbeel (UC Berkeley)
16. @rasbt - Sebastian Raschka
17. @SebastienBubeck - Sebastien Bubeck (Microsoft)
18. @soumithchintala - Soumith Chintala (Meta)
19. @woj_zaremba - Wojciech Zaremba (OpenAI)
20. @Yoshua_Bengio - Yoshua Bengio
21. @zephyr_z9 - Zephyr
22. @_jasonwei - Jason Wei (OpenAI)
23. @lennysan - Lenny
24. @thinkymachines - Thinky Machines

## 如何获取 Twitter User ID

由于 Twitter API 限制，需要手动获取用户 ID。推荐以下方法：

### 方法 1: 使用 TweeterID.com（最简单）

1. 访问 https://tweeterid.com/
2. 输入 Twitter 用户名（如 `karpathy`，不需要 @ 符号）
3. 点击 "Convert"
4. 复制显示的数字 ID

### 方法 2: 使用浏览器开发者工具

1. 访问用户的 Twitter 主页（如 https://twitter.com/karpathy）
2. 打开浏览器开发者工具（F12）
3. 在 Network 标签中查找 API 请求
4. 在响应中搜索 "rest_id" 或 "id_str"

### 方法 3: 使用第三方工具

- https://www.twitterid.net/
- https://codeofaninja.com/tools/find-twitter-id/

## 添加账号的三种方法

### 方法 1: 使用便捷脚本（推荐）

```bash
cd backend
source venv/bin/activate

# 确保 API 服务器正在运行
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# 添加单个账号
./scripts/add_account.sh karpathy 17919972 "Andrej Karpathy"
```

### 方法 2: 批量导入 JSON 文件

1. 编辑 `backend/scripts/accounts_to_add.json`，将 "TODO" 替换为实际的 user_id

2. 运行导入脚本：
```bash
cd backend
source venv/bin/activate
python scripts/import_accounts.py scripts/accounts_to_add.json
```

### 方法 3: 直接使用 API

```bash
# 添加单个账号
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "17919972",
    "username": "karpathy",
    "display_name": "Andrej Karpathy",
    "is_active": true
  }'
```

## 管理账号

### 查看所有账号
```bash
curl http://localhost:8000/api/accounts | python3 -m json.tool
```

### 查看活跃账号
```bash
curl "http://localhost:8000/api/accounts?is_active=true" | python3 -m json.tool
```

### 禁用账号
```bash
curl -X PUT http://localhost:8000/api/accounts/41 \
  -H "Content-Type: application/json" \
  -d '{"is_active": false}'
```

### 删除账号
```bash
curl -X DELETE http://localhost:8000/api/accounts/41
```

## API 文档

启动服务器后，访问以下地址查看完整的 API 文档：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 下一步操作

1. **获取 User IDs**: 访问 https://tweeterid.com/ 获取所有待添加账号的 user_id

2. **更新 JSON 文件**: 编辑 `backend/scripts/accounts_to_add.json`，填入获取的 user_id

3. **批量导入**: 运行导入脚本添加所有账号
   ```bash
   cd backend
   source venv/bin/activate
   python scripts/import_accounts.py scripts/accounts_to_add.json
   ```

4. **验证**: 检查账号是否成功添加
   ```bash
   python scripts/import_accounts.py --list
   ```

5. **开始收集**: 系统会自动按照配置的时间表（每2小时）收集这些账号的推文

## 故障排除

### API 服务器未运行
```bash
cd backend
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 查看服务器日志
服务器日志会显示所有 API 请求和错误信息

### 数据库连接问题
确保 PostgreSQL 正在运行：
```bash
psql -U pingxn7 -d ai_news -c "SELECT COUNT(*) FROM monitored_accounts;"
```

## 自动化收集

系统已配置自动任务：
- **推文收集**: 每2小时运行一次（0 */2 * * *）
- **每日摘要**: 每天早上8点运行（0 8 * * *）

可以在 `.env` 文件中修改这些时间表：
```
SCHEDULE_TWEET_COLLECTION_CRON=0 */2 * * *
SCHEDULE_DAILY_SUMMARY_CRON=0 8 * * *
```
