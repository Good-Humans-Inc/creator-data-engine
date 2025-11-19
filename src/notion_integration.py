"""
Notion API集成模块
处理所有与Notion的交互，包括查询数据库、更新属性等
"""

from notion_client import Client
from typing import Dict, List, Optional, Tuple
import time
import traceback
import requests


def format_database_id(database_id: str) -> str:
    """
    格式化数据库ID，去掉连字符

    Args:
        database_id: 原始数据库ID

    Returns:
        格式化后的数据库ID
    """
    return database_id.replace('-', '')


class NotionIntegration:
    """Notion集成类，处理所有Notion API操作"""

    def __init__(self, token: str):
        """
        初始化Notion客户端

        Args:
            token: Notion集成Token
        """
        self.client = Client(auth=token)
        self.token = token
        self.debug_info = []

    def add_debug(self, message: str):
        """添加调试信息"""
        self.debug_info.append(message)
        print(f"[DEBUG] {message}")

    def get_database_structure(self, database_id: str) -> Dict:
        """
        获取数据库结构

        Args:
            database_id: 数据库ID

        Returns:
            数据库结构信息
        """
        try:
            formatted_id = format_database_id(database_id)
            db = self.client.databases.retrieve(database_id=formatted_id)
            self.add_debug(f"成功获取数据库结构: {db.get('title', [{}])[0].get('plain_text', 'Unknown')}")
            return db
        except Exception as e:
            self.add_debug(f"获取数据库结构失败: {str(e)}")
            raise

    def query_database(self, database_id: str, filter_dict: Optional[Dict] = None) -> List[Dict]:
        """
        查询数据库

        Args:
            database_id: 数据库ID
            filter_dict: 过滤条件（可选）

        Returns:
            查询结果列表
        """
        try:
            formatted_id = format_database_id(database_id)

            # 使用直接的HTTP请求（兼容所有版本）
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Notion-Version': '2022-06-28',
                'Content-Type': 'application/json'
            }

            body = {}
            if filter_dict:
                body['filter'] = filter_dict

            url = f"https://api.notion.com/v1/databases/{formatted_id}/query"
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()

            data = response.json()
            results = data.get('results', [])
            self.add_debug(f"查询数据库成功，返回 {len(results)} 条结果")
            return results

        except Exception as e:
            self.add_debug(f"查询数据库失败: {str(e)}")
            self.add_debug(f"错误详情: {traceback.format_exc()}")
            raise

    def get_page_children(self, page_id: str) -> List[Dict]:
        """
        获取页面的子块

        Args:
            page_id: 页面ID

        Returns:
            子块列表
        """
        try:
            formatted_id = format_database_id(page_id)
            response = self.client.blocks.children.list(block_id=formatted_id)
            blocks = response.get('results', [])
            self.add_debug(f"获取页面子块: {len(blocks)} 个块")
            return blocks
        except Exception as e:
            self.add_debug(f"获取页面子块失败: {str(e)}")
            raise

    def find_child_databases(self, page_id: str) -> List[Dict]:
        """
        查找页面内的所有子数据库

        Args:
            page_id: 页面ID

        Returns:
            子数据库列表，每个包含 {'id': str, 'type': str}
        """
        child_dbs = []
        try:
            blocks = self.get_page_children(page_id)

            for block in blocks:
                block_type = block.get('type')
                if block_type == 'child_database':
                    child_db_id = block.get('id')
                    child_dbs.append({
                        'id': child_db_id,
                        'type': 'child_database'
                    })
                    self.add_debug(f"找到子数据库: {child_db_id}")

            if not child_dbs:
                self.add_debug(f"页面 {page_id} 没有子数据库")

            return child_dbs

        except Exception as e:
            self.add_debug(f"查找子数据库失败: {str(e)}")
            return child_dbs

    def detect_fields(self, database_id: str) -> Tuple[List[str], Optional[str]]:
        """
        自动检测数据库的字段

        Args:
            database_id: 数据库ID

        Returns:
            (link_fields, views_field) - URL字段列表和Views字段名
        """
        try:
            self.add_debug(f"\n=== 开始检测字段 ===")

            # 方法1: 尝试从数据库结构获取（可能失败，因为inline database没有properties）
            try:
                db_structure = self.get_database_structure(database_id)
                properties = db_structure.get('properties', {})

                if properties:
                    self.add_debug(f"从数据库结构获取到 {len(properties)} 个字段")
                else:
                    self.add_debug(f"数据库结构中properties为空，尝试从查询结果获取字段")
                    raise ValueError("properties为空")

            except:
                # 方法2: 从查询结果获取字段（适用于inline database）
                self.add_debug(f"从查询结果中获取字段...")
                results = self.query_database(database_id)

                if not results or len(results) == 0:
                    self.add_debug(f"数据库为空，无法检测字段")
                    return [], None

                # 从第一行数据中获取字段信息
                first_row = results[0]
                properties = first_row.get('properties', {})
                self.add_debug(f"从查询结果获取到 {len(properties)} 个字段")

            link_fields = []
            views_field = None

            for prop_name, prop_data in properties.items():
                prop_type = prop_data.get('type')

                # 查找所有URL类型字段（排除Views字段）
                if prop_type == 'url':
                    if 'view' not in prop_name.lower():
                        link_fields.append(prop_name)
                        self.add_debug(f"找到URL字段: {prop_name}")

                # 查找Views字段（Number类型）
                if prop_type == 'number' and ('view' in prop_name.lower()):
                    views_field = prop_name
                    self.add_debug(f"找到Views字段: {prop_name}")

            self.add_debug(f"\n检测结果:")
            self.add_debug(f"- URL字段: {link_fields}")
            self.add_debug(f"- Views字段: {views_field}")
            self.add_debug(f"===================\n")

            return link_fields, views_field

        except Exception as e:
            self.add_debug(f"字段检测失败: {str(e)}")
            raise

    def update_page_views(self, page_id: str, views_field: str, total_views: int):
        """
        更新页面的Views字段

        Args:
            page_id: 页面ID
            views_field: Views字段名称
            total_views: 总播放量
        """
        try:
            formatted_id = format_database_id(page_id)

            properties = {
                views_field: {
                    "number": total_views
                }
            }

            self.client.pages.update(
                page_id=formatted_id,
                properties=properties
            )

            self.add_debug(f"更新成功: {total_views} views")

        except Exception as e:
            self.add_debug(f"更新Views失败: {str(e)}")
            raise

    def get_all_creators(self, master_db_id: str) -> List[Dict]:
        """
        获取所有创作者

        Args:
            master_db_id: 主数据库ID

        Returns:
            创作者列表，每个包含 {'id': str, 'name': str, 'label': str}
        """
        try:
            self.add_debug(f"\n=== 开始获取所有创作者 ===")
            results = self.query_database(master_db_id)

            creators = []
            for page in results:
                page_id = page.get('id')

                # 获取创作者名称（从Title字段）
                properties = page.get('properties', {})
                creator_name = "Unknown"
                creator_label = ""

                # 查找Title类型的字段和Label字段
                for prop_name, prop_data in properties.items():
                    if prop_data.get('type') == 'title':
                        title_list = prop_data.get('title', [])
                        if title_list:
                            creator_name = title_list[0].get('plain_text', 'Unknown')

                    # 查找Label字段（可能是multi_select, select, 或 rich_text类型）
                    if 'label' in prop_name.lower():
                        prop_type = prop_data.get('type')

                        if prop_type == 'multi_select':
                            # multi_select类型，获取所有选项
                            multi_select_list = prop_data.get('multi_select', [])
                            if multi_select_list:
                                labels = [item.get('name', '') for item in multi_select_list]
                                creator_label = ', '.join(labels)

                        elif prop_type == 'select':
                            # select类型，获取单个选项
                            select_obj = prop_data.get('select')
                            if select_obj:
                                creator_label = select_obj.get('name', '')

                        elif prop_type == 'rich_text':
                            # rich_text类型
                            rich_text_list = prop_data.get('rich_text', [])
                            if rich_text_list:
                                creator_label = rich_text_list[0].get('plain_text', '')

                creators.append({
                    'id': page_id,
                    'name': creator_name,
                    'label': creator_label
                })

                self.add_debug(f"找到创作者: {creator_name} (Label: {creator_label}, ID: {page_id})")

            self.add_debug(f"总共找到 {len(creators)} 个创作者")
            self.add_debug(f"===================\n")

            return creators

        except Exception as e:
            self.add_debug(f"获取创作者列表失败: {str(e)}")
            raise

    def get_video_rows(self, database_id: str, link_fields: List[str], views_field: str) -> List[Dict]:
        """
        获取数据库中的所有视频行

        Args:
            database_id: 数据库ID
            link_fields: URL字段列表
            views_field: Views字段名称

        Returns:
            视频行列表，每个包含 {'id': str, 'name': str, 'links': List[str], 'current_views': int}
        """
        try:
            results = self.query_database(database_id)

            video_rows = []
            for page in results:
                page_id = page.get('id')
                properties = page.get('properties', {})

                # 获取视频名称
                video_name = "Unknown"
                for prop_name, prop_data in properties.items():
                    if prop_data.get('type') == 'title':
                        title_list = prop_data.get('title', [])
                        if title_list:
                            video_name = title_list[0].get('plain_text', 'Unknown')
                        break

                # 获取所有链接
                links = []
                for field in link_fields:
                    if field in properties:
                        url = properties[field].get('url')
                        if url:
                            links.append(url)

                # 获取当前Views
                current_views = 0
                if views_field and views_field in properties:
                    current_views = properties[views_field].get('number', 0) or 0

                # 只处理有链接的行
                if links:
                    video_rows.append({
                        'id': page_id,
                        'name': video_name,
                        'links': links,
                        'current_views': current_views
                    })
                    self.add_debug(f"视频: {video_name}, 链接数: {len(links)}, 当前Views: {current_views}")

            self.add_debug(f"找到 {len(video_rows)} 个视频行")
            return video_rows

        except Exception as e:
            self.add_debug(f"获取视频行失败: {str(e)}")
            raise

    def process_creator_tables(self, creator_id: str, creator_name: str, scraper) -> Dict:
        """
        处理单个创作者的所有表格

        Args:
            creator_id: 创作者页面ID
            creator_name: 创作者名称
            scraper: ViewScraper实例

        Returns:
            处理结果统计 {'tables_found': int, 'videos_updated': int, 'total_views': int}
        """
        stats = {
            'tables_found': 0,
            'videos_updated': 0,
            'total_views': 0,
            'errors': []
        }

        try:
            self.add_debug(f"\n{'='*60}")
            self.add_debug(f"处理创作者: {creator_name}")
            self.add_debug(f"{'='*60}")

            # 查找子数据库
            child_dbs = self.find_child_databases(creator_id)

            if not child_dbs:
                self.add_debug(f"创作者 {creator_name} 没有子表格，跳过")
                return stats

            stats['tables_found'] = len(child_dbs)

            # 处理每个子表格
            for idx, child_db in enumerate(child_dbs, 1):
                self.add_debug(f"\n--- 处理第 {idx} 个表格 ---")
                db_id = child_db['id']

                try:
                    # 自动检测字段
                    link_fields, views_field = self.detect_fields(db_id)

                    if not link_fields:
                        self.add_debug(f"表格没有URL字段，跳过")
                        continue

                    if not views_field:
                        self.add_debug(f"警告: 没有找到Views字段，将无法更新")
                        continue

                    # 获取所有视频行
                    video_rows = self.get_video_rows(db_id, link_fields, views_field)

                    # 处理每个视频
                    for video in video_rows:
                        self.add_debug(f"\n处理视频: {video['name']}")

                        total_views = 0
                        success_count = 0

                        # 爬取所有链接的播放量
                        for link in video['links']:
                            views = scraper.scrape_views(link)
                            if views is not None:
                                total_views += views
                                success_count += 1
                                self.add_debug(f"  {link}: {views} views")
                            else:
                                self.add_debug(f"  {link}: 爬取失败")

                        # 更新到Notion
                        if success_count > 0:
                            try:
                                self.update_page_views(video['id'], views_field, total_views)
                                stats['videos_updated'] += 1
                                stats['total_views'] += total_views
                                self.add_debug(f"✓ 更新成功: {video['name']} → {total_views} views")
                            except Exception as e:
                                error_msg = f"更新失败: {video['name']} - {str(e)}"
                                self.add_debug(f"✗ {error_msg}")
                                stats['errors'].append(error_msg)
                        else:
                            error_msg = f"所有链接爬取失败: {video['name']}"
                            self.add_debug(f"✗ {error_msg}")
                            stats['errors'].append(error_msg)

                except Exception as e:
                    error_msg = f"处理表格失败: {str(e)}"
                    self.add_debug(f"✗ {error_msg}")
                    stats['errors'].append(error_msg)

            self.add_debug(f"\n创作者 {creator_name} 处理完成:")
            self.add_debug(f"- 找到表格: {stats['tables_found']}")
            self.add_debug(f"- 更新视频: {stats['videos_updated']}")
            self.add_debug(f"- 总播放量: {stats['total_views']}")

            return stats

        except Exception as e:
            error_msg = f"处理创作者失败: {creator_name} - {str(e)}"
            self.add_debug(f"✗ {error_msg}")
            stats['errors'].append(error_msg)
            return stats

    def batch_update_all_creators(self, master_db_id: str, scraper, delay: float = 2.0) -> Dict:
        """
        批量更新所有创作者的视频播放量

        Args:
            master_db_id: 主数据库ID
            scraper: ViewScraper实例
            delay: 每个视频之间的延迟（秒）

        Returns:
            总体统计结果，包含creator_details列表
        """
        total_stats = {
            'creators_processed': 0,
            'tables_found': 0,
            'videos_updated': 0,
            'total_views': 0,
            'errors': [],
            'creator_details': []  # 新增：存储每个创作者的详细信息
        }

        try:
            # 获取所有创作者
            creators = self.get_all_creators(master_db_id)

            if not creators:
                self.add_debug("没有找到任何创作者")
                return total_stats

            # 处理每个创作者
            for idx, creator in enumerate(creators, 1):
                self.add_debug(f"\n\n{'#'*60}")
                self.add_debug(f"进度: {idx}/{len(creators)}")
                self.add_debug(f"{'#'*60}")

                stats = self.process_creator_tables(
                    creator['id'],
                    creator['name'],
                    scraper
                )

                # 保存创作者详细信息
                creator_detail = {
                    'name': creator['name'],
                    'label': creator['label'],
                    'videos_updated': stats['videos_updated'],
                    'total_views': stats['total_views']
                }
                total_stats['creator_details'].append(creator_detail)

                total_stats['creators_processed'] += 1
                total_stats['tables_found'] += stats['tables_found']
                total_stats['videos_updated'] += stats['videos_updated']
                total_stats['total_views'] += stats['total_views']
                total_stats['errors'].extend(stats['errors'])

                # 延迟，避免请求过快
                if idx < len(creators):
                    time.sleep(delay)

            # 输出总结
            self.add_debug(f"\n\n{'='*60}")
            self.add_debug(f"批量更新完成！")
            self.add_debug(f"{'='*60}")
            self.add_debug(f"处理创作者: {total_stats['creators_processed']}")
            self.add_debug(f"找到表格: {total_stats['tables_found']}")
            self.add_debug(f"更新视频: {total_stats['videos_updated']}")
            self.add_debug(f"总播放量: {total_stats['total_views']}")
            self.add_debug(f"错误数量: {len(total_stats['errors'])}")

            return total_stats

        except Exception as e:
            error_msg = f"批量更新失败: {str(e)}\n{traceback.format_exc()}"
            self.add_debug(f"✗ {error_msg}")
            total_stats['errors'].append(error_msg)
            return total_stats
