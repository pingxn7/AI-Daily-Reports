#!/bin/bash
# 批量添加 Twitter 账号脚本
# 使用方法：
# 1. 访问 https://tweeterid.com/ 获取每个账号的 user_id
# 2. 将下面的 "REPLACE_WITH_USER_ID" 替换为实际的 user_id
# 3. 运行此脚本：bash scripts/batch_add_accounts.sh

cd "$(dirname "$0")/.."
source venv/bin/activate

echo "=================================="
echo "批量添加 Twitter 账号"
echo "=================================="
echo ""

# 计数器
ADDED=0
SKIPPED=0
FAILED=0

# 最高优先级（3个）
echo "添加最高优先级账号..."

# 1. Geoffrey Hinton
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @geoffreyhinton..."
    ./scripts/add_account.sh geoffreyhinton "$USER_ID" "Geoffrey Hinton"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @geoffreyhinton (未提供 user_id)"
    ((SKIPPED++))
fi

# 2. Yoshua Bengio
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @Yoshua_Bengio..."
    ./scripts/add_account.sh Yoshua_Bengio "$USER_ID" "Yoshua Bengio"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @Yoshua_Bengio (未提供 user_id)"
    ((SKIPPED++))
fi

# 3. Aidan Gomez
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @aidangomez..."
    ./scripts/add_account.sh aidangomez "$USER_ID" "Aidan Gomez"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @aidangomez (未提供 user_id)"
    ((SKIPPED++))
fi

echo ""
echo "添加高优先级账号..."

# 4. Greg Brockman
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @gdb..."
    ./scripts/add_account.sh gdb "$USER_ID" "Greg Brockman"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @gdb (未提供 user_id)"
    ((SKIPPED++))
fi

# 5. Mustafa Suleyman
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @mustafasuleyman..."
    ./scripts/add_account.sh mustafasuleyman "$USER_ID" "Mustafa Suleyman"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @mustafasuleyman (未提供 user_id)"
    ((SKIPPED++))
fi

# 6. Noam Shazeer
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @NoamShazeer..."
    ./scripts/add_account.sh NoamShazeer "$USER_ID" "Noam Shazeer"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @NoamShazeer (未提供 user_id)"
    ((SKIPPED++))
fi

# 7. Jack Clark
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @jackclarkSF..."
    ./scripts/add_account.sh jackclarkSF "$USER_ID" "Jack Clark"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @jackclarkSF (未提供 user_id)"
    ((SKIPPED++))
fi

# 8. Fei-Fei Li
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @drfeifei..."
    ./scripts/add_account.sh drfeifei "$USER_ID" "Fei-Fei Li"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @drfeifei (未提供 user_id)"
    ((SKIPPED++))
fi

echo ""
echo "添加中等优先级账号..."

# 9. Oriol Vinyals
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @OriolVinyalsML..."
    ./scripts/add_account.sh OriolVinyalsML "$USER_ID" "Oriol Vinyals"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @OriolVinyalsML (未提供 user_id)"
    ((SKIPPED++))
fi

# 10. Sebastien Bubeck
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @SebastienBubeck..."
    ./scripts/add_account.sh SebastienBubeck "$USER_ID" "Sebastien Bubeck"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @SebastienBubeck (未提供 user_id)"
    ((SKIPPED++))
fi

# 11. Soumith Chintala
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @soumithchintala..."
    ./scripts/add_account.sh soumithchintala "$USER_ID" "Soumith Chintala"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @soumithchintala (未提供 user_id)"
    ((SKIPPED++))
fi

# 12. John Schulman
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @johnschulman2..."
    ./scripts/add_account.sh johnschulman2 "$USER_ID" "John Schulman"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @johnschulman2 (未提供 user_id)"
    ((SKIPPED++))
fi

# 13. Wojciech Zaremba
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @woj_zaremba..."
    ./scripts/add_account.sh woj_zaremba "$USER_ID" "Wojciech Zaremba"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @woj_zaremba (未提供 user_id)"
    ((SKIPPED++))
fi

# 14. Jason Wei
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @_jasonwei..."
    ./scripts/add_account.sh _jasonwei "$USER_ID" "Jason Wei"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @_jasonwei (未提供 user_id)"
    ((SKIPPED++))
fi

# 15. Pieter Abbeel
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @pabbeel..."
    ./scripts/add_account.sh pabbeel "$USER_ID" "Pieter Abbeel"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @pabbeel (未提供 user_id)"
    ((SKIPPED++))
fi

echo ""
echo "添加低优先级账号..."

# 16. Epoch AI Research
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @EpochAIResearch..."
    ./scripts/add_account.sh EpochAIResearch "$USER_ID" "Epoch AI Research"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @EpochAIResearch (未提供 user_id)"
    ((SKIPPED++))
fi

# 17. Sebastian Raschka
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @rasbt..."
    ./scripts/add_account.sh rasbt "$USER_ID" "Sebastian Raschka"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @rasbt (未提供 user_id)"
    ((SKIPPED++))
fi

# 18. Indigo
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @indigox..."
    ./scripts/add_account.sh indigox "$USER_ID" "Indigo"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @indigox (未提供 user_id)"
    ((SKIPPED++))
fi

# 19. Zephyr
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @zephyr_z9..."
    ./scripts/add_account.sh zephyr_z9 "$USER_ID" "Zephyr"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @zephyr_z9 (未提供 user_id)"
    ((SKIPPED++))
fi

# 20. Lenny
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @lennysan..."
    ./scripts/add_account.sh lennysan "$USER_ID" "Lenny"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @lennysan (未提供 user_id)"
    ((SKIPPED++))
fi

# 21. Thinky Machines
USER_ID="REPLACE_WITH_USER_ID"
if [ "$USER_ID" != "REPLACE_WITH_USER_ID" ]; then
    echo "添加 @thinkymachines..."
    ./scripts/add_account.sh thinkymachines "$USER_ID" "Thinky Machines"
    if [ $? -eq 0 ]; then ((ADDED++)); else ((FAILED++)); fi
else
    echo "跳过 @thinkymachines (未提供 user_id)"
    ((SKIPPED++))
fi

echo ""
echo "=================================="
echo "批量添加完成"
echo "=================================="
echo "成功添加: $ADDED"
echo "跳过: $SKIPPED"
echo "失败: $FAILED"
echo "=================================="
echo ""
echo "查看当前账号列表："
echo "python scripts/add_accounts_interactive.py --list"
echo ""
