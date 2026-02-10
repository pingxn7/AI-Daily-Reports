# 添加 Twitter 监听账号指南

## 当前监听的账号

系统已经配置了以下默认账号：
- Elon Musk (@elonmusk)
- Yann LeCun (@ylecun)
- Andrew Ng (@AndrewYNg)
- OpenAI (@OpenAI)
- Anthropic (@AnthropicAI)
- Sam Altman (@sama)
- Andrej Karpathy (@karpathy)
- Demis Hassabis (@demishassabis)
- Ian Goodfellow (@goodfellow_ian)
- François Chollet (@fchollet)
- Google AI (@GoogleAI)
- DeepMind (@DeepMind)
- hardmaru (@hardmaru)
- Aran Komatsuzaki (@arankomatsuzaki)

## 如何添加新的监听账号

### 方法 1: 使用 API（推荐）

1. **获取 Twitter User ID**

   由于 Twitter API 限制，需要手动获取用户的 Twitter ID。有以下几种方法：

   - 访问 https://tweeterid.com/ 输入用户名（如 @karpathy）获取 ID
   - 使用浏览器开发者工具查看 Twitter 页面源代码
   - 使用第三方工具如 https://www.twitterid.net/

2. **编辑 JSON 文件**

   编辑 `backend/scripts/accounts_to_add.json` 文件，将 "TODO" 替换为实际的 user_id：

   ```json
   {
     "user_id": "17919972",
     "username": "karpathy",
     "display_name": "Andrej Karpathy"
   }
   ```

3. **启动 API 服务器**

   ```bash
   cd backend
   source venv/bin/activate
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

4. **导入账号**

   ```bash
   cd backend
   source venv/bin/activate
   python scripts/import_accounts.py scripts/accounts_to_add.json
   ```

### 方法 2: 使用 API 端点

如果服务器正在运行，可以直接使用 API：

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

# 批量添加账号
curl -X POST http://localhost:8000/api/accounts/batch \
  -H "Content-Type: application/json" \
  -d '[
    {
      "user_id": "17919972",
      "username": "karpathy",
      "display_name": "Andrej Karpathy",
      "is_active": true
    }
  ]'
```

### 方法 3: 直接修改数据库

```bash
cd backend
source venv/bin/activate
python scripts/add_new_accounts.py
```

## 管理账号的 API 端点

- `GET /api/accounts` - 列出所有监听账号
- `GET /api/accounts/{id}` - 获取特定账号信息
- `POST /api/accounts` - 添加新账号
- `PUT /api/accounts/{id}` - 更新账号信息
- `DELETE /api/accounts/{id}` - 删除账号
- `POST /api/accounts/batch` - 批量添加账号

## 查看当前监听的账号

```bash
# 使用脚本
cd backend
source venv/bin/activate
python scripts/import_accounts.py --list

# 或使用 curl
curl http://localhost:8000/api/accounts | python3 -m json.tool
```

## 您提供的账号列表

以下是您想要监听的账号，需要获取它们的 user_id：

1. @aidangomez - Aidan Gomez (Cohere CEO)
2. @karpathy - Andrej Karpathy (已在默认列表中)
3. @DarioAmodei - Dario Amodei (Anthropic CEO)
4. @demishassabis - Demis Hassabis (已在默认列表中)
5. @EpochAIResearch - Epoch AI Research
6. @drfeifei - Fei-Fei Li
7. @fchollet - François Chollet (已在默认列表中)
8. @geoffreyhinton - Geoffrey Hinton
9. @gdb - Greg Brockman
10. @ilyasut - Ilya Sutskever
11. @indigox - Indigo
12. @jackclarkSF - Jack Clark
13. @JeffDean - Jeff Dean
14. @johnschulman2 - John Schulman
15. @mustafasuleyman - Mustafa Suleyman
16. @NoamShazeer - Noam Shazeer
17. @OriolVinyalsML - Oriol Vinyals
18. @pabbeel - Pieter Abbeel
19. @rasbt - Sebastian Raschka
20. @SebastienBubeck - Sebastien Bubeck
21. @soumithchintala - Soumith Chintala
22. @woj_zaremba - Wojciech Zaremba
23. @Yoshua_Bengio - Yoshua Bengio
24. @zephyr_z9 - Zephyr
25. @AndrewYNg - Andrew Ng (已在默认列表中)
26. @_jasonwei - Jason Wei
27. @lennysan - Lenny
28. @thinkymachines - Thinky Machines

## 下一步

1. 访问 https://tweeterid.com/ 获取上述账号的 user_id
2. 更新 `backend/scripts/accounts_to_add.json` 文件
3. 运行导入脚本添加账号
4. 系统将自动开始收集这些账号的推文
