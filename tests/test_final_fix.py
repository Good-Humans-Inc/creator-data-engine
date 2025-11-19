"""
测试最终修复 - 完整流程测试
模拟从Notion获取数据到计算结算的完整流程
"""

from utils import SettlementCalculator

print("="*60)
print("测试完整结算流程（模拟真实数据）")
print("="*60)
print()

# 模拟从Notion获取的创作者数据（带Label）
creators_data = [
    {
        'name': 'Sora',
        'label': 'Core UGC',  # 大UGC
        'videos': [
            {'date': '20251114', 'views': 791}
        ]
    },
    {
        'name': 'Mercedes',
        'label': 'Core UGC',  # 大UGC
        'videos': [
            {'date': '20251115', 'views': 2482}
        ]
    },
    {
        'name': 'Jeon',
        'label': 'discord ugc',  # 小UGC
        'videos': [
            {'date': '20251116', 'views': 2835}
        ]
    },
    {
        'name': 'Skyler',
        'label': 'discord ugc',  # 小UGC
        'videos': [
            {'date': '20251117', 'views': 300},
            {'date': '20251118', 'views': 339}
        ]
    }
]

# 使用SettlementCalculator计算
calculator = SettlementCalculator()
settlement_df = calculator.calculate_monthly_settlement(creators_data, 2025, 11)

print("结算明细：\n")
print(settlement_df.to_string(index=False))
print()

# 验证结果
print("\n" + "="*60)
print("验证结果：")
print("="*60)

expected_results = {
    'Sora': {'ugc_type': 'Core UGC (20元/条)', 'base_pay': 20},
    'Mercedes': {'ugc_type': 'Core UGC (20元/条)', 'base_pay': 20},
    'Jeon': {'ugc_type': 'Discord UGC (10元/条)', 'base_pay': 10},
    'Skyler': {'ugc_type': 'Discord UGC (10元/条)', 'base_pay': 20},  # 2条视频
}

all_correct = True
for _, row in settlement_df.iterrows():
    creator = row['creator']
    expected = expected_results[creator]

    ugc_correct = row['ugc_type'] == expected['ugc_type']
    pay_correct = row['base_pay'] == expected['base_pay']

    status = "✅" if (ugc_correct and pay_correct) else "❌"
    print(f"{status} {creator}: {row['ugc_type']}, 底薪=¥{row['base_pay']}")

    if not (ugc_correct and pay_correct):
        all_correct = False
        print(f"   期望: {expected['ugc_type']}, 底薪=¥{expected['base_pay']}")

print()
if all_correct:
    print("🎉 所有测试通过！Label识别和结算计算都正确！")
else:
    print("⚠️ 部分测试失败，请检查逻辑")

print("="*60)
