# 🚀 开始使用 - AI News Collector

## ✅ 当前状态

### 已完成配置
- ✅ 邮件推送时间：每天上午 8:00（北京时间）
- ✅ 收件人：pingxn7@gmail.com
- ✅ 后端服务运行中
- ✅ 定时任务已配置
- ✅ 当前监控 38 个账号

### 待完成任务
- ⏳ 添加 28 个新账号（需要约 20 分钟）

---

## 🎯 立即开始

### 方式 1: 查看快速参考（推荐）

```bash
./scripts/quick_ref.sh
```

### 方式 2: 查看系统仪表板

```bash
./scripts/dashboard.sh
```

### 方式 3: 查看任务总结

```bash
cat TASK_COMPLETION_SUMMARY.txt
```

---

## 📋 添加新账号（3 步完成）

### 步骤 1: 获取 User IDs

访问 **https://tweeterid.com/**

逐个输入以下 username（不带 @）：

```
swyx, gregisenberg, joshwoodward, kevinweil, petergyang,
thenanyu, realmadhuguru, mckaywrigley, stevenbjohnson,
amandaaskell, _catwu, trq212, GoogleLabs, george__mack,
raizamrtn, amasad, rauchg, rileybrown, alexalbert__,
hamelhusain, levie, garrytan, lulumeservey, venturetwins,
attturck, joulee, PJaccetturo, zarazhangrui
```

### 步骤 2: 编辑导入文件

```bash
nano scripts/user_ids_to_import.txt
```

添加格式：`username user_id`

例如：
```
swyx 33521530
karpathy 1270166613
```

### 步骤 3: 运行导入

```bash
./venv/bin/python scripts/import_user_ids.py
```

---

## 🛠️ 常用工具

### 添加账号工具

```bash
# 批量导入（推荐）
./venv/bin/python scripts/import_user_ids.py

# 交互式添加
./venv/bin/python scripts/add_accounts_interactive.py

# 快速导入（带确认）
./scripts/quick_import.sh

# 查看所有工具
./scripts/show_add_tools.sh
```

### 系统管理

```bash
# 查看状态
python scripts/check_status.py

# 手动收集推文
python scripts/manual_collect.py

# 测试邮件
python scripts/test_email.py

# 查看日志
tail -f /tmp/backend.log
```

---

## 📚 文档导航

| 文档 | 说明 | 命令 |
|------|------|------|
| 快速参考 | 最常用命令 | `./scripts/quick_ref.sh` |
| 系统仪表板 | 当前状态 | `./scripts/dashboard.sh` |
| 任务总结 | 完成情况 | `cat TASK_COMPLETION_SUMMARY.txt` |
| 添加账号快速指南 | 3 步添加 | `cat scripts/README_ADD_ACCOUNTS.md` |
| 完整添加指南 | 详细说明 | `cat scripts/QUICK_START_ADD_ACCOUNTS.md` |
| 下一步行动 | 完整总结 | `cat SUMMARY_AND_NEXT_STEPS.md` |

---

## 🌐 Web 访问

- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/api/health
- **系统指标**: http://localhost:8000/api/metrics
- **账号列表**: http://localhost:8000/api/accounts

---

## ⏰ 定时任务

### 推文收集
- **频率**: 每 2 小时
- **功能**: 自动收集推文 + AI 分析

### 邮件推送
- **时间**: 每天上午 8:00（北京时间）
- **内容**: AI 生成的摘要 + Top 10 精选推文
- **收件人**: pingxn7@gmail.com
- **下次推送**: 明天上午 8:00

---

## 🔧 服务管理

### 启动服务

```bash
cd /Users/pingxn7/Desktop/x/backend
./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 查看服务状态

```bash
# 查看进程
ps aux | grep uvicorn

# 查看日志
tail -f /tmp/backend.log

# 检查健康状态
curl http://localhost:8000/api/health
```

### 重启服务

```bash
# 停止服务
kill $(ps aux | grep uvicorn | grep -v grep | awk '{print $2}')

# 启动服务
./venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📊 系统概览

### 当前数据
- 监控账号: 38 个
- 总推文数: 15
- AI 相关推文: 15（100%）
- 每日摘要数: 1

### 完成后（添加 28 个账号）
- 监控账号: 66 个
- 自动收集和分析
- 每天上午 8:00 收到邮件
- 完整的 Web API 访问

---

## 💡 快速命令

```bash
# 一键查看所有信息
./scripts/dashboard.sh

# 查看快速参考
./scripts/quick_ref.sh

# 查看添加工具
./scripts/show_add_tools.sh

# 查看系统状态
python scripts/check_status.py

# 手动收集推文
python scripts/manual_collect.py

# 测试邮件发送
python scripts/test_email.py
```

---

## 🎉 完成后的效果

添加完 28 个账号后，系统将：

1. ✅ **自动收集**: 每 2 小时从 66 个账号收集推文
2. ✅ **AI 分析**: 自动分析推文的 AI 相关性和重要性
3. ✅ **每日摘要**: 每天生成精选推文摘要
4. ✅ **邮件推送**: 每天上午 8:00 发送邮件到你的邮箱
5. ✅ **Web 访问**: 通过 API 和前端查看所有数据

---

## 📞 需要帮助？

### 查看文档
```bash
# 查看所有可用工具
./scripts/show_add_tools.sh

# 查看完整指南
cat SUMMARY_AND_NEXT_STEPS.md

# 查看任务总结
cat TASK_COMPLETION_SUMMARY.txt
```

### 检查系统
```bash
# 查看系统状态
./scripts/dashboard.sh

# 查看日志
tail -f /tmp/backend.log

# 查看 API 状态
curl http://localhost:8000/api/health | python3 -m json.tool
```

---

## 🚀 开始使用

**推荐流程**：

1. 查看快速参考：`./scripts/quick_ref.sh`
2. 查看系统仪表板：`./scripts/dashboard.sh`
3. 添加新账号（按照上面的 3 步完成）
4. 验证结果：`python scripts/check_status.py`
5. 等待自动收集和邮件推送

---

祝使用愉快！🎉

如有问题，请查看文档或运行 `./scripts/dashboard.sh` 查看系统状态。
