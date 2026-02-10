# 📧 邮件推送时间已更新 + 📋 添加账号指南

## ✅ 已完成的配置

### 1. 邮件推送时间修改

**原配置**：
- 时间：每天 8:00 AM UTC（北京时间下午 4:00）

**新配置**：
- ⏰ **时间**：每天上午 8:00（北京时间）
- 🌍 **时区**：Asia/Shanghai
- 📅 **Cron**：`0 8 * * *`
- 📧 **收件人**：pingxn7@gmail.com

**下次邮件推送**：明天（2026-02-09）上午 8:00

**邮件内容**：
- AI 生成的关键亮点摘要
- Top 10 精选推文（带中文翻译和截图）
- 参与度指标（点赞、评论、转发）
- 完整汇总链接

---

## 📋 添加账号任务

### 当前状况

由于 Twitter API 限制，需要手动获取账号的 user_id：
- ❌ twitterapi.io API 不可用
- ❌ 官方 Twitter API 免费额度已用完（CreditsDepleted）
- ❌ 网页抓取受到反爬虫限制

### 需要添加的 28 个账号

```
swyx, gregisenberg, joshwoodward, kevinweil, petergyang,
thenanyu, realmadhuguru, mckaywrigley, stevenbjohnson,
amandaaskell, _catwu, trq212, GoogleLabs, george__mack,
raizamrtn, amasad, rauchg, rileybrown, alexalbert__,
hamelhusain, levie, garrytan, lulumeservey, venturetwins,
attturck, joulee, PJaccetturo, zarazhangrui
```

---

## 🚀 添加账号 - 三步完成

### 步骤 1: 获取 User IDs

访问 **https://tweeterid.com/**

逐个输入 username（不带 @），获取 user_id

### 步骤 2: 编辑导入文件

```bash
nano scripts/user_ids_to_import.txt
```

添加账号信息（格式：`username user_id`）：

```
swyx 33521530
gregisenberg 1234567890
joshwoodward 9876543210
...
```

### 步骤 3: 运行导入脚本

```bash
cd /Users/pingxn7/Desktop/x/backend
./venv/bin/python scripts/import_user_ids.py
```

---

## 🛠️ 可用工具

### 方法 1: 批量导入（推荐）

```bash
# 编辑文件
nano scripts/user_ids_to_import.txt

# 运行导入
./venv/bin/python scripts/import_user_ids.py
```

### 方法 2: 交互式添加

```bash
# 逐个输入 username 和 user_id
./venv/bin/python scripts/add_accounts_interactive.py
```

### 方法 3: 快速导入（带确认）

```bash
# 编辑文件后运行
./scripts/quick_import.sh
```

---

## 📚 文档和帮助

### 查看所有工具

```bash
./scripts/show_add_tools.sh
```

### 查看快速参考

```bash
cat scripts/README_ADD_ACCOUNTS.md
```

### 查看完整指南

```bash
cat scripts/QUICK_START_ADD_ACCOUNTS.md
```

### 查看详细说明

```bash
cat scripts/HOW_TO_ADD_ACCOUNTS.md
```

---

## ✅ 验证和测试

### 查看系统状态

```bash
python scripts/check_status.py
```

### 查看当前监控账号

```bash
curl http://localhost:8000/api/accounts | python3 -m json.tool
```

### 手动收集推文

```bash
python scripts/manual_collect.py
```

### 测试邮件发送

```bash
python scripts/test_email.py
```

### 查看系统指标

```bash
curl http://localhost:8000/api/metrics | python3 -m json.tool
```

---

## 📊 当前系统状态

### 监控账号数

当前：38 个账号
待添加：28 个账号
完成后：66 个账号

### 定时任务

1. **推文收集**：每 2 小时
   - 下次运行：今晚 8:00 PM

2. **邮件推送**：每天上午 8:00（北京时间）
   - 下次运行：明天上午 8:00

### 系统数据

- 总摘要数：1
- 总推文数：15
- AI 相关推文：15（100%）

---

## 💡 推荐工作流程

### 添加账号的最佳实践

1. **准备工作**
   ```bash
   # 打开两个窗口
   # 窗口 1: https://tweeterid.com/
   # 窗口 2: nano scripts/user_ids_to_import.txt
   ```

2. **批量查询**
   - 在 tweeterid.com 逐个输入 username
   - 复制 user_id
   - 粘贴到文件中（格式：`username user_id`）

3. **批量导入**
   ```bash
   ./venv/bin/python scripts/import_user_ids.py
   ```

4. **验证结果**
   ```bash
   python scripts/check_status.py
   ```

### 时间估算

- 单个账号：约 30 秒
- 28 个账号：约 15-20 分钟
- 批量导入：约 10 秒

---

## 🔧 常见问题

### Q: API 服务器未运行？

```bash
cd /Users/pingxn7/Desktop/x/backend
./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Q: 如何查看服务器日志？

```bash
tail -f /tmp/backend.log
```

### Q: 如何重启服务器？

```bash
# 查找进程
ps aux | grep uvicorn

# 停止服务
kill <PID>

# 启动服务
./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Q: 文件格式错误？

确保格式正确：
```
username user_id
```

不要：
- 使用逗号分隔
- 添加 @ 符号
- 使用引号
- 有多余空格

### Q: 账号已存在？

这是正常的，系统会自动跳过已存在的账号。

---

## 📁 重要文件位置

### 配置文件

- `.env` - 环境配置（包含邮件推送时间）
- `app/config.py` - 应用配置

### 添加账号相关

- `scripts/usernames_to_add.txt` - 需要添加的 username 列表
- `scripts/user_ids_to_import.txt` - 导入文件（需要编辑）
- `scripts/import_user_ids.py` - 批量导入脚本
- `scripts/add_accounts_interactive.py` - 交互式添加工具

### 文档

- `scripts/README_ADD_ACCOUNTS.md` - 快速参考
- `scripts/QUICK_START_ADD_ACCOUNTS.md` - 完整指南
- `scripts/HOW_TO_ADD_ACCOUNTS.md` - 详细说明

### 验证工具

- `scripts/check_status.py` - 查看系统状态
- `scripts/manual_collect.py` - 手动收集推文
- `scripts/test_email.py` - 测试邮件发送

---

## 🎯 下一步行动

### 立即执行

1. ✅ 邮件推送时间已更新（明天上午 8:00 收到邮件）
2. ⏳ 添加 28 个新账号（需要手动操作）

### 添加账号步骤

```bash
# 1. 查看需要添加的账号
cat scripts/usernames_to_add.txt

# 2. 访问 https://tweeterid.com/ 获取 user_ids

# 3. 编辑导入文件
nano scripts/user_ids_to_import.txt

# 4. 运行导入
./venv/bin/python scripts/import_user_ids.py

# 5. 验证结果
python scripts/check_status.py
```

### 完成后

系统将自动：
- ✅ 每 2 小时收集推文
- ✅ 使用 AI 分析推文
- ✅ 每天上午 8:00 发送邮件摘要
- ✅ 提供 Web API 查看数据

---

## 📞 获取帮助

### 查看工具列表

```bash
./scripts/show_add_tools.sh
```

### 查看文档

```bash
cat scripts/README_ADD_ACCOUNTS.md
```

### 查看日志

```bash
tail -f /tmp/backend.log
```

### 查看 API 文档

访问：http://localhost:8000/docs

---

## 🎉 总结

### 已完成

✅ 邮件推送时间已修改为北京时间上午 8:00
✅ 后端服务已重启并应用新配置
✅ 创建了完整的账号添加工具和文档

### 待完成

⏳ 添加 28 个新账号（需要手动获取 user_id）

### 预计时间

- 获取 user_ids：15-20 分钟
- 批量导入：10 秒
- 总计：约 20 分钟

### 完成后效果

- 监控账号数：66 个
- 每天上午 8:00 收到 AI 新闻摘要邮件
- 自动收集和分析推文
- 完整的 Web API 和前端展示

---

祝使用愉快！🚀

如有问题，请查看文档或查看日志。
