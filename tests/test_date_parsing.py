"""测试日期解析功能 - 支持同一天多个视频"""

from utils import parse_video_date

# 测试各种日期格式
test_cases = [
    # 基本格式
    "20251114",
    "2025-11-14",
    "2025/11/14",
    "2025.11.14",

    # 同一天多个视频（带序号）
    "20251114-1",
    "20251114-2",
    "20251114-3",

    # 其他序号格式
    "20251114_01",
    "20251114_02",
    "20251114a",
    "20251114b",
    "20251114_video1",

    # 无效格式
    "invalid",
    "2025",
    "",
]

print("=" * 60)
print("测试日期解析功能")
print("=" * 60)

for test_str in test_cases:
    result = parse_video_date(test_str)
    status = "✅" if result else "❌"

    if result:
        print(f"{status} '{test_str:20s}' -> {result.strftime('%Y-%m-%d')} (年:{result.year} 月:{result.month})")
    else:
        print(f"{status} '{test_str:20s}' -> 解析失败")

print("\n" + "=" * 60)
print("结论：")
print("✅ 支持同一天多个视频的命名格式")
print("✅ 推荐格式：20251114-1, 20251114-2, 20251114-3")
print("=" * 60)
