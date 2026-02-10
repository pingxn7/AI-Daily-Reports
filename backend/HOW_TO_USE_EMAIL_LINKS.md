# 如何使用日报邮件查看详情功能

## 🎯 功能说明

用户收到 AI 行业日报邮件后，可以通过邮件中的链接查看完整内容和浏览历史日报。

## 📧 邮件中的三个链接

### 1. 头部主按钮 - "📖 查看完整详情"
- **位置**: 邮件顶部，标题下方
- **样式**: 白色背景，蓝紫色文字，大按钮
- **功能**: 点击跳转到当天日报的详情页
- **适用场景**: 想要查看完整报告和所有推文详情

### 2. 底部次按钮 - "🌐 在线查看完整报告"
- **位置**: 邮件底部，页脚区域
- **样式**: 半透明背景，白色文字
- **功能**: 点击跳转到当天日报的详情页
- **适用场景**: 阅读完邮件后想要查看更多内容

### 3. 底部文字链接 - "📚 浏览历史日报"
- **位置**: 邮件底部，次按钮下方
- **样式**: 文字链接，带下划线
- **功能**: 点击跳转到首页，查看所有历史日报
- **适用场景**: 想要查看之前的日报或浏览所有历史记录

## 🚀 快速测试

### 步骤 1: 生成邮件预览
```bash
cd backend
source venv/bin/activate
python scripts/preview_email.py
```

这会生成一个 `email_preview.html` 文件，你可以在浏览器中打开查看效果。

### 步骤 2: 发送测试邮件
```bash
python scripts/test_email_with_links.py
```

这会发送一封测试邮件到你配置的邮箱地址。

### 步骤 3: 检查邮件
1. 打开你的邮箱
2. 查找标题为 "🤖 AI 行业日报 | 2026年02月10日" 的邮件
3. 点击邮件中的各个链接，验证是否能正确跳转

## 🔧 配置要求

### 必需配置
在 `backend/.env` 文件中设置：

```bash
FRONTEND_URL=http://localhost:3000
```

生产环境改为：
```bash
FRONTEND_URL=https://your-domain.com
```

### 可选配置（用于发送邮件）
```bash
RESEND_API_KEY=your-resend-api-key
EMAIL_TO=your-email@example.com
ENABLE_EMAIL=True
```

## 📱 用户使用流程

### 场景 1: 查看当天详情
```
1. 用户收到邮件
   ↓
2. 在邮箱中快速浏览摘要
   ↓
3. 点击 "📖 查看完整详情"
   ↓
4. 浏览器打开详情页
   ↓
5. 查看完整的推文列表和详细分析
```

### 场景 2: 浏览历史日报
```
1. 用户收到邮件
   ↓
2. 想查看之前的日报
   ↓
3. 点击 "📚 浏览历史日报"
   ↓
4. 浏览器打开首页
   ↓
5. 看到所有历史日报列表
   ↓
6. 点击任意日期查看详情
```

## ✅ 验证清单

使用以下清单验证功能是否正常：

- [ ] 邮件头部有 "📖 查看完整详情" 按钮
- [ ] 按钮样式正确（白色背景，蓝紫色文字）
- [ ] 邮件底部有 "🌐 在线查看完整报告" 按钮
- [ ] 邮件底部有 "📚 浏览历史日报" 链接
- [ ] 点击头部按钮能跳转到详情页
- [ ] 点击底部按钮能跳转到详情页
- [ ] 点击历史链接能跳转到首页
- [ ] 详情页显示完整内容
- [ ] 首页显示历史列表
- [ ] 移动端显示正常

## 🔗 URL 格式

### 详情页 URL
```
格式: {FRONTEND_URL}/summary/{url_slug}

示例:
- 开发环境: http://localhost:3000/summary/2026-02-10
- 生产环境: https://your-domain.com/summary/2026-02-10
```

### 首页 URL
```
格式: {FRONTEND_URL}

示例:
- 开发环境: http://localhost:3000
- 生产环境: https://your-domain.com
```

## 🐛 常见问题

### Q1: 点击链接显示 404
**原因**: 前端服务未启动或 URL 配置错误

**解决方法**:
```bash
# 启动前端服务
cd frontend
npm run dev

# 检查 .env 配置
grep FRONTEND_URL backend/.env
```

### Q2: 邮件中的链接无法点击
**原因**: 邮件客户端不支持 HTML 或链接被屏蔽

**解决方法**:
- 使用现代邮件客户端（Gmail、Outlook、Apple Mail）
- 检查邮件是否被标记为垃圾邮件
- 尝试在浏览器中打开邮件

### Q3: 链接跳转到错误的地址
**原因**: FRONTEND_URL 配置错误

**解决方法**:
```bash
# 检查配置
cat backend/.env | grep FRONTEND_URL

# 更新配置
# 开发环境
FRONTEND_URL=http://localhost:3000

# 生产环境
FRONTEND_URL=https://your-domain.com
```

### Q4: 详情页显示空白
**原因**: 数据库中没有对应的日报记录

**解决方法**:
```bash
# 生成测试日报
cd backend
source venv/bin/activate
python scripts/generate_daily_report.py 2026-02-10
```

## 📊 测试命令汇总

```bash
# 进入项目目录
cd backend
source venv/bin/activate

# 1. 预览邮件（生成 HTML 文件）
python scripts/preview_email.py
open email_preview.html

# 2. 发送测试邮件
python scripts/test_email_with_links.py

# 3. 一键测试所有功能
bash scripts/test_all.sh

# 4. 完整功能演示
bash scripts/demo_email_feature.sh

# 5. 生成测试日报
python scripts/generate_daily_report.py 2026-02-10

# 6. 启动前端服务（新终端）
cd ../frontend
npm run dev
```

## 📚 相关文档

- **EMAIL_LINKS_README.md** - 简明使用说明
- **QUICK_REFERENCE_EMAIL_LINKS.md** - 快速参考
- **EMAIL_DETAIL_LINK_GUIDE.md** - 详细使用指南
- **VISUAL_EXAMPLE.md** - 可视化示例
- **FINAL_IMPLEMENTATION_SUMMARY.md** - 最终实现总结

## 🎉 开始使用

现在你可以：

1. **测试功能**: 运行 `bash scripts/test_all.sh`
2. **发送邮件**: 运行 `python scripts/test_email_with_links.py`
3. **查看效果**: 打开邮箱，点击邮件中的链接

功能已完成并可投入使用！

---

**最后更新**: 2026-02-10
**版本**: v1.0.0
