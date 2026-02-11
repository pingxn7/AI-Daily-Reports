# Claude.md - AI News Collection Tool

> 专为 Claude AI 助手优化的项目文档，帮助快速理解项目结构、功能和开发指南

## 📋 项目概览

**项目名称**: AI News Collection Tool
**版本**: 1.0.0
**类型**: 全栈 Web 应用
**主要功能**: 自动监控 Twitter/X 账号，收集 AI 相关内容，使用 Claude API 分析，生成每日摘要并发送邮件通知

### 核心价值

- 🤖 **自动化**: 每 2 小时自动收集推文，每天生成摘要
- 🧠 **AI 驱动**: 使用 Claude API 识别 AI 相关内容并生成摘要
- 📊 **智能排序**: 基于互动数据和 AI 相关性的重要性评分
- 💰 **成本优化**: 选择性截图和翻译，成本降低 90%
- 📧 **邮件通知**: 每日自动发送精美的 HTML 邮件摘要

---

## 🏗️ 技术架构

### 技术栈

**后端 (Backend)**
```
FastAPI (Python 3.9+)
├── PostgreSQL (数据库)
├── SQLAlchemy + Alembic (ORM + 迁移)
├── APScheduler (定时任务)
├── Anthropic Claude API (AI 分析)
├── Playwright (截图生成)
├── AWS S3 (截图存储)
└── Resend (邮件服务)
```

**前端 (Frontend)**
```
Next.js 14 (App Router)
├── TypeScript
├── Tailwind CSS
├── React 18
└── Axios
```

### 系统架构图

```
┌─────────────────┐
│  Twitter/X API  │
└────────┬────────┘
         │ 每2小时收集
         ↓
┌─────────────────────────────────────┐
│         Backend (FastAPI)           │
│  ┌──────────────────────────────┐  │
│  │  Services                    │  │
│  │  ├── twitter_collector.py   │  │
│  │  ├── ai_analyzer.py         │  │
│  │  ├── screenshot_service.py  │  │
│  │  ├── aggregator.py          │  │
│  │  └── email_service_v2.py    │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │  Scheduled Tasks             │  │
│  │  ├── collect_tweets_task()  │  │
│  │  └── daily_summary_task()   │  │
│  └──────────────────────────────┘  │
└────────┬────────────────────────────┘
         │
         ├──→ Claude API (AI 分析)
         ├──→ PostgreSQL (数据存储)
         ├──→ AWS S3 (截图存储)
         └──→ Resend (邮件发送)
         │
         ↓
┌─────────────────────────────────────┐
│      Frontend (Next.js)             │
│  ┌──────────────────────────────┐  │
│  │  Pages                       │  │
│  │  ├── / (摘要列表)           │  │
│  │  └── /summary/[id] (详情)   │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │  Components                  │  │
│  │  ├── EventBasedSummary.tsx  │  │
│  │  ├── TweetCard.tsx          │  │
│  │  ├── SummaryView.tsx        │  │
│  │  └── ui/ (组件库)          │  │
│  └──────────────────────────────┘  │
└─────────────────────────────────────┘
```

---

## 📁 项目结构

```
/Users/pingxn7/Desktop/x/
├── backend/                          # 后端服务
│   ├── app/
│   │   ├── main.py                  # FastAPI 入口
│   │   ├── config.py                # 配置管理
│   │   ├── database.py              # 数据库连接
│   │   ├── models/                  # 数据模型
│   │   │   ├── monitored_account.py
│   │   │   ├── tweet.py
│   │   │   └── daily_summary.py
│   │   ├── schemas/                 # Pydantic 模式
│   │   ├── services/                # 业务逻辑
│   │   │   ├── twitter_collector.py    # 推文收集
│   │   │   ├── ai_analyzer.py          # AI 分析
│   │   │   ├── screenshot_service.py   # 截图服务
│   │   │   ├── aggregator.py           # 数据聚合
│   │   │   ├── email_service_v2.py     # 邮件服务
│   │   │   └── ai_report_editor.py     # AI 报告编辑
│   │   ├── api/routes/              # API 路由
│   │   │   ├── summaries.py
│   │   │   ├── accounts.py
│   │   │   └── scheduler.py
│   │   └── tasks/                   # 定时任务
│   │       └── scheduler.py
│   ├── alembic/                     # 数据库迁移
│   ├── scripts/                     # 工具脚本
│   │   ├── generate_daily_report.py
│   │   ├── send_daily_report.py
│   │   └── manual_summary.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                         # 前端应用
│   ├── app/                         # Next.js 页面
│   │   ├── page.tsx                # 首页（摘要列表）
│   │   ├── summary/[id]/page.tsx   # 摘要详情页
│   │   └── layout.tsx
│   ├── components/                  # React 组件
│   │   ├── EventBasedSummary.tsx   # 事件摘要（优化后）
│   │   ├── TweetCard.tsx           # 推文卡片（优化后）
│   │   ├── SummaryView.tsx         # 摘要视图（优化后）
│   │   ├── HighlightsSummary.tsx   # 关键信息摘要（优化后）
│   │   ├── ui/                     # UI 组件库（新增）
│   │   │   ├── MetricPill.tsx      # 互动数据胶囊
│   │   │   ├── TopicTag.tsx        # 话题标签
│   │   │   ├── StatCard.tsx        # 统计卡片
│   │   │   ├── LoadingSkeleton.tsx # 骨架屏
│   │   │   ├── FilterBar.tsx       # 筛选栏
│   │   │   ├── ScrollToTopButton.tsx
│   │   │   ├── EmptyState.tsx
│   │   │   ├── index.ts
│   │   │   └── README.md           # 组件库文档
│   │   └── examples/               # 示例页面（新增）
│   │       └── ComponentShowcase.tsx
│   ├── lib/
│   │   └── api.ts                  # API 客户端
│   ├── package.json
│   └── .env.local.example
│
├── .env.example                     # 环境变量示例
├── docker-compose.yml               # Docker 配置
├── setup.sh                         # 安装脚本
├── Makefile                         # 快捷命令
├── README.md                        # 项目说明
├── API.md                           # API 文档
├── DEPLOYMENT.md                    # 部署指南
├── FAQ.md                           # 常见问题
└── 中文使用指南.md                  # 中文指南
```

---

## 🔑 核心功能详解

### 1. 推文收集 (Tweet Collection)

**文件**: `backend/app/services/twitter_collector.py`

**功能**:
- 从监控的 Twitter 账号收集推文
- 每 2 小时自动运行一次
- 使用 twitterapi.io API

**关键方法**:
```python
async def collect_all_tweets(db: Session) -> dict:
    """收集所有监控账号的推文"""

async def collect_tweets_for_account(db: Session, account: MonitoredAccount) -> dict:
    """收集单个账号的推文"""
```

**配置**:
```bash
SCHEDULE_TWEET_COLLECTION_CRON=0 */2 * * *  # 每2小时
TWITTER_API_KEY=your-key
```

---

### 2. AI 分析 (AI Analysis)

**文件**: `backend/app/services/ai_analyzer.py`

**功能**:
- 使用 Claude API 分析推文内容
- 判断是否与 AI/ML 相关
- 生成摘要和评估相关性（0-10分）
- 批量处理以优化成本

**关键方法**:
```python
async def process_unprocessed_tweets(db: Session) -> int:
    """处理未分析的推文"""

async def analyze_tweets_batch(tweets: List[Tweet]) -> List[dict]:
    """批量分析推文"""
```

**AI 判断标准**:
- `is_ai_related`: 是否与 AI/ML 相关
- `ai_relevance`: AI 相关性评分 (0-10)
- `summary`: AI 生成的摘要
- `topics`: 提取的话题标签

---

### 3. 重要性评分 (Importance Scoring)

**文件**: `backend/app/services/aggregator.py`

**算法**:
```python
# 互动分数
engagement_score = (
    likes * 1.0 +
    retweets * 2.0 +
    replies * 1.5 +
    bookmarks * 2.5
)

# 归一化互动分数 (0-1)
normalized_engagement = engagement_score / max_engagement_score

# 重要性分数 (0-10)
importance_score = (
    normalized_engagement * 7.0 +  # 70% 权重
    ai_relevance * 0.3              # 30% 权重
)
```

**配置**:
```bash
ENGAGEMENT_WEIGHT_LIKES=1.0
ENGAGEMENT_WEIGHT_RETWEETS=2.0
ENGAGEMENT_WEIGHT_REPLIES=1.5
ENGAGEMENT_WEIGHT_BOOKMARKS=2.5
AI_RELEVANCE_WEIGHT=3.0
```

---

### 4. 每日摘要 (Daily Summary)

**文件**: `backend/app/services/aggregator.py`

**功能**:
- 每天早上 8:00 (UTC) 自动生成昨天的摘要
- 筛选 AI 相关推文
- 按重要性排序
- 生成两层展示结构

**两层展示**:

1. **精选 (Highlights)** - Top 10:
   - 完整推文卡片
   - 截图
   - AI 摘要
   - 中文翻译
   - 所有互动数据

2. **更多资讯 (Other News)** - 其余推文:
   - 紧凑卡片
   - 仅摘要（无截图、无翻译）
   - 互动数据

**配置**:
```bash
SCHEDULE_DAILY_SUMMARY_CRON=0 8 * * *  # 每天8:00 UTC
TOP_TWEETS_COUNT=10                     # Top 10 精选
```

---

### 5. 邮件服务 (Email Service)

**文件**: `backend/app/services/email_service_v2.py`

**功能**:
- 使用 Resend API 发送邮件
- 精美的 HTML 邮件模板
- 包含 Top 10 精选推文
- 响应式设计

**邮件内容**:
- 统计数据（监控推文数、精选数、关键信息数）
- Top 10 精选推文卡片
- 每个推文包含：
  - 作者信息
  - 推文内容
  - 中文翻译
  - 互动数据
  - 查看原文链接

**配置**:
```bash
RESEND_API_KEY=your-key
EMAIL_FROM=noreply@yourdomain.com
EMAIL_TO=your-email@example.com
ENABLE_EMAIL=True
```

---

### 6. 截图服务 (Screenshot Service)

**文件**: `backend/app/services/screenshot_service.py`

**功能**:
- 使用 Playwright 生成推文截图
- 仅为 Top 10 推文生成（成本优化）
- 上传到 AWS S3
- 返回公开访问 URL

**配置**:
```bash
ENABLE_SCREENSHOT=True
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_S3_BUCKET=your-bucket
```

---

## 🎨 前端优化 (最近更新)

### UI 设计优化

**优化内容**:
- ✅ 模块化卡片设计（5种浅色背景循环）
- ✅ 彩色胶囊按钮系统（互动数据和标签）
- ✅ 紧凑布局（空间节省 30-40%）
- ✅ 统一设计语言（圆角、间距、字体）
- ✅ 完整响应式设计

**优化效果**:
- 统计面板高度: ↓ 35%
- 事件卡片高度: ↓ 30%
- 互动数据占用: ↓ 40%
- 页面可视内容: ↑ 25%

### 可复用组件库

**位置**: `frontend/components/ui/`

**组件列表**:
1. **MetricPill** - 互动数据胶囊
2. **TopicTag** - 话题标签胶囊
3. **StatCard** - 统计卡片
4. **LoadingSkeleton** - 骨架屏加载
5. **FilterBar** - 筛选栏
6. **ScrollToTopButton** - 返回顶部按钮
7. **EmptyState** - 空状态
8. **ComponentShowcase** - 组件展示页面

**使用方式**:
```tsx
import { MetricPill, TopicTag, StatCard } from '@/components/ui';

<MetricPill icon="👍" value={1234} variant="like" />
<TopicTag topic="AI" variant="blue" />
<StatCard icon="📊" value={1234} label="监控推文" variant="blue" />
```

**文档**: `frontend/components/ui/README.md`

### 性能优化

**优化措施**:
- ✅ React.memo 包装所有主要组件
- ✅ useMemo 缓存计算结果
- ✅ useCallback 优化事件处理
- ✅ displayName 便于调试

---

## ⚙️ 配置说明

### 环境变量

**后端 (.env)**:
```bash
# 应用配置
APP_NAME=ai-news-collector
APP_ENV=production
DEBUG=False

# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/ai_news

# API Keys
TWITTER_API_KEY=your-twitter-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
RESEND_API_KEY=your-resend-api-key

# AWS S3
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_S3_BUCKET=your-bucket-name
AWS_REGION=us-east-1

# 邮件配置
EMAIL_FROM=noreply@yourdomain.com
EMAIL_TO=your-email@example.com

# 定时任务
SCHEDULE_TWEET_COLLECTION_CRON=0 */2 * * *  # 每2小时
SCHEDULE_DAILY_SUMMARY_CRON=0 8 * * *       # 每天北京时间8:00
SCHEDULE_TIMEZONE=Asia/Shanghai              # 时区（北京时间）

# 功能开关
ENABLE_TRANSLATION=True
ENABLE_SCREENSHOT=True
ENABLE_EMAIL=True

# 排序配置
TOP_TWEETS_COUNT=10
ENGAGEMENT_WEIGHT_LIKES=1.0
ENGAGEMENT_WEIGHT_RETWEETS=2.0
ENGAGEMENT_WEIGHT_REPLIES=1.5
ENGAGEMENT_WEIGHT_BOOKMARKS=2.5
AI_RELEVANCE_WEIGHT=3.0
```

**前端 (.env.local)**:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🚀 快速开始

### 1. 克隆项目

```bash
cd /Users/pingxn7/Desktop/x
```

### 2. 后端设置

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
playwright install chromium

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 API keys

# 创建数据库
createdb ai_news

# 运行迁移
alembic upgrade head

# 添加监控账号
python scripts/seed_accounts.py

# 启动服务
uvicorn app.main:app --reload
```

### 3. 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.local.example .env.local
# 编辑 .env.local

# 启动开发服务器
npm run dev
```

### 4. 访问应用

- **后端 API**: http://localhost:8000
- **API 文档**: http://localhost:8000/docs
- **前端应用**: http://localhost:3000

---

## 📡 API 端点

### 摘要相关

```
GET  /api/summaries              # 获取摘要列表（分页）
GET  /api/summaries/{id}         # 获取摘要详情
GET  /api/summaries/slug/{slug}  # 通过 slug 获取摘要
```

### 账号管理

```
GET  /api/accounts               # 获取监控账号列表
POST /api/accounts               # 添加监控账号
PUT  /api/accounts/{id}          # 更新账号
DELETE /api/accounts/{id}        # 删除账号
```

### 调度器

```
GET  /api/scheduler/status       # 获取调度器状态
POST /api/scheduler/collect      # 手动触发推文收集
POST /api/scheduler/summary      # 手动触发摘要生成
```

### 系统

```
GET  /api/health                 # 健康检查
GET  /api/metrics                # 系统指标
```

---

## 🛠️ 开发指南

### 添加新的监控账号

**方法 1: 使用脚本**
```bash
cd backend
python scripts/add_account.py
```

**方法 2: 使用 API**
```bash
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "twitter_user_id",
    "username": "username",
    "display_name": "Display Name"
  }'
```

**方法 3: 直接操作数据库**
```python
from app.models.monitored_account import MonitoredAccount
from app.database import SessionLocal

db = SessionLocal()
account = MonitoredAccount(
    user_id="twitter_user_id",
    username="username",
    display_name="Display Name",
    is_active=True
)
db.add(account)
db.commit()
```

### 手动生成摘要

```bash
cd backend
python scripts/generate_daily_report.py
```

### 手动发送邮件

```bash
cd backend
python scripts/send_daily_report.py
```

### 数据库迁移

**创建新迁移**:
```bash
cd backend
alembic revision --autogenerate -m "description"
```

**应用迁移**:
```bash
alembic upgrade head
```

**回滚迁移**:
```bash
alembic downgrade -1
```

### 运行测试

```bash
cd backend
pytest
```

---

## 🐛 故障排查

### 推文收集失败

**可能原因**:
- Twitter API key 无效或过期
- 监控账号不存在或被封禁
- API 速率限制

**解决方法**:
1. 检查 `TWITTER_API_KEY` 是否正确
2. 查看日志: `tail -f backend/logs/app.log`
3. 检查调度器状态: `GET /api/scheduler/status`

### AI 分析失败

**可能原因**:
- Anthropic API key 无效
- API 速率限制
- 网络问题

**解决方法**:
1. 检查 `ANTHROPIC_API_KEY` 是否正确
2. 查看 Claude API 使用情况
3. 检查日志中的错误信息

### 截图生成失败

**可能原因**:
- Playwright 未安装
- AWS S3 配置错误
- 网络问题

**解决方法**:
1. 安装 Playwright: `playwright install chromium`
2. 检查 AWS 凭证是否正确
3. 验证 S3 bucket 权限

### 邮件发送失败

**可能原因**:
- Resend API key 无效
- 邮箱地址格式错误
- API 速率限制

**解决方法**:
1. 检查 `RESEND_API_KEY` 是否正确
2. 验证 `EMAIL_FROM` 和 `EMAIL_TO` 格式
3. 查看 Resend 控制台日志

### 前端无法连接后端

**可能原因**:
- 后端服务未启动
- CORS 配置错误
- API URL 配置错误

**解决方法**:
1. 确认后端服务运行: `curl http://localhost:8000/api/health`
2. 检查 `NEXT_PUBLIC_API_URL` 配置
3. 查看浏览器控制台错误

---

## 💰 成本优化

### 当前优化措施

1. **选择性截图**: 仅为 Top 10 推文生成截图（90% 成本降低）
2. **选择性翻译**: 仅为 Top 10 推文翻译（90% 成本降低）
3. **批量处理**: 多个推文在单次 API 调用中分析
4. **智能过滤**: 仅处理 AI 相关内容

### 成本估算

**假设**:
- 每天收集 100 条推文
- 其中 30 条与 AI 相关
- Top 10 需要截图和翻译

**月度成本**:
- Claude API: $15-30
- Resend (邮件): $0-5
- AWS S3: $1-3
- Twitter API: $0 (免费层)

**总计**: $20-40/月

**优化前**: $80-150/月

---

## 📚 相关文档

- **README.md** - 项目概述和快速开始
- **API.md** - 完整 API 文档
- **DEPLOYMENT.md** - 部署指南
- **FAQ.md** - 常见问题
- **中文使用指南.md** - 中文详细指南
- **frontend/components/ui/README.md** - UI 组件库文档

---

## 🔄 定时任务

### 推文收集任务

- **频率**: 每 2 小时
- **Cron**: `0 */2 * * *`
- **功能**: 收集监控账号的推文并进行 AI 分析

### 每日摘要任务

- **频率**: 每天 1 次
- **时间**: 8:00 (UTC)
- **Cron**: `0 8 * * *`
- **功能**: 生成昨天的摘要并发送邮件

**注意**: 如果在中国，UTC 8:00 = 北京时间 16:00

**修改为北京时间 8:00**:
```bash
# 当前配置：北京时间早上 8 点
SCHEDULE_TIMEZONE=Asia/Shanghai
SCHEDULE_DAILY_SUMMARY_CRON=0 8 * * *

# 其他时区示例
# UTC 时间（需要调整小时数）
SCHEDULE_TIMEZONE=UTC
SCHEDULE_DAILY_SUMMARY_CRON=0 0 * * *  # UTC 0:00 = 北京 8:00

# 美国东部时间
SCHEDULE_TIMEZONE=America/New_York
SCHEDULE_DAILY_SUMMARY_CRON=0 8 * * *  # 纽约时间 8:00
```

---

## 🎯 最佳实践

### 开发建议

1. **使用虚拟环境**: 始终在虚拟环境中开发
2. **环境变量**: 不要提交 `.env` 文件到 Git
3. **数据库迁移**: 每次修改模型后创建迁移
4. **日志记录**: 使用 Loguru 记录重要操作
5. **错误处理**: 捕获并记录所有异常

### 代码规范

1. **Python**: 遵循 PEP 8
2. **TypeScript**: 使用 ESLint 和 Prettier
3. **命名**: 使用清晰、描述性的变量名
4. **注释**: 为复杂逻辑添加注释
5. **类型提示**: Python 使用类型提示，TypeScript 使用接口

### 性能优化

1. **数据库查询**: 使用索引和适当的查询优化
2. **API 调用**: 批量处理以减少调用次数
3. **缓存**: 对频繁访问的数据使用缓存
4. **异步处理**: 使用 async/await 处理 I/O 操作
5. **前端优化**: 使用 React.memo 和 useMemo

---

## 🤝 贡献指南

### 提交代码

1. Fork 项目
2. 创建特性分支: `git checkout -b feature/amazing-feature`
3. 提交更改: `git commit -m 'Add amazing feature'`
4. 推送到分支: `git push origin feature/amazing-feature`
5. 提交 Pull Request

### 报告问题

在 GitHub Issues 中报告问题时，请包含:
- 问题描述
- 复现步骤
- 预期行为
- 实际行为
- 环境信息（OS、Python 版本等）
- 相关日志

---

## 📄 许可证

MIT License - 详见 LICENSE 文件

---

## 📞 支持

- **GitHub Issues**: 报告问题和功能请求
- **文档**: 查看项目文档获取详细信息
- **邮件**: 联系项目维护者

---

## 🎉 最近更新

### v1.0.0 (2026-02-11)

**前端优化**:
- ✅ 优化 UI 设计（模块化卡片、彩色胶囊）
- ✅ 创建可复用组件库（8个组件）
- ✅ 添加性能优化（React.memo、useMemo）
- ✅ 创建组件展示页面

**成果**:
- 空间节省 30-40%
- 页面可视内容增加 25%
- 代码净增加 1663 行
- 4 个 Git 提交

**详情**: 查看最近的 Git 提交历史

---

**最后更新**: 2026-02-11
**维护者**: PengTan
**项目路径**: `/Users/pingxn7/Desktop/x`
