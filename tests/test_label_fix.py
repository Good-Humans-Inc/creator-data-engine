"""
测试Label修复 - 使用实际从Notion获取的label数据
"""

from utils import SettlementCalculator

def test_label_fix():
    """测试label空格问题的修复"""

    calculator = SettlementCalculator()

    print("="*60)
    print("测试Label修复（使用实际Notion数据）")
    print("="*60)
    print()

    # 使用实际从Notion获取的label
    test_cases = [
        {
            'name': 'Sora',
            'label': 'Core UGC',  # 实际从Notion获取的label（带空格）
            'video_count': 1,
            'total_views': 791,
            'expected_type': 'Core UGC (20元/条)',
            'expected_base': 20
        },
        {
            'name': 'Mercedes',
            'label': 'Core UGC',
            'video_count': 1,
            'total_views': 2482,
            'expected_type': 'Core UGC (20元/条)',
            'expected_base': 20
        },
        {
            'name': 'Jeon',
            'label': 'discord ugc',
            'video_count': 1,
            'total_views': 2835,
            'expected_type': 'Discord UGC (10元/条)',
            'expected_base': 10
        },
        {
            'name': 'Skyler',
            'label': 'discord ugc',
            'video_count': 2,
            'total_views': 639,
            'expected_type': 'Discord UGC (10元/条)',
            'expected_base': 20  # 2条视频
        },
    ]

    all_passed = True

    for i, case in enumerate(test_cases, 1):
        print(f"测试 {i}: {case['name']}")
        print("-" * 60)
        print(f"  Label (原始): '{case['label']}'")

        # 计算结算
        settlement = calculator.calculate_settlement(
            video_count=case['video_count'],
            total_views=case['total_views'],
            label=case['label']
        )

        # 验证结果
        base_correct = settlement['base_pay'] == case['expected_base']
        type_correct = settlement['ugc_type'] == case['expected_type']

        # 显示结果
        print(f"  视频数: {settlement['video_count']}")
        print(f"  总播放量: {settlement['total_views']:,}")
        print(f"  检测类型: {settlement['ugc_type']}", end='')

        if type_correct:
            print(" ✅")
        else:
            print(f" ❌ (预期: {case['expected_type']})")

        print(f"  底薪: ¥{settlement['base_pay']:.2f}", end='')

        if base_correct:
            print(" ✅")
        else:
            print(f" ❌ (预期: ¥{case['expected_base']})")

        print(f"  提成: ¥{settlement['commission']:.2f}")
        print(f"  总计: ¥{settlement['total']:.2f}")

        if base_correct and type_correct:
            print(f"  结果: ✅ 通过")
        else:
            print(f"  结果: ❌ 失败")
            all_passed = False

        print()

    print("="*60)
    if all_passed:
        print("✅ 所有测试通过！Label检测修复成功")
        print()
        print("验证结果:")
        print("  - Sora (Core UGC) → 20元/条 ✅")
        print("  - Mercedes (Core UGC) → 20元/条 ✅")
        print("  - Jeon (discord ugc) → 10元/条 ✅")
        print("  - Skyler (discord ugc) → 10元/条 ✅")
    else:
        print("❌ 部分测试失败！")
    print("="*60)

if __name__ == "__main__":
    test_label_fix()
