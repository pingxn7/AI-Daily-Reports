# AI News Collector - Vercel + Render 部署指南

本指南将详细指导你使用 Vercel 部署前端，Render 部署后端。

---

## 📋 部署前准备

### 必需的账号和 API Keys

在开始之前，请确保你已经准备好：

- [ ] GitHub 账号（用于代码托管）
- [ ] Vercel 账号（https://vercel.com）
- [ ] Render 账号（https://render.com）
- [ ] Twitter API Key（https://twitterapi.io）
- [ ] Anthropic API Key（https://console.anthropic.com）
- [ ] AWS 账号（用于 S3 存储截图）
- [ ] Resend 账号（https://resend.com）

### 预估成本

| 服务 | 月费用 | 说明 |
|------|--------|------|
| Render | $7-25 | 后端 + PostgreSQL |
| Vercel | $0 | 前端（免费层） |
| Claude API | $15-30 | AI 分析 |
| Twitter API | $0-20 | 推文收集 |
| AWS S3 | $1-3 | 截图存储 |
| Resend | $0-5 | 邮件发送 |
| **总计** | **$23-83/月** | |

---

## 第一步：准备代码仓库（5 分钟）

### 1.1 创建 GitHub 仓库

```bash
# 进入项目目录
cd /Users/pingxn7/Desktop/x

# 初始化 Git（如果还没有）
git init

# 添加所有文件
git add .

# 创建初始提交
git commit -m "Initial commit for deployment"

# 在 GitHub 上创建新仓库
# 访问 https://github.com/new
# 仓库名称：ai-news-collector
# 设置为 Private（推荐）

# 关联远程仓库（替换为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/ai-news-collector.git

# 推送代码
git branch -M main
git push -u origin main
```

### 1.2 创建 .gitignore（如果还没有）

确保以下文件不会被提交：

```bash
cat >> .gitignore << 'EOF'
# 环境变量
.env
.env.local
.env.production

# Python
__pycache__/
*.pyc
venv/
*.egg-info/

# Node
node_modules/
.next/
out/

# 数据库
*.db
*.sqlite

# 日志
*.log

# IDE
.vscode/
.idea/
EOF

git add .gitignore
git commit -m "Add .gitignore"
git push
```

---

## 第二步：配置 AWS S3（10 分钟）

### 2.1 创建 S3 Bucket

```bash
# 安装 AWS CLI（如果还没有）
# macOS:
brew install awscli

# 配置 AWS CLI
aws configure
# 输入你的 AWS Access Key ID
# 输入你的 AWS Secret Access Key
# 默认区域：us-east-1
# 默认输出格式：json

# 创建 S3 bucket（bucket 名称必须全局唯一）
aws s3 mb s3://ai-news-screenshots-YOUR_NAME --region us-east-1
```

### 2.2 设置 Bucket 公开访问策略

```bash
# 创建策略文件（替换 YOUR_BUCKET_NAME）
cat > bucket-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
    }
  ]
}
EOF

# 替换 bucket 名称
sed -i '' 's/YOUR_BUCKET_NAME/ai-news-screenshots-YOUR_NAME/g' bucket-policy.json

# 应用策略
aws s3api put-bucket-policy \
  --bucket ai-news-screenshots-YOUR_NAME \
  --policy file://bucket-policy.json
```

### 2.3 启用 CORS

```bash
# 创建 CORS 配置
cat > cors-config.json << 'EOF'
{
  "CORSRules": [
    {
      "AllowedHeaders": ["*"],
      "AllowedMethods": ["GET", "HEAD", "PUT", "POST"],
      "AllowedOrigins": ["*"],
      "ExposeHeaders": []
    }
  ]
}
EOF

# 应用 CORS 配置
aws s3api put-bucket-cors \
  --bucket ai-news-screenshots-YOUR_NAME \
  --cors-configuration file://cors-config.json
```

### 2.4 创建 IAM 用户（用于上传）

1. 访问 AWS Console: https://console.aws.amazon.com/iam/
2. 点击 **Users** → **Create user**
3. 用户名：`ai-news-uploader`
4. 勾选 **Programmatic access**
5. 点击 **Next: Permissions**
6. 选择 **Attach existing policies directly**
7. 搜索并勾选 `AmazonS3FullAccess`
8. 点击 **Next** → **Create user**
9. **重要**：保存 **Access Key ID** 和 **Secret Access Key**

---

## 第三步：部署后端到 Render（15 分钟）

### 3.1 创建 Render 账号

1. 访问 https://render.com
2. 点击 **Get Started** 或 **Sign Up**
3. 使用 GitHub 账号登录（推荐）
4. 授权 Render 访问你的 GitHub 仓库

### 3.2 创建 PostgreSQL 数据库

1. 在 Render Dashboard，点击 **New +** → **PostgreSQL**
2. 配置数据库：
   - **Name**: `ai-news-db`
   - **Database**: `ai_news`
   - **User**: `ai_news_user`（自动生成）
   - **Region**: 选择离你最近的区域（如 Singapore）
   - **PostgreSQL Version**: 14
   - **Plan**: 选择 **Free**（开发测试）或 **Starter $7/月**（生产环境）
3. 点击 **Create Database**
4. 等待数据库创建完成（约 1-2 分钟）
5. **重要**：复制 **Internal Database URL**（格式：`postgresql://...`）

### 3.3 创建后端 Web Service

1. 在 Render Dashboard，点击 **New +** → **Web Service**
2. 选择 **Connect a repository**
3. 找到并选择你的 `ai-news-collector` 仓库
4. 点击 **Connect**

### 3.4 配置后端服务

填写以下配置：

#### 基本设置
- **Name**: `ai-news-backend`
- **Region**: 选择与数据库相同的区域
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3`
- **Build Command**:
  ```bash
  pip install -r requirements.txt && playwright install chromium && playwright install-deps chromium
  ```
- **Start Command**:
  ```bash
  alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```

#### 实例类型
- **Instance Type**:
  - 开发测试：**Free**（512MB RAM，会休眠）
  - 生产环境：**Starter $7/月**（512MB RAM，不休眠）或 **Standard $25/月**（2GB RAM）

### 3.5 配置环境变量

点击 **Advanced** → **Add Environment Variable**，添加以下变量：

#### 数据库配置
```
DATABASE_URL = [粘贴你的 Render PostgreSQL Internal Database URL]
```

#### API Keys
```
TWITTER_API_KEY = your_twitter_api_key
ANTHROPIC_API_KEY = your_anthropic_api_key
```

#### AWS S3 配置
```
AWS_ACCESS_KEY_ID = your_aws_access_key_id
AWS_SECRET_ACCESS_KEY = your_aws_secret_access_key
AWS_S3_BUCKET = ai-news-screenshots-YOUR_NAME
AWS_REGION = us-east-1
```

#### 邮件配置
```
RESEND_API_KEY = your_resend_api_key
EMAIL_FROM = noreply@yourdomain.com
EMAIL_TO = your-email@example.com
```

#### 应用配置
```
APP_NAME = AI News Collector
APP_ENV = production
DEBUG = False
LOG_LEVEL = INFO
```

#### CORS 配置（先留空，部署前端后再更新）
```
FRONTEND_URL = https://your-frontend.vercel.app
CORS_ORIGINS = https://your-frontend.vercel.app
```

#### 功能开关
```
ENABLE_TRANSLATION = True
ENABLE_SCREENSHOT = True
ENABLE_EMAIL = True
```

#### 定时任务配置
```
SCHEDULE_TWEET_COLLECTION_CRON = 0 */2 * * *
SCHEDULE_DAILY_SUMMARY_CRON = 0 8 * * *
SCHEDULE_TIMEZONE = Asia/Shanghai
```

#### 排序配置
```
TOP_TWEETS_COUNT = 10
ENGAGEMENT_WEIGHT_LIKES = 1.0
ENGAGEMENT_WEIGHT_RETWEETS = 2.0
ENGAGEMENT_WEIGHT_REPLIES = 1.5
ENGAGEMENT_WEIGHT_BOOKMARKS = 2.5
AI_RELEVANCE_WEIGHT = 3.0
```

### 3.6 部署后端

1. 点击 **Create Web Service**
2. Render 会自动开始构建和部署（约 5-10 分钟）
3. 等待状态变为 **Live**
4. 复制你的后端 URL（格式：`https://ai-news-backend.onrender.com`）

### 3.7 初始化数据库

部署完成后，需要添加监控账号：

1. 在 Render Dashboard，进入你的 `ai-news-backend` 服务
2. 点击 **Shell** 标签
3. 在命令行中执行：
   ```bash
   python scripts/seed_accounts.py
   ```
4. 看到成功消息后，关闭 Shell

### 3.8 验证后端部署

```bash
# 测试健康检查
curl https://ai-news-backend.onrender.com/api/health

# 应该返回：
# {"status":"healthy","database":"healthy","scheduler":"running","timestamp":"..."}

# 测试 API
curl https://ai-news-backend.onrender.com/api/summaries

# 查看 API 文档
open https://ai-news-backend.onrender.com/docs
```

---

## 第四步：部署前端到 Vercel（10 分钟）

### 4.1 创建 Vercel 账号

1. 访问 https://vercel.com
2. 点击 **Sign Up**
3. 使用 GitHub 账号登录（推荐）
4. 授权 Vercel 访问你的 GitHub 仓库

### 4.2 导入项目

1. 在 Vercel Dashboard，点击 **Add New...** → **Project**
2. 找到并选择你的 `ai-news-collector` 仓库
3. 点击 **Import**

### 4.3 配置前端项目

#### 项目设置
- **Project Name**: `ai-news-frontend`
- **Framework Preset**: `Next.js`（自动检测）
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`（自动填充）
- **Output Directory**: `.next`（自动填充）
- **Install Command**: `npm install`（自动填充）

#### 环境变量

点击 **Environment Variables**，添加以下变量：

```
NEXT_PUBLIC_API_URL = https://ai-news-backend.onrender.com
```
（替换为你的 Render 后端 URL）

```
NEXT_PUBLIC_API_TIMEOUT = 10000
```

```
NEXT_PUBLIC_APP_NAME = AI News Collector
```

```
NEXT_PUBLIC_ENV = production
```

**重要**：确保所有环境变量都选择了 **Production**、**Preview** 和 **Development** 三个环境。

### 4.4 部署前端

1. 点击 **Deploy**
2. Vercel 会自动开始构建和部署（约 2-3 分钟）
3. 等待部署完成
4. 复制你的前端 URL（格式：`https://ai-news-frontend.vercel.app`）

### 4.5 验证前端部署

1. 在浏览器中打开你的前端 URL
2. 应该能看到首页和摘要列表
3. 点击任意摘要，查看详情页
4. 按 F12 打开开发者工具，检查是否有错误

---

## 第五步：更新后端 CORS 配置（2 分钟）

现在你有了前端 URL，需要更新后端的 CORS 配置：

### 5.1 更新 Render 环境变量

1. 回到 Render Dashboard
2. 进入 `ai-news-backend` 服务
3. 点击 **Environment** 标签
4. 找到并更新以下变量：

```
FRONTEND_URL = https://ai-news-frontend.vercel.app
```
（替换为你的 Vercel 前端 URL）

```
CORS_ORIGINS = https://ai-news-frontend.vercel.app
```
（替换为你的 Vercel 前端 URL）

5. 点击 **Save Changes**
6. Render 会自动重新部署后端（约 1-2 分钟）

### 5.2 验证 CORS 配置

```bash
# 测试 CORS
curl -I -H "Origin: https://ai-news-frontend.vercel.app" \
  https://ai-news-backend.onrender.com/api/health

# 应该看到响应头中包含：
# access-control-allow-origin: https://ai-news-frontend.vercel.app
```

---

## 第六步：配置 Resend 邮件服务（5 分钟）

### 6.1 注册 Resend

1. 访问 https://resend.com
2. 点击 **Sign Up**
3. 使用邮箱注册

### 6.2 验证域名（可选但推荐）

如果你有自己的域名：

1. 在 Resend Dashboard，点击 **Domains** → **Add Domain**
2. 输入你的域名（如：`yourdomain.com`）
3. 添加提供的 DNS 记录到你的域名服务商
4. 等待验证完成（通常 5-30 分钟）

如果没有域名，可以使用 Resend 提供的测试域名。

### 6.3 获取 API Key

1. 在 Resend Dashboard，点击 **API Keys** → **Create API Key**
2. 名称：`ai-news-production`
3. 权限：**Sending access**
4. 点击 **Create**
5. **重要**：复制 API Key（只显示一次）

### 6.4 更新后端环境变量

1. 回到 Render Dashboard
2. 进入 `ai-news-backend` 服务
3. 点击 **Environment** 标签
4. 更新 `RESEND_API_KEY` 变量
5. 点击 **Save Changes**

### 6.5 测试邮件发送

在 Render Shell 中执行：

```bash
python scripts/send_daily_report.py
```

检查你的邮箱是否收到测试邮件。

---

## 第七步：最终验证（5 分钟）

### 7.1 完整功能测试

#### 测试后端

```bash
# 1. 健康检查
curl https://ai-news-backend.onrender.com/api/health

# 2. 获取摘要列表
curl https://ai-news-backend.onrender.com/api/summaries

# 3. 获取摘要详情
curl https://ai-news-backend.onrender.com/api/summaries/10

# 4. 查看系统指标
curl https://ai-news-backend.onrender.com/api/metrics

# 5. 检查调度器状态
curl https://ai-news-backend.onrender.com/api/scheduler/status
```

#### 测试前端

1. 打开前端 URL：`https://ai-news-frontend.vercel.app`
2. 验证以下功能：
   - [ ] 首页显示摘要列表
   - [ ] 点击摘要可以查看详情
   - [ ] 详情页显示事件格式内容
   - [ ] 图片正常加载（如果有）
   - [ ] 没有控制台错误

#### 测试定时任务

```bash
# 手动触发推文收集
curl -X POST https://ai-news-backend.onrender.com/api/scheduler/collect

# 手动触发摘要生成
curl -X POST https://ai-news-backend.onrender.com/api/scheduler/summary
```

### 7.2 检查日志

#### Render 日志

1. 进入 Render Dashboard
2. 点击 `ai-news-backend` 服务
3. 点击 **Logs** 标签
4. 查看是否有错误信息

#### Vercel 日志

1. 进入 Vercel Dashboard
2. 点击 `ai-news-frontend` 项目
3. 点击最新的部署
4. 查看 **Build Logs** 和 **Function Logs**

---

## 第八步：配置自定义域名（可选，10 分钟）

### 8.1 配置前端域名（Vercel）

1. 在 Vercel Dashboard，进入 `ai-news-frontend` 项目
2. 点击 **Settings** → **Domains**
3. 输入你的域名（如：`news.yourdomain.com`）
4. 点击 **Add**
5. 按照提示添加 DNS 记录到你的域名服务商：
   - **Type**: `CNAME`
   - **Name**: `news`
   - **Value**: `cname.vercel-dns.com`
6. 等待 DNS 生效（通常 5-30 分钟）

### 8.2 配置后端域名（Render）

1. 在 Render Dashboard，进入 `ai-news-backend` 服务
2. 点击 **Settings** → **Custom Domain**
3. 输入你的域名（如：`api.yourdomain.com`）
4. 点击 **Save**
5. 按照提示添加 DNS 记录到你的域名服务商：
   - **Type**: `CNAME`
   - **Name**: `api`
   - **Value**: `ai-news-backend.onrender.com`
6. 等待 DNS 生效

### 8.3 更新环境变量

配置自定义域名后，需要更新环境变量：

#### Render（后端）
```
FRONTEND_URL = https://news.yourdomain.com
CORS_ORIGINS = https://news.yourdomain.com
```

#### Vercel（前端）
```
NEXT_PUBLIC_API_URL = https://api.yourdomain.com
```

---

## 第九步：设置监控（10 分钟）

### 9.1 使用 UptimeRobot（免费）

1. 访问 https://uptimerobot.com
2. 注册账号
3. 点击 **Add New Monitor**
4. 配置监控：
   - **Monitor Type**: `HTTP(s)`
   - **Friendly Name**: `AI News Backend`
   - **URL**: `https://ai-news-backend.onrender.com/api/health`
   - **Monitoring Interval**: `5 minutes`
5. 点击 **Create Monitor**
6. 重复步骤 3-5，添加前端监控：
   - **Friendly Name**: `AI News Frontend`
   - **URL**: `https://ai-news-frontend.vercel.app`

### 9.2 配置告警

1. 在 UptimeRobot，点击 **My Settings** → **Alert Contacts**
2. 添加你的邮箱或手机号
3. 当服务宕机时会收到通知

---

## 第十步：日常维护（持续）

### 10.1 查看日志

#### Render 日志
```bash
# 在 Render Dashboard 查看实时日志
# 或使用 Render CLI
render logs -s ai-news-backend
```

#### Vercel 日志
```bash
# 在 Vercel Dashboard 查看
# 或使用 Vercel CLI
vercel logs ai-news-frontend
```

### 10.2 更新代码

```bash
# 本地修改代码后
git add .
git commit -m "Update: description of changes"
git push

# Render 和 Vercel 会自动检测并重新部署
```

### 10.3 手动触发部署

#### Render
1. 进入服务页面
2. 点击 **Manual Deploy** → **Deploy latest commit**

#### Vercel
1. 进入项目页面
2. 点击 **Deployments**
3. 点击最新部署旁的 **...** → **Redeploy**

### 10.4 数据库备份

```bash
# 在 Render Dashboard
# 进入 PostgreSQL 数据库
# 点击 "Backups" 标签
# 点击 "Create Backup"

# 或使用命令行
pg_dump -h your-render-db-host -U your-user -d ai_news > backup.sql
```

---

## 📊 成本优化建议

### 降低 Render 成本

1. **使用 Free 层**（开发测试）
   - 注意：Free 层会在 15 分钟无活动后休眠
   - 首次请求会有 30-60 秒延迟

2. **升级到 Starter $7/月**（生产环境）
   - 不会休眠
   - 512MB RAM
   - 足够运行本项目

3. **优化数据库**
   - 定期清理旧数据
   - 添加索引优化查询

### 降低 API 成本

1. **Claude API**
   - 批量处理推文
   - 仅分析 AI 相关内容
   - 使用缓存

2. **AWS S3**
   - 仅 Top 10 生成截图（已实现）
   - 设置生命周期策略删除旧截图

3. **Resend**
   - 免费层 3000 封/月足够使用

---

## 🆘 常见问题排查

### 问题 1: Render 部署失败

**症状**：构建或启动失败

**解决方法**：
1. 查看 Render Logs
2. 检查 `requirements.txt` 是否完整
3. 确认 Python 版本兼容（3.11）
4. 检查环境变量是否正确设置

### 问题 2: 前端无法连接后端

**症状**：前端显示加载错误

**解决方法**：
1. 检查 `NEXT_PUBLIC_API_URL` 是否正确
2. 检查后端 `CORS_ORIGINS` 配置
3. 在浏览器控制台查看具体错误
4. 测试后端 API 是否可访问：
   ```bash
   curl https://ai-news-backend.onrender.com/api/health
   ```

### 问题 3: 定时任务不运行

**症状**：推文不自动收集，摘要不自动生成

**解决方法**：
1. 检查调度器状态：
   ```bash
   curl https://ai-news-backend.onrender.com/api/metrics
   ```
2. 查看 Render Logs 中的 scheduler 相关日志
3. 确认 `SCHEDULE_*_CRON` 环境变量格式正确
4. 注意：Render Free 层休眠时定时任务不会运行

### 问题 4: 数据库连接失败

**症状**：后端启动失败，显示数据库错误

**解决方法**：
1. 检查 `DATABASE_URL` 是否正确
2. 确认使用的是 **Internal Database URL**（不是 External）
3. 检查数据库是否在同一区域
4. 在 Render Shell 中测试连接：
   ```bash
   python -c "from app.database import engine; engine.connect()"
   ```

### 问题 5: 邮件发送失败

**症状**：没有收到每日摘要邮件

**解决方法**：
1. 检查 `RESEND_API_KEY` 是否正确
2. 验证 `EMAIL_FROM` 和 `EMAIL_TO` 格式
3. 检查 Resend Dashboard 的发送日志
4. 手动测试发送：
   ```bash
   # 在 Render Shell
   python scripts/send_daily_report.py
   ```

### 问题 6: 截图上传失败

**症状**：详情页没有截图

**解决方法**：
1. 检查 AWS 凭证是否正确
2. 验证 S3 bucket 权限
3. 检查 bucket 策略是否允许公开读取
4. 查看 Render Logs 中的 S3 错误信息

---

## ✅ 部署完成检查清单

- [ ] 后端部署成功（Render）
- [ ] 前端部署成功（Vercel）
- [ ] 数据库创建并初始化
- [ ] 监控账号已添加
- [ ] AWS S3 配置完成
- [ ] Resend 邮件配置完成
- [ ] CORS 配置正确
- [ ] 健康检查通过
- [ ] API 可以正常访问
- [ ] 前端可以显示数据
- [ ] 定时任务正常运行
- [ ] 监控已设置（UptimeRobot）
- [ ] 自定义域名配置（可选）

---

## 🎉 恭喜！部署完成

你的 AI News Collector 现在已经成功部署到生产环境！

### 重要链接

- **前端**: https://ai-news-frontend.vercel.app
- **后端**: https://ai-news-backend.onrender.com
- **API 文档**: https://ai-news-backend.onrender.com/docs
- **Render Dashboard**: https://dashboard.render.com
- **Vercel Dashboard**: https://vercel.com/dashboard

### 下一步

1. **添加更多监控账号**
   ```bash
   # 在 Render Shell
   python scripts/add_account.py
   ```

2. **调整定时任务时间**
   - 在 Render 环境变量中修改 `SCHEDULE_*_CRON`

3. **配置自定义域名**
   - 让你的应用更专业

4. **设置数据库备份**
   - 定期备份重要数据

5. **监控成本**
   - 定期检查 Render、AWS、Claude API 的使用情况

---

## 📚 相关文档

- **项目文档**: `README.md`
- **API 文档**: `API.md`
- **常见问题**: `FAQ.md`
- **完整部署指南**: `DEPLOYMENT_GUIDE_CN.md`

---

## 🆘 需要帮助？

如果遇到问题：

1. 查看本文档的"常见问题排查"章节
2. 检查 Render 和 Vercel 的日志
3. 访问项目文档查找答案
4. 联系我获取帮助

祝你使用愉快！🚀
