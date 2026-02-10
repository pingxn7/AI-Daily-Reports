# System Prompt 更新总结

## ✅ 已完成的更新

### 1. 代码修改
**文件**: `app/services/ai_report_editor.py`

**修改内容**:
- `_load_system_prompt()` 方法现在从外部文件加载 prompt
- 文件路径: `/Users/pingxn7/Desktop/AI_Twitter_Editor_System_Prompt_v2_FULL.md`
- 自动移除 "# Daily Run Prompt" 部分
- 如果文件不存在，使用内置备用 prompt

### 2. Prompt 文件位置
```
/Users/pingxn7/Desktop/AI_Twitter_Editor_System_Prompt_v2_FULL.md
```

### 3. 新 Prompt 特点
- 专业 AI 行业媒体主编风格
- 全文中文 + Twitter 原文英文引用
- 每个事件包含完整引用（作者、原文、互动数据、链接）
- 深度解读 + 对 AI 从业者的启示（产品/技术/商业/职业）
- Signal > Noise：从数百推文提炼 5-10 个关键事件
- Insight > Summary：跨作者综合分析

## 🎯 如何验证更新生效

### 方法 1: 查看加载的 Prompt
```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python -c "
from app.services.ai_report_editor import ai_report_editor
print('Prompt 长度:', len(ai_report_editor.system_prompt))
print('Prompt 前 300 字符:')
print(ai_report_editor.system_prompt[:300])
"
```

### 方法 2: 生成日报并对比
```bash
# 生成新日报
python scripts/generate_daily_report.py 2026-02-08

# 查看生成的日报
cat reports/ai_daily_report_2026-02-08.md
```

**新日报应该包含**:
- 🔥 今日最重要的 3 件事
- 🧠 关键事件深度解读（5-8 个）
  - 发生了什么
  - 🔎 Twitter 原文引用（完整格式）
  - 关键细节
  - 行业解读
  - 对 AI 从业者的启示（产品/技术/商业/职业）
- 📈 今日趋势
- 🧭 值得关注的信号
- 💡 编辑点评（Daily Take）

## 🚀 快速命令

### 生成日报
```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python scripts/generate_daily_report.py 2026-02-08
```

### 自动重试生成（推荐）
```bash
cd /Users/pingxn7/Desktop/x/backend
./scripts/generate_report_with_retry.sh
```

### 发送邮件
```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python scripts/test_email.py
```

### 查看系统状态
```bash
cd /Users/pingxn7/Desktop/x/backend
source venv/bin/activate
python scripts/check_status.py
```

## ⚠️ 当前问题

**Anthropic API 502 错误**
- 这是 Anthropic 服务端的临时问题
- 不是代码问题
- 通常几分钟到几小时后会恢复
- 可以使用自动重试脚本

## 📝 修改 Prompt

如果需要修改 prompt，直接编辑文件：
```bash
nano /Users/pingxn7/Desktop/AI_Twitter_Editor_System_Prompt_v2_FULL.md
```

修改后立即生效，无需重启服务。

## ✅ 确认清单

- [x] 代码已更新为从外部文件加载 prompt
- [x] Prompt 文件已存在于 Desktop
- [x] 自动重试脚本已创建
- [x] 系统正常运行（监听 65 个账号）
- [ ] 等待 API 恢复后生成新日报
- [ ] 验证新日报格式符合要求

---

**最后更新**: 2026-02-08 21:56
