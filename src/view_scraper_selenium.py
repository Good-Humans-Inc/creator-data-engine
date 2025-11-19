"""
播放量爬取模块 - Selenium版本
使用真实浏览器爬取Instagram和TikTok播放量
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
from typing import Optional


class ViewScraperSelenium:
    """使用Selenium的播放量爬取器"""

    def __init__(self, delay: float = 2.0, headless: bool = True):
        """
        初始化爬取器

        Args:
            delay: 每次请求之间的延迟（秒）
            headless: 是否使用无头模式
        """
        self.delay = delay
        self.headless = headless
        self.driver = None

    def _init_driver(self):
        """初始化Chrome驱动"""
        if self.driver is None:
            chrome_options = Options()

            if self.headless:
                chrome_options.add_argument('--headless=new')

            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(30)

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def identify_platform(self, url: str) -> str:
        """识别平台"""
        url_lower = url.lower()
        if 'instagram.com' in url_lower or 'instagr.am' in url_lower:
            return 'instagram'
        elif 'tiktok.com' in url_lower:
            return 'tiktok'
        else:
            return 'unknown'

    def scrape_instagram_views(self, url: str) -> Optional[int]:
        """从Instagram爬取播放量"""
        try:
            print(f"[Instagram] 开始爬取: {url}")

            self._init_driver()
            self.driver.get(url)

            # 等待页面加载
            time.sleep(3)

            # 方法1: 查找包含"views"文本的元素
            try:
                # Instagram Reels的播放量通常在特定的span或div中
                page_source = self.driver.page_source

                # 匹配各种可能的播放量格式
                patterns = [
                    r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?[KMB]?)\s*(?:views?|次播放)',
                    r'videoViewCount["\']?\s*:\s*["\']?(\d+)',
                    r'"viewCount"\s*:\s*(\d+)',
                ]

                for pattern in patterns:
                    matches = re.findall(pattern, page_source, re.IGNORECASE)
                    if matches:
                        views_str = matches[0]
                        views = self._parse_views_number(views_str)
                        if views and views > 0:
                            print(f"[Instagram] ✓ 成功: {views:,} views")
                            return views

            except Exception as e:
                print(f"[Instagram] 查找失败: {str(e)}")

            print(f"[Instagram] ✗ 未找到播放量数据")
            return None

        except Exception as e:
            print(f"[Instagram] ✗ 错误: {str(e)}")
            return None

    def scrape_tiktok_views(self, url: str) -> Optional[int]:
        """从TikTok爬取播放量"""
        try:
            print(f"[TikTok] 开始爬取: {url}")

            self._init_driver()
            self.driver.get(url)

            # 等待页面加载
            time.sleep(3)

            # 方法1: 从页面源码中提取
            try:
                page_source = self.driver.page_source

                # TikTok的播放量可能在JSON数据中
                patterns = [
                    r'"playCount["\']?\s*:\s*["\']?(\d+)',
                    r'"viewCount["\']?\s*:\s*["\']?(\d+)',
                    r'(\d+(?:\.\d+)?[KMB]?)\s*views?',
                ]

                for pattern in patterns:
                    matches = re.findall(pattern, page_source, re.IGNORECASE)
                    if matches:
                        views_str = matches[0]
                        views = self._parse_views_number(views_str)
                        if views and views > 0:
                            print(f"[TikTok] ✓ 成功: {views:,} views")
                            return views

            except Exception as e:
                print(f"[TikTok] 查找失败: {str(e)}")

            print(f"[TikTok] ✗ 未找到播放量数据")
            return None

        except Exception as e:
            print(f"[TikTok] ✗ 错误: {str(e)}")
            return None

    def _parse_views_number(self, views_str: str) -> Optional[int]:
        """解析播放量字符串为整数"""
        try:
            views_str = str(views_str).strip().replace(',', '')

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
        """自动识别平台并爬取播放量"""
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

        # 延迟
        time.sleep(self.delay)

        return views


# 测试代码
if __name__ == "__main__":
    scraper = ViewScraperSelenium(delay=2.0, headless=False)

    test_urls = [
        "https://www.instagram.com/reel/DRD0cSOiecS/?igsh=MzRlODBiNWFlZA==",
        "https://www.tiktok.com/t/ZTMTXDrt7/",
    ]

    try:
        for url in test_urls:
            print(f"\n测试: {url}")
            views = scraper.scrape_views(url)
            if views:
                print(f"✅ 结果: {views:,} views")
            else:
                print(f"❌ 失败")
            print("-" * 60)
    finally:
        scraper.close()
