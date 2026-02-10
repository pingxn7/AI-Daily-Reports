# AI News Collector - 定时任务配置

## 功能说明

系统已配置自动定时任务：

### 1. 推文收集任务
- **频率**: 每2小时执行一次
- **Cron**: `0 */2 * * *`
- **功能**: 自动从监控的 Twitter 账号收集最新推文并进行 AI 分析

### 2. 日报生成与发送任务
- **频率**: 每天早上 8:00（北京时间）
- **Cron**: `0 8 * * *`
- **时区**: Asia/Shanghai
- **收件人**: pingxn7@gmail.com
- **功能**:
  - 自动生成前一天的 AI 行业日报
  - 使用 Claude AI 分析和总结
  - 发送精美的 HTML 邮件到指定邮箱

## 快速启动

### 方式一：前台运行（开发模式）
```bash
cd /Users/pingxn7/Desktop/x/backend
./scripts/start_service.sh
```

### 方式二：后台运行（生产模式）
```bash
cd /Users/pingxn7/Desktop/x/backend
./scripts/start_daemon.sh
```

## 服务管理

### 查看服务状态
```bash
./scripts/check_service.sh
```

### 停止服务
```bash
./scripts/stop_service.sh
```

### 查看日志
```bash
tail -f logs/app.log
```

## 手动操作

### 手动发送日报
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

## 配置文件

定时任务配置在 `.env` 文件中：

```bash
# 定时任务配置
SCHEDULE_TWEET_COLLECTION_CRON=0 */2 * * *  # 每2小时
SCHEDULE_DAILY_SUMMARY_CRON=0 8 * * *       # 每天早上8点
SCHEDULE_TIMEZONE=Asia/Shanghai              # 北京时间

# 邮件配置
ENABLE_EMAIL=True
EMAIL_TO=pingxn7@gmail.com
EMAIL_FROM=onboarding@resend.dev
RESEND_API_KEY=your-api-key
```

## API 端点

服务启动后可访问：

- **API 文档**: http://localhost:8000/docs
- **健康检查**: http://localhost:8000/
- **调度器状态**: http://localhost:8000/api/scheduler/status

## 注意事项

1. **时区设置**: 确保 `SCHEDULE_TIMEZONE=Asia/Shanghai` 以使用北京时间
2. **邮件配置**: 确保 `ENABLE_EMAIL=True` 且 Resend API Key 已配置
3. **数据库**: 确保 PostgreSQL 数据库正在运行
4. **后台运行**: 使用 `start_daemon.sh` 启动后台服务，服务会持续运行

## 下次运行时间

当前配置下，日报将在：
- **明天早上 8:00（北京时间）** 自动生成并发送
- 之后每天早上 8:00 自动执行

## 测试配置

运行测试脚本查看定时任务配置：
```bash
./venv/bin/python scripts/test_scheduler.py
```

## 故障排查

### 邮件未收到
1. 检查垃圾邮件文件夹
2. 确认 `.env` 中 `ENABLE_EMAIL=True`
3. 确认 Resend API Key 有效
4. 查看日志: `tail -f logs/app.log`

### 服务未启动
1. 检查端口 8000 是否被占用: `lsof -i :8000`
2. 查看日志: `cat logs/app.log`
3. 确认数据库连接正常

### 定时任务未执行
1. 确认服务正在运行: `./scripts/check_service.sh`
2. 查看调度器状态: `curl http://localhost:8000/api/scheduler/status`
3. 检查日志中的定时任务执行记录
