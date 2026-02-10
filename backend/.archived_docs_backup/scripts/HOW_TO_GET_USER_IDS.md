# 如何批量获取 Twitter User IDs

## 需要获取 User ID 的账号列表

```
1. aidangomez
2. EpochAIResearch
3. drfeifei
4. geoffreyhinton
5. gdb
6. indigox
7. jackclarkSF
8. johnschulman2
9. mustafasuleyman
10. NoamShazeer
11. OriolVinyalsML
12. pabbeel
13. rasbt
14. SebastienBubeck
15. soumithchintala
16. woj_zaremba
17. Yoshua_Bengio
18. zephyr_z9
19. _jasonwei
20. lennysan
21. thinkymachines
```

## 方法 1：使用 tweeterid.com（最简单）

1. 访问 https://tweeterid.com/
2. 在输入框中输入 username（不带 @）
3. 点击 "Convert"
4. 复制显示的数字 ID
5. 粘贴到下面的模板中

## 方法 2：使用 Twitter 网页

1. 访问 https://twitter.com/username
2. 右键点击页面 -> 查看源代码
3. 搜索 "rest_id" 或 "user_id"
4. 找到对应的数字 ID

## 填写模板

获取到 ID 后，请按以下格式填写到 `user_ids.txt` 文件中：

```
aidangomez 获取到的ID
EpochAIResearch 获取到的ID
drfeifei 获取到的ID
...
```

## 快速批量处理技巧

1. 打开 tweeterid.com
2. 打开 `user_ids.txt` 文件
3. 逐个输入 username，获取 ID，填入文件
4. 完成后运行：`python scripts/add_from_txt.py`

## 已经添加的账号（无需重复获取）

✅ karpathy (17919972)
✅ DarioAmodei (739232892)
✅ demishassabis (2735246778)
✅ fchollet (15002544)
✅ ilyasut (16616354)
✅ JeffDean (11658782)
✅ AndrewYNg (1603818258)
