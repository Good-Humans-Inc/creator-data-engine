"""
系统测试脚本
用于测试各个模块的基本功能
"""

import sys


def test_imports():
    """测试所有模块是否可以正常导入"""
    print("=" * 60)
    print("测试模块导入...")
    print("=" * 60)

    try:
        import streamlit
        print("✓ Streamlit 导入成功")
    except ImportError as e:
        print(f"✗ Streamlit 导入失败: {e}")
        return False

    try:
        from notion_client import Client
        print("✓ notion-client 导入成功")
    except ImportError as e:
        print(f"✗ notion-client 导入失败: {e}")
        return False

    try:
        import requests
        print("✓ requests 导入成功")
    except ImportError as e:
        print(f"✗ requests 导入失败: {e}")
        return False

    try:
        from bs4 import BeautifulSoup
        print("✓ BeautifulSoup 导入成功")
    except ImportError as e:
        print(f"✗ BeautifulSoup 导入失败: {e}")
        return False

    try:
        import pandas
        print("✓ pandas 导入成功")
    except ImportError as e:
        print(f"✗ pandas 导入失败: {e}")
        return False

    print("\n所有依赖包导入成功！\n")
    return True


def test_modules():
    """测试自定义模块"""
    print("=" * 60)
    print("测试自定义模块...")
    print("=" * 60)

    try:
        from notion_integration import NotionIntegration, format_database_id
        print("✓ notion_integration 模块导入成功")

        # 测试format_database_id函数
        test_id = "2af95b54-7d5e-811b-8b01-e1b61f64f900"
        formatted_id = format_database_id(test_id)
        expected = "2af95b547d5e811b8b01e1b61f64f900"
        assert formatted_id == expected, f"格式化失败: {formatted_id} != {expected}"
        print(f"  - format_database_id 测试通过")

    except Exception as e:
        print(f"✗ notion_integration 模块测试失败: {e}")
        return False

    try:
        from view_scraper import ViewScraper
        print("✓ view_scraper 模块导入成功")

        # 测试基本功能
        scraper = ViewScraper(delay=1.0)

        # 测试平台识别
        assert scraper.identify_platform("https://www.instagram.com/reel/xxx/") == "instagram"
        assert scraper.identify_platform("https://www.tiktok.com/@user/video/xxx") == "tiktok"
        print(f"  - identify_platform 测试通过")

        # 测试数字解析
        assert scraper._parse_views_number("1,234,567") == 1234567
        assert scraper._parse_views_number("1.2M") == 1200000
        assert scraper._parse_views_number("1.2K") == 1200
        print(f"  - _parse_views_number 测试通过")

    except Exception as e:
        print(f"✗ view_scraper 模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    try:
        from utils import SettlementCalculator, DataStorage, format_number
        print("✓ utils 模块导入成功")

        # 测试结算计算
        calculator = SettlementCalculator()
        result = calculator.calculate_settlement(10, 50000, True)
        assert result['base_pay'] == 200  # 10 * 20
        assert result['commission'] == 50  # 50000 / 1000
        assert result['total'] == 250  # 200 + 50
        print(f"  - calculate_settlement 测试通过")

        # 测试数字格式化
        assert format_number(1234567) == "1,234,567"
        assert format_number(1234.567, 2) == "1,234.57"
        print(f"  - format_number 测试通过")

        # 测试数据存储
        storage = DataStorage()
        print(f"  - DataStorage 初始化成功")

    except Exception as e:
        print(f"✗ utils 模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

    print("\n所有自定义模块测试通过！\n")
    return True


def test_python_version():
    """检查Python版本"""
    print("=" * 60)
    print("检查Python版本...")
    print("=" * 60)

    version = sys.version_info
    print(f"当前Python版本: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("✗ Python版本过低，建议使用Python 3.8或更高版本")
        return False

    print("✓ Python版本符合要求\n")
    return True


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("UGC结算管理系统 - 系统测试")
    print("=" * 60 + "\n")

    # 检查Python版本
    if not test_python_version():
        print("\n❌ 测试失败: Python版本不符合要求")
        sys.exit(1)

    # 测试依赖包导入
    if not test_imports():
        print("\n❌ 测试失败: 依赖包导入失败")
        print("\n请运行以下命令安装依赖:")
        print("  pip install -r requirements.txt")
        sys.exit(1)

    # 测试自定义模块
    if not test_modules():
        print("\n❌ 测试失败: 自定义模块测试失败")
        sys.exit(1)

    # 所有测试通过
    print("=" * 60)
    print("✅ 所有测试通过！系统已准备就绪。")
    print("=" * 60)
    print("\n运行以下命令启动应用:")
    print("  streamlit run app.py")
    print("\n或使用一键启动脚本:")
    print("  ./start.sh (macOS/Linux)")
    print("  start.bat (Windows)")
    print()


if __name__ == "__main__":
    main()
