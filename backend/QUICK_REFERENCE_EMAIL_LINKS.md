# 快速参考 - 日报邮件查看详情功能

## 🚀 快速开始

### 1. 配置环境变量
```bash
# backend/.env
FRONTEND_URL=http://localhost:3000
RESEND_API_KEY=your-api-key
EMAIL_TO=your-email@example.com
ENABLE_EMAIL=True
```

### 2. 测试邮件
```bash
cd backend
source venv/bin/activate
python scripts/test_email_with_links.py
```

### 3. 预览邮件
```bash
python scripts/preview_email.py
open email_preview.html
```

## 📧 邮件中的链接

| 位置 | 文字 | 跳转目标 | 样式 |
|------|------|----------|------|
| 头部 | 📖 查看完整详情 | 当天详情页 | 白色按钮 |
| 底部 | 🌐 在线查看完整报告 | 当天详情页 | 半透明按钮 |
| 底部 | 📚 浏览历史日报 | 首页列表 | 文字链接 |

## 🔗 URL 格式

```
详情页: {FRONTEND_URL}/summary/{url_slug}
示例: http://localhost:3000/summary/2026-02-10

首页: {FRONTEND_URL}
示例: http://localhost:3000
```

## 🧪 测试命令

```bash
# 预览邮件模板
python scripts/preview_email.py

# 发送测试邮件
python scripts/test_email_with_links.py

# 启动后端服务
uvicorn app.main:app --reload

# 启动前端服务（新终端）
cd ../frontend && npm run dev
```

## ✅ 验证清单

- [ ] 邮件头部有"查看完整详情"按钮
- [ ] 邮件底部有"在线查看完整报告"按钮
- [ ] 邮件底部有"浏览历史日报"链接
- [ ] 点击链接能正确跳转
- [ ] 详情页显示完整内容
- [ ] 首页显示历史列表

## 🔧 常见问题

**Q: 链接无法跳转？**
A: 检查 FRONTEND_URL 配置是否正确

**Q: 详情页 404？**
A: 确保前端服务正在运行，检查 URL slug

**Q: 生产环境链接错误？**
A: 更新生产环境的 FRONTEND_URL 为正确域名

## 📁 相关文件

```
backend/
├── app/services/email_service_v2.py  # 邮件服务（已修改）
├── scripts/
│   ├── preview_email.py              # 预览邮件
│   └── test_email_with_links.py      # 测试邮件
├── EMAIL_FEATURE_SUMMARY.md          # 功能总结
└── EMAIL_DETAIL_LINK_GUIDE.md        # 使用指南

frontend/
├── app/
│   ├── page.tsx                      # 首页（历史列表）
│   └── summary/[id]/page.tsx         # 详情页
└── lib/api.ts                        # API 客户端
```

## 🎯 核心代码

### 生成详情页 URL
```python
# backend/app/services/email_service_v2.py
detail_url = f"{settings.frontend_url}/summary/{summary.url_slug}"
```

### 邮件中的按钮
```html
<a href="{detail_url}" style="...">
    📖 查看完整详情
</a>
```

### 前端路由
```typescript
// frontend/app/summary/[id]/page.tsx
// 支持: /summary/123 或 /summary/2026-02-10
```

## 📊 数据流

```
定时任务 → 生成日报 → 保存数据库 → 发送邮件 → 用户点击 → Web 页面
```

## 🔐 生产环境配置

```bash
# 生产环境 .env
FRONTEND_URL=https://your-domain.com
RESEND_API_KEY=your-production-key
EMAIL_FROM=noreply@your-domain.com
EMAIL_TO=user@example.com
ENABLE_EMAIL=True
```

## 📞 获取帮助

- 详细指南: `EMAIL_DETAIL_LINK_GUIDE.md`
- 功能总结: `EMAIL_FEATURE_SUMMARY.md`
- 项目文档: `README.md`
