"""
测试货币单位和播放量向下取整
"""

from utils import SettlementCalculator

print("="*60)
print("测试货币单位和播放量向下取整修复")
print("="*60)
print()

calculator = SettlementCalculator()

# 测试用例 - 验证向下取整
test_cases = [
    {'name': 'Sora (Core UGC)', 'label': 'Core UGC', 'video_count': 1, 'views': 806},
    {'name': 'Mercedes (Core UGC)', 'label': 'Core UGC', 'video_count': 1, 'views': 2488},
    {'name': 'Jeon (Discord)', 'label': 'discord ugc', 'video_count': 1, 'views': 2839},
    {'name': 'Test (500 views)', 'label': 'discord ugc', 'video_count': 1, 'views': 500},
    {'name': 'Test (1500 views)', 'label': 'discord ugc', 'video_count': 1, 'views': 1500},
    {'name': 'Test (1999 views)', 'label': 'discord ugc', 'video_count': 1, 'views': 1999},
]

print("测试结果：\n")

all_correct = True
for case in test_cases:
    settlement = calculator.calculate_settlement(
        video_count=case['video_count'],
        total_views=case['views'],
        label=case['label']
    )

    # 计算预期的提成（向下取整）
    expected_commission = int(case['views'] / 1000)
    commission_correct = settlement['commission'] == expected_commission

    # 检查货币单位是否正确
    currency_correct = '$' in settlement['ugc_type']

    status = "✅" if (commission_correct and currency_correct) else "❌"

    print(f"{status} {case['name']}")
    print(f"   Views: {case['views']:,} → 提成: ${settlement['commission']:.0f} (预期: ${expected_commission})")
    print(f"   UGC类型: {settlement['ugc_type']}")
    print(f"   底薪: ${settlement['base_pay']}, 总计: ${settlement['total']:.2f}")

    if not commission_correct:
        print(f"   ⚠️ 提成计算错误！")
        all_correct = False

    if not currency_correct:
        print(f"   ⚠️ 货币单位错误！")
        all_correct = False

    print()

print("="*60)
if all_correct:
    print("🎉 所有测试通过！")
    print()
    print("✅ 货币单位已改为美元 ($)")
    print("✅ 播放量按1000向下取整")
    print()
    print("示例：")
    print("  - 500 views → $0 提成")
    print("  - 1500 views → $1 提成")
    print("  - 1999 views → $1 提成")
    print("  - 2488 views → $2 提成")
else:
    print("❌ 部分测试失败，请检查代码")
print("="*60)
