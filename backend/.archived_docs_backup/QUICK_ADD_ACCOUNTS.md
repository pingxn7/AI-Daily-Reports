# 快速添加 Twitter 账号指南

## 当前状态

✅ 已添加 7 个账号
⏳ 还需添加 21 个账号

## 方法 1：使用 tweeterid.com（推荐，最快）

### 步骤：

1. **打开两个窗口**
   - 窗口 1: https://tweeterid.com/
   - 窗口 2: 编辑 `scripts/user_ids.txt` 文件

2. **批量处理**
   - 在 tweeterid.com 输入 username（不带 @）
   - 点击 "Convert"
   - 复制数字 ID
   - 粘贴到 `user_ids.txt` 对应行

3. **运行导入**
   ```bash
   cd /Users/pingxn7/Desktop/x/backend
   source venv/bin/activate
   python scripts/add_from_txt.py
   ```

## 需要获取 ID 的账号列表

```
aidangomez
EpochAIResearch
drfeifei
geoffreyhinton
gdb
indigox
jackclarkSF
johnschulman2
mustafasuleyman
NoamShazeer
OriolVinyalsML
pabbeel
rasbt
SebastienBubeck
soumithchintala
woj_zaremba
Yoshua_Bengio
zephyr_z9
_jasonwei
lennysan
thinkymachines
```

## 方法 2：逐个添加（如果只想添加几个重要账号）

使用命令行直接添加：

```bash
# 格式：
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"username": "账号名", "user_id": "账号ID", "is_active": true}'

# 示例：
curl -X POST http://localhost:8000/api/accounts \
  -H "Content-Type: application/json" \
  -d '{"username": "aidangomez", "user_id": "123456789", "is_active": true}'
```

## 优先级建议

如果时间有限，建议优先添加这些重要账号：

**高优先级（AI 领域核心人物）：**
1. geoffreyhinton - Geoffrey Hinton（图灵奖得主，深度学习之父）
2. Yoshua_Bengio - Yoshua Bengio（图灵奖得主）
3. aidangomez - Aidan Gomez（Cohere CEO，Transformer 作者）
4. gdb - Greg Brockman（OpenAI 联合创始人）
5. mustafasuleyman - Mustafa Suleyman（Microsoft AI CEO）

**中优先级（知名研究者）：**
6. NoamShazeer - Noam Shazeer（Transformer 作者）
7. johnschulman2 - John Schulman（OpenAI 研究员）
8. pabbeel - Pieter Abbeel（UC Berkeley 教授）
9. OriolVinyalsML - Oriol Vinyals（DeepMind）
10. SebastienBubeck - Sebastien Bubeck（Microsoft Research）

**低优先级（内容创作者和组织）：**
11-21. 其他账号

## 文件位置

- 模板文件：`/Users/pingxn7/Desktop/x/backend/scripts/user_ids.txt`
- 导入脚本：`/Users/pingxn7/Desktop/x/backend/scripts/add_from_txt.py`
- 指南文件：`/Users/pingxn7/Desktop/x/backend/scripts/HOW_TO_GET_USER_IDS.md`

## 预计时间

- 每个账号约 30 秒（在 tweeterid.com 查询 + 复制粘贴）
- 21 个账号约 10-15 分钟
- 只添加高优先级 5 个账号约 3-5 分钟
