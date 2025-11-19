"""
测试结算计算逻辑
"""

from utils import SettlementCalculator

calculator = SettlementCalculator()

print("="*60)
print("测试结算计算逻辑")
print("="*60)
print()

# 测试用例
test_cases = [
    {'name': 'Sora', 'label': 'Core UGC', 'video_count': 1, 'views': 791},
    {'name': 'Mercedes', 'label': 'Core UGC', 'video_count': 1, 'views': 2482},
    {'name': 'Jeon', 'label': 'discord ugc', 'video_count': 1, 'views': 2835},
    {'name': 'Skyler', 'label': 'discord ugc', 'video_count': 2, 'views': 639},
]

for case in test_cases:
    settlement = calculator.calculate_settlement(
        video_count=case['video_count'],
        total_views=case['views'],
        label=case['label']
    )

    print(f"{case['name']} (Label: '{case['label']}')")
    print(f"  - UGC类型: {settlement['ugc_type']}")
    print(f"  - 视频数: {settlement['video_count']}")
    print(f"  - 播放量: {settlement['total_views']}")
    print(f"  - 底薪: ¥{settlement['base_pay']}")
    print(f"  - 提成: ¥{settlement['commission']:.2f}")
    print(f"  - 总计: ¥{settlement['total']:.2f}")
    print()

print("="*60)
print("测试完成")
print("="*60)
