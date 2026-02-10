# AI News Collector - 完整使用指南

## 🎯 快速开始

### 一键启动服务
```bash
cd /Users/pingxn7/Desktop/x/backend
./scripts/start.sh
```

这个脚本会自动：
- ✅ 检查环境和依赖
- ✅ 验证配置文件
- ✅ 检查数据库连接
- ✅ 启动后台服务
- ✅ 启动定时任务

## 📅 自动定时任务

服务启动后，以下任务会自动执行：

### 1. 推文收集（每2小时）
- **时间**: 每天 0:00, 2:00, 4:00, 6:00, 8:00, 10:00, 12:00, 14:00, 16:00, 18:00, 20:00, 22:00
- **功能**: 自动从65个监控账号收集最新推文并进行 AI 分析

### 2. 日报发送（每天早上8点）
- **时间**: 每天早上 8:00（北京时间）
- **收件人**: pingxn7@gmail.com
- **内容**:
  - 前一天的 AI 行业要闻总结
  - 精选10条重要推文
  - 热门话题标签
  - 精美的 HTML 邮件格式

**下次发送时间**: 2026-02-10 08:00:00 CST（明天早上8点）

## 🛠️ 服务管理

### 查看服务状态
```bash
./scripts/check_service.sh
```

### 停止服务
```bash
./scripts/stop_service.sh
```

### 重启服务
```bash
./scripts/stop_service.sh
./scripts/start.sh
```

### 查看实时日志
```bash
tail -f logs/app.log
```

## 📧 手动操作

### 立即发送日报
```bash
# 发送昨天的日报
./venv/bin/python scripts/send_daily_report.py

# 发送指定日期的日报
./venv/bin/python scripts/send_daily_report.py 2026-02-08
```

### 手动收集推文
```bash
./venv/bin/python scripts/manual_collect.py
```

### 手动生成摘要
```bash
./venv/bin/python scripts/manual_summary.py
```

### 测试邮件发送
```bash
./venv/bin/python scripts/test_email.py
```

## 🔍 监控和调试

### 查看系统状态
```bash
./venv/bin/python scripts/check_status.py
```

### 查看调度器状态
```bash
curl http://localhost:8000/api/scheduler/status | python3 -m json.tool
```

### 查看 API 文档
浏览器访问: http://localhost:8000/docs

## ⚙️ 配置说明

配置文件位置: `/Users/pingxn7/Desktop/x/backend/.env`

### 关键配置项

```bash
# 定时任务
SCHEDULE_TWEET_COLLECTION_CRON=0 */2 * * *  # 每2小时
SCHEDULE_DAILY_SUMMARY_CRON=0 8 * * *       # 每天早上8点
SCHEDULE_TIMEZONE=Asia/Shanghai              # 北京时间

# 邮件服务
ENABLE_EMAIL=True
EMAIL_TO=pingxn7@gmail.com
EMAIL_FROM=onboarding@resend.dev
RESEND_API_KEY=re_CzHXWJEB_EDuJFFcvtc9yevuV4UgVv2GR

# 数据库
DATABASE_URL=postgresql://pingxn7:@localhost:5432/ai_news

# Claude AI
ANTHROPIC_API_KEY=sk-64493fff232d7ba4f49391c937f52d362872686ba4e70173
CLAUDE_MODEL=claude-sonnet-4-5-20250929
```

## 📊 当前系统状态

- **监控账号**: 65个 AI 领域 Twitter 账号
- **已收集推文**: 15条
- **AI 相关推文**: 15条 (100%)
- **已生成日报**: 1份 (2026-02-08)
- **邮件状态**: ✅ 已发送到 pingxn7@gmail.com

## 🔧 故障排查

### 邮件未收到
1. 检查垃圾邮件文件夹
2. 确认 `.env` 中 `ENABLE_EMAIL=True`
3. 验证 Resend API Key: `./venv/bin/python scripts/test_email.py`
4. 查看日志: `grep "email" logs/app.log`

### 服务无法启动
1. 检查端口占用: `lsof -i :8000`
2. 查看错误日志: `cat logs/app.log`
3. 验证数据库: `psql -U pingxn7 -d ai_news -c "SELECT 1"`

### 定时任务未执行
1. 确认服务运行: `./scripts/check_service.sh`
2. 查看调度器: `curl http://localhost:8000/api/scheduler/status`
3. 检查时区设置: `SCHEDULE_TIMEZONE=Asia/Shanghai`

### 推文收集失败
1. 检查 Twitter API Key: `./venv/bin/python scripts/test_bearer_token.py`
2. 查看收集日志: `grep "collect" logs/app.log`
3. 手动测试: `./venv/bin/python scripts/manual_collect.py`

## 📁 项目结构

```
backend/
├── app/
│   ├── api/routes/          # API 路由
│   │   ├── scheduler.py     # 调度器状态 API
│   │   ├── summaries.py     # 日报摘要 API
│   │   └── accounts.py      # 账号管理 API
│   ├── services/
│   │   ├── email_service_v2.py      # 邮件服务
│   │   ├── twitter_collector.py     # 推文收集
│   │   ├── ai_analyzer.py           # AI 分析
│   │   └── aggregator.py            # 数据聚合
│   ├── tasks/
│   │   └── scheduler.py     # 定时任务调度器
│   └── main.py              # FastAPI 应用入口
├── scripts/
│   ├── start.sh             # 一键启动脚本 ⭐
│   ├── stop_service.sh      # 停止服务
│   ├── check_service.sh     # 查看状态
│   ├── send_daily_report.py # 手动发送日报
│   ├── manual_collect.py    # 手动收集推文
│   └── test_email.py        # 测试邮件
├── logs/
│   ├── app.log              # 应用日志
│   └── app.pid              # 进程 ID
└── .env                     # 配置文件

## 🎉 完成！

您的 AI News Collector 已经配置完成！

**明天早上8点**，您将收到第一封自动生成的 AI 行业日报邮件。

如有任何问题，请查看日志文件或运行相应的测试脚本。
```

## 🔗 相关文档

- [调度器配置指南](SCHEDULER_GUIDE.md)
- [API 文档](http://localhost:8000/docs)
- [系统状态检查](scripts/check_status.py)

## 📞 支持

如需帮助，请查看：
1. 日志文件: `logs/app.log`
2. 系统状态: `./venv/bin/python scripts/check_status.py`
3. 测试脚本: `scripts/test_*.py`
