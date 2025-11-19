"""
测试UGC分层检测
验证系统能否正确识别CoreUGC和DiscordUGC
"""

from utils import SettlementCalculator

def test_ugc_tier_detection():
    """测试UGC分层检测功能"""

    calculator = SettlementCalculator()

    print("="*60)
    print("测试UGC分层检测")
    print("="*60)
    print()

    # 测试案例
    test_cases = [
        {
            'name': 'Mercedes',
            'label': 'CoreUGC',
            'video_count': 2,
            'total_views': 3500,
            'expected_base': 40,  # 2 * 20
            'expected_type': 'CoreUGC (20元/条)'
        },
        {
            'name': 'Skyler',
            'label': 'DiscordUGC',
            'video_count': 2,
            'total_views': 3500,
            'expected_base': 20,  # 2 * 10
            'expected_type': 'DiscordUGC (10元/条)'
        },
        {
            'name': 'Sora',
            'label': 'CoreUGC',
            'video_count': 1,
            'total_views': 1500,
            'expected_base': 20,  # 1 * 20
            'expected_type': 'CoreUGC (20元/条)'
        },
        {
            'name': 'Jeon',
            'label': 'DiscordUGC',
            'video_count': 1,
            'total_views': 1500,
            'expected_base': 10,  # 1 * 10
            'expected_type': 'DiscordUGC (10元/条)'
        },
        {
            'name': 'Unknown',
            'label': '',
            'video_count': 1,
            'total_views': 1000,
            'expected_base': 10,  # 1 * 10 (默认为小UGC)
            'expected_type': 'DiscordUGC (10元/条)'
        },
    ]

    all_passed = True

    for i, case in enumerate(test_cases, 1):
        print(f"测试 {i}: {case['name']} (Label: '{case['label']}')")
        print("-" * 60)

        # 计算结算
        settlement = calculator.calculate_settlement(
            video_count=case['video_count'],
            total_views=case['total_views'],
            label=case['label']
        )

        # 验证结果
        base_pay_correct = settlement['base_pay'] == case['expected_base']
        type_correct = settlement['ugc_type'] == case['expected_type']

        # 显示结果
        print(f"  视频数: {settlement['video_count']}")
        print(f"  总播放量: {settlement['total_views']:,}")
        print(f"  UGC类型: {settlement['ugc_type']}")
        print(f"  底薪: ¥{settlement['base_pay']:.2f} {'✅' if base_pay_correct else '❌ 预期:¥' + str(case['expected_base'])}")
        print(f"  提成: ¥{settlement['commission']:.2f}")
        print(f"  总计: ¥{settlement['total']:.2f}")

        if base_pay_correct and type_correct:
            print(f"  结果: ✅ 通过")
        else:
            print(f"  结果: ❌ 失败")
            all_passed = False

        print()

    print("="*60)
    if all_passed:
        print("✅ 所有测试通过！UGC分层检测工作正常")
    else:
        print("❌ 部分测试失败！请检查代码")
    print("="*60)

if __name__ == "__main__":
    test_ugc_tier_detection()
