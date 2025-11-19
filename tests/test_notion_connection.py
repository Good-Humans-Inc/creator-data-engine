"""
测试Notion连接
帮助用户验证Token和数据库ID是否正确
"""

from notion_client import Client
import sys

def format_database_id(db_id):
    """格式化数据库ID"""
    # 移除所有连字符和空格
    clean_id = db_id.replace('-', '').replace(' ', '').strip()

    # 如果长度是32，添加连字符
    if len(clean_id) == 32:
        # 格式: 8-4-4-4-12
        formatted = f"{clean_id[0:8]}-{clean_id[8:12]}-{clean_id[12:16]}-{clean_id[16:20]}-{clean_id[20:32]}"
        return formatted

    return clean_id

def test_notion_connection():
    """测试Notion连接"""

    print("=" * 60)
    print("🔍 Notion连接测试工具")
    print("=" * 60)
    print()

    # 获取Token
    token = input("请输入你的Notion Token: ").strip()

    if not token:
        print("❌ Token不能为空！")
        return

    # 获取数据库ID
    db_id = input("请输入数据库ID: ").strip()

    if not db_id:
        print("❌ 数据库ID不能为空！")
        return

    print()
    print("-" * 60)
    print("正在测试连接...")
    print("-" * 60)
    print()

    try:
        # 创建Notion客户端
        notion = Client(auth=token)
        print("✅ Token验证成功")

        # 格式化数据库ID
        formatted_id = format_database_id(db_id)
        print(f"📋 格式化后的数据库ID: {formatted_id}")
        print()

        # 尝试获取数据库信息
        print("正在获取数据库信息...")
        db_info = notion.databases.retrieve(database_id=formatted_id)

        # 获取数据库标题
        title = "未命名"
        if 'title' in db_info and len(db_info['title']) > 0:
            title = db_info['title'][0].get('plain_text', '未命名')

        print()
        print("=" * 60)
        print("✅ 连接成功！")
        print("=" * 60)
        print(f"📊 数据库名称: {title}")
        print(f"🆔 数据库ID: {formatted_id}")
        print()

        # 测试查询数据库
        print("正在测试查询数据库...")
        results = notion.databases.query(database_id=formatted_id)

        num_pages = len(results.get('results', []))
        print(f"✅ 查询成功！找到 {num_pages} 个页面（创作者）")
        print()

        print("=" * 60)
        print("🎉 所有测试通过！你可以使用这个配置：")
        print("=" * 60)
        print(f"Notion Token: {token[:10]}...")
        print(f"数据库ID: {formatted_id}")
        print()
        print("⚠️ 重要提示:")
        print("1. 请确保你已经在Notion数据库中连接了这个集成")
        print("2. 在系统中使用这个格式的数据库ID: " + formatted_id)
        print()

    except Exception as e:
        print()
        print("=" * 60)
        print("❌ 连接失败！")
        print("=" * 60)
        print(f"错误信息: {str(e)}")
        print()
        print("可能的原因：")
        print("1. Token不正确")
        print("2. 数据库ID不正确")
        print("3. 集成未连接到数据库（在Notion数据库页面点击'...' > 'Connections' > 添加你的集成）")
        print("4. 数据库ID格式错误")
        print()

if __name__ == "__main__":
    test_notion_connection()
