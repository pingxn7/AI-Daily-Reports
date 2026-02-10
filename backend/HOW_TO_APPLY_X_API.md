# 如何申请和使用 X Developer API

## 为什么需要官方 API？

官方 Twitter/X API v2 是获取用户信息最可靠的方式：
- ✅ 支持批量查询（一次最多100个用户）
- ✅ 数据准确可靠
- ✅ 有官方文档和支持
- ✅ 免费层级足够使用

## 申请步骤（约 10-15 分钟）

### 第 1 步：申请 X Developer 账号

1. **访问 X Developer Portal**
   - 网址: https://developer.twitter.com/
   - 点击右上角 "Sign up" 或 "Apply for access"

2. **登录您的 X/Twitter 账号**
   - 使用您的 Twitter 账号登录
   - 如果没有账号，需要先注册一个

3. **填写申请表单**
   - 选择使用目的: "Hobbyist" 或 "Academic"
   - 项目名称: "AI News Monitoring"
   - 项目描述: "Monitor AI researchers' tweets for news aggregation"
   - 说明您将如何使用 API（示例）:
     ```
     I'm building a personal AI news aggregator that monitors tweets
     from AI researchers and companies. I need to:
     - Look up user IDs by username
     - Fetch recent tweets from monitored accounts
     - No posting, only reading public data
     ```

4. **同意服务条款**
   - 阅读并同意 Developer Agreement
   - 提交申请

5. **等待审批**
   - 通常几分钟到几小时内会收到邮件
   - 免费层级（Free tier）通常会自动批准

### 第 2 步：创建应用并获取 Bearer Token

1. **进入 Developer Portal**
   - 访问: https://developer.twitter.com/en/portal/dashboard

2. **创建项目 (Project)**
   - 点击 "Create Project"
   - 项目名称: "AI News Collector"
   - 使用场景: 选择最接近的选项

3. **创建应用 (App)**
   - 在项目下点击 "Create App"
   - 应用名称: "ai-news-monitor"
   - 应用描述: "Monitor AI researchers tweets"

4. **获取 Bearer Token**
   - 进入应用设置页面
   - 点击 "Keys and tokens" 标签
   - 找到 "Bearer Token" 部分
   - 点击 "Generate" 生成 Bearer Token
   - **重要**: 立即复制并保存 Token（只显示一次！）

### 第 3 步：配置到系统

**方法 1: 使用环境变量（推荐）**

```bash
# 临时设置（当前终端会话）
export TWITTER_BEARER_TOKEN='your-bearer-token-here'

# 永久设置（添加到 ~/.zshrc 或 ~/.bashrc）
echo 'export TWITTER_BEARER_TOKEN="your-bearer-token-here"' >> ~/.zshrc
source ~/.zshrc
```

**方法 2: 添加到 .env 文件**

```bash
cd /Users/pingxn7/Desktop/x/backend
echo 'TWITTER_BEARER_TOKEN=your-bearer-token-here' >> .env
```

### 第 4 步：运行脚本获取 User IDs

```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python scripts/fetch_with_official_api.py
```

脚本会自动：
1. 使用官方 API 批量获取所有账号的 user_id
2. 保存结果到文件
3. 自动添加到监听系统

## API 限制说明

### 免费层级 (Free Tier)

- **用户查询**: 300 次/15分钟
- **推文查询**: 1,500 次/月
- 完全足够我们的使用场景

### 我们的使用量估算

- **获取 21 个账号的 user_id**: 1 次 API 调用（批量查询）
- **每 2 小时收集推文**: 约 250 次/月（17个账号 × 30天 / 2）
- **总计**: 远低于免费限制

## 常见问题

### Q: 申请需要多久？
A: 免费层级通常几分钟到几小时自动批准。

### Q: 需要信用卡吗？
A: 免费层级不需要信用卡。

### Q: Bearer Token 丢失了怎么办？
A: 可以在 Developer Portal 重新生成，旧的会失效。

### Q: 如果申请被拒绝？
A: 可以重新申请，详细说明使用目的。或者使用 tweeterid.com 手动查询。

### Q: 可以用于商业项目吗？
A: 需要申请更高级别的访问权限。个人学习和研究使用免费层级即可。

## 相关链接

- Developer Portal: https://developer.twitter.com/en/portal/dashboard
- API 文档: https://developer.twitter.com/en/docs/twitter-api
- 用户查询 API: https://developer.twitter.com/en/docs/twitter-api/users/lookup/introduction
- 价格说明: https://developer.twitter.com/en/products/twitter-api

## 下一步

获取 Bearer Token 后：

1. 设置环境变量或添加到 .env 文件
2. 运行 `python scripts/fetch_with_official_api.py`
3. 脚本会自动获取所有账号的 user_id 并添加到系统
4. 完成！

如有问题，查看脚本输出的详细错误信息。
