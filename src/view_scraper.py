"""
播放量爬取模块
支持从Instagram和TikTok爬取视频播放量
"""

import requests
from bs4 import BeautifulSoup
import re
import json
import time
from typing import Optional
import traceback


class ViewScraper:
    """视频播放量爬取器"""

    def __init__(self, delay: float = 2.0):
        """
        初始化爬取器

        Args:
            delay: 每次请求之间的延迟（秒），避免被封禁
        """
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def identify_platform(self, url: str) -> str:
        """
        识别链接所属的平台

        Args:
            url: 视频链接

        Returns:
            平台名称 ('instagram', 'tiktok', 'unknown')
        """
        url_lower = url.lower()
        if 'instagram.com' in url_lower or 'instagr.am' in url_lower:
            return 'instagram'
        elif 'tiktok.com' in url_lower:
            return 'tiktok'
        else:
            return 'unknown'

    def scrape_instagram_views(self, url: str) -> Optional[int]:
        """
        从Instagram爬取播放量

        Args:
            url: Instagram视频链接

        Returns:
            播放量（整数），失败返回None
        """
        try:
            print(f"[Instagram] 开始爬取: {url}")

            # 发送请求
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # 方法1: 从meta标签提取
            meta_description = soup.find('meta', {'property': 'og:description'})
            if meta_description:
                content = meta_description.get('content', '')
                # 匹配 "X views" 或 "X,XXX views" 或 "X万 views"
                matches = re.findall(r'([\d,]+(?:\.\d+)?[万千百]?)\s*(?:views?|次播放)', content, re.IGNORECASE)
                if matches:
                    views_str = matches[0]
                    views = self._parse_views_number(views_str)
                    if views is not None:
                        print(f"[Instagram] ✓ 从meta标签获取: {views} views")
                        return views

            # 方法2: 从页面JSON数据提取
            scripts = soup.find_all('script', {'type': 'application/ld+json'})
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    if isinstance(data, dict):
                        # 查找interactionStatistic
                        if 'interactionStatistic' in data:
                            for stat in data['interactionStatistic']:
                                if stat.get('interactionType') == 'http://schema.org/WatchAction':
                                    views = int(stat.get('userInteractionCount', 0))
                                    print(f"[Instagram] ✓ 从JSON-LD获取: {views} views")
                                    return views
                except:
                    continue

            # 方法3: 从页面文本搜索
            page_text = soup.get_text()
            matches = re.findall(r'([\d,]+(?:\.\d+)?[万千百]?)\s*(?:views?|次播放)', page_text, re.IGNORECASE)
            if matches:
                views_str = matches[0]
                views = self._parse_views_number(views_str)
                if views is not None:
                    print(f"[Instagram] ✓ 从页面文本获取: {views} views")
                    return views

            print(f"[Instagram] ✗ 未找到播放量数据")
            return None

        except requests.Timeout:
            print(f"[Instagram] ✗ 请求超时")
            return None
        except requests.RequestException as e:
            print(f"[Instagram] ✗ 请求失败: {str(e)}")
            return None
        except Exception as e:
            print(f"[Instagram] ✗ 爬取失败: {str(e)}")
            print(traceback.format_exc())
            return None

    def scrape_tiktok_views(self, url: str) -> Optional[int]:
        """
        从TikTok爬取播放量

        Args:
            url: TikTok视频链接

        Returns:
            播放量（整数），失败返回None
        """
        try:
            print(f"[TikTok] 开始爬取: {url}")

            # 发送请求
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # 方法1: 从meta标签提取
            meta_description = soup.find('meta', {'property': 'og:description'})
            if meta_description:
                content = meta_description.get('content', '')
                # 匹配 "X views" 或 "X,XXX views" 或 "X.XM views"
                matches = re.findall(r'([\d.]+[KMB]?)\s*(?:views?)', content, re.IGNORECASE)
                if matches:
                    views_str = matches[0]
                    views = self._parse_views_number(views_str)
                    if views is not None:
                        print(f"[TikTok] ✓ 从meta标签获取: {views} views")
                        return views

            # 方法2: 从script标签中的JSON数据提取
            scripts = soup.find_all('script', {'id': '__UNIVERSAL_DATA_FOR_REHYDRATION__'})
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    # TikTok的数据结构: __DEFAULT_SCOPE__.__SIGI_STATE__.ItemModule
                    if '__DEFAULT_SCOPE__' in data:
                        scope = data['__DEFAULT_SCOPE__']
                        if 'webapp.video-detail' in scope:
                            video_detail = scope['webapp.video-detail']
                            if 'itemInfo' in video_detail and 'itemStruct' in video_detail['itemInfo']:
                                stats = video_detail['itemInfo']['itemStruct'].get('stats', {})
                                views = int(stats.get('playCount', 0))
                                if views > 0:
                                    print(f"[TikTok] ✓ 从JSON数据获取: {views} views")
                                    return views
                except:
                    continue

            # 方法3: 从SIGI_STATE提取
            scripts = soup.find_all('script', {'id': 'SIGI_STATE'})
            for script in scripts:
                try:
                    data = json.loads(script.string)
                    # 查找ItemModule
                    if 'ItemModule' in data:
                        for item_id, item_data in data['ItemModule'].items():
                            if 'stats' in item_data:
                                views = int(item_data['stats'].get('playCount', 0))
                                if views > 0:
                                    print(f"[TikTok] ✓ 从SIGI_STATE获取: {views} views")
                                    return views
                except:
                    continue

            # 方法4: 从页面文本搜索
            page_text = soup.get_text()
            matches = re.findall(r'([\d.]+[KMB]?)\s*(?:views?)', page_text, re.IGNORECASE)
            if matches:
                views_str = matches[0]
                views = self._parse_views_number(views_str)
                if views is not None:
                    print(f"[TikTok] ✓ 从页面文本获取: {views} views")
                    return views

            print(f"[TikTok] ✗ 未找到播放量数据")
            return None

        except requests.Timeout:
            print(f"[TikTok] ✗ 请求超时")
            return None
        except requests.RequestException as e:
            print(f"[TikTok] ✗ 请求失败: {str(e)}")
            return None
        except Exception as e:
            print(f"[TikTok] ✗ 爬取失败: {str(e)}")
            print(traceback.format_exc())
            return None

    def _parse_views_number(self, views_str: str) -> Optional[int]:
        """
        解析播放量字符串为整数

        支持格式:
        - "1,234,567" → 1234567
        - "1.2M" → 1200000
        - "1.2K" → 1200
        - "1.2B" → 1200000000
        - "1.2万" → 12000

        Args:
            views_str: 播放量字符串

        Returns:
            播放量整数，解析失败返回None
        """
        try:
            views_str = views_str.strip().replace(',', '')

            # 处理K/M/B后缀
            multipliers = {
                'K': 1000,
                'M': 1000000,
                'B': 1000000000,
                '千': 1000,
                '万': 10000,
                '百万': 1000000,
                '亿': 100000000
            }

            for suffix, multiplier in multipliers.items():
                if views_str.upper().endswith(suffix.upper()):
                    number_str = views_str[:-len(suffix)].strip()
                    number = float(number_str)
                    return int(number * multiplier)

            # 直接转换为整数
            return int(float(views_str))

        except:
            return None

    def scrape_views(self, url: str) -> Optional[int]:
        """
        自动识别平台并爬取播放量

        Args:
            url: 视频链接

        Returns:
            播放量（整数），失败返回None
        """
        if not url:
            return None

        platform = self.identify_platform(url)

        views = None
        if platform == 'instagram':
            views = self.scrape_instagram_views(url)
        elif platform == 'tiktok':
            views = self.scrape_tiktok_views(url)
        else:
            print(f"[Unknown] 不支持的平台: {url}")
            return None

        # 延迟，避免请求过快
        time.sleep(self.delay)

        return views

    def test_scraper(self, test_urls: list):
        """
        测试爬取器

        Args:
            test_urls: 测试URL列表
        """
        print("\n=== 开始测试爬取器 ===\n")

        for url in test_urls:
            print(f"\n测试URL: {url}")
            platform = self.identify_platform(url)
            print(f"识别平台: {platform}")

            views = self.scrape_views(url)
            if views is not None:
                print(f"✓ 成功: {views:,} views")
            else:
                print(f"✗ 失败")

            print("-" * 60)

        print("\n=== 测试完成 ===\n")


# 测试代码
if __name__ == "__main__":
    # 创建爬取器实例
    scraper = ViewScraper(delay=2.0)

    # 测试URL（替换为实际的URL）
    test_urls = [
        # "https://www.instagram.com/reel/xxxxx/",
        # "https://www.tiktok.com/@username/video/xxxxx",
    ]

    if test_urls:
        scraper.test_scraper(test_urls)
    else:
        print("请在test_urls中添加测试URL")
