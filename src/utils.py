"""
工具函数模块
包含数据存储、结算计算等功能
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd


class SettlementCalculator:
    """结算计算器"""

    def __init__(self):
        """初始化结算计算器"""
        self.base_pay_large = 20  # 大UGC底薪（$/条）
        self.base_pay_small = 10  # 小UGC底薪（$/条）
        self.commission_rate = 1  # 每1000 views = $1

    def calculate_commission(self, total_views: int) -> float:
        """
        计算提成 - 按1000为最小单位，向下取整

        Args:
            total_views: 总播放量

        Returns:
            提成金额（$）
        """
        # 向下取整到1000，例如: 2800 views -> 2000 views -> $2
        thousands = int(total_views / 1000)
        return thousands * self.commission_rate

    def calculate_settlement(self, video_count: int, total_views: int, label: str = '') -> Dict:
        """
        计算结算金额

        Args:
            video_count: 视频数量
            total_views: 总播放量
            label: 创作者标签（CoreUGC或DiscordUGC）

        Returns:
            结算详情 {'base_pay': float, 'commission': float, 'total': float}
        """
        # 根据label判断是否为大UGC
        # Core UGC = 大UGC ($20/条)
        # discord ugc = 小UGC ($10/条)
        # 移除空格后进行比较，因为Notion中的label可能是 "Core UGC" (带空格)
        label_lower = label.lower().replace(' ', '')
        is_large_ugc = 'coreugc' in label_lower

        base_pay = video_count * (self.base_pay_large if is_large_ugc else self.base_pay_small)
        commission = self.calculate_commission(total_views)
        total = base_pay + commission

        return {
            'video_count': video_count,
            'total_views': total_views,
            'base_pay': base_pay,
            'commission': commission,
            'total': total,
            'ugc_type': 'Core UGC ($20/video)' if is_large_ugc else 'Discord UGC ($10/video)',
            'label': label
        }

    def calculate_monthly_settlement(self, creators_data: List[Dict], year: int, month: int) -> pd.DataFrame:
        """
        计算月度结算

        Args:
            creators_data: 创作者数据列表
                [{'name': str, 'videos': List[Dict], 'label': str}, ...]
                videos: [{'date': str, 'views': int}, ...]
            year: 年份
            month: 月份

        Returns:
            结算数据DataFrame
        """
        settlements = []

        for creator in creators_data:
            name = creator.get('name', 'Unknown')
            label = creator.get('label', '')
            videos = creator.get('videos', [])

            # 筛选指定月份的视频
            monthly_videos = []
            for video in videos:
                try:
                    video_date = parse_video_date(video.get('date', ''))
                    if video_date and video_date.year == year and video_date.month == month:
                        monthly_videos.append(video)
                except:
                    continue

            # 计算总播放量
            total_views = sum(v.get('views', 0) for v in monthly_videos)
            video_count = len(monthly_videos)

            if video_count > 0:
                # 计算结算，传入label而不是is_large_ugc
                settlement = self.calculate_settlement(video_count, total_views, label)
                settlement['creator'] = name
                settlement['year'] = year
                settlement['month'] = month
                settlements.append(settlement)

        # 转换为DataFrame
        if settlements:
            df = pd.DataFrame(settlements)
            df = df[['creator', 'label', 'ugc_type', 'video_count', 'total_views',
                     'base_pay', 'commission', 'total', 'year', 'month']]
            return df
        else:
            return pd.DataFrame()


class DataStorage:
    """数据存储管理器"""

    def __init__(self, data_dir: str = './data'):
        """
        初始化数据存储

        Args:
            data_dir: 数据存储目录
        """
        self.data_dir = data_dir
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        """确保数据目录存在"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def save_settlement_record(self, settlement_df: pd.DataFrame, year: int, month: int):
        """
        保存结算记录

        Args:
            settlement_df: 结算数据DataFrame
            year: 年份
            month: 月份
        """
        filename = f"settlement_{year}_{month:02d}.csv"
        filepath = os.path.join(self.data_dir, filename)

        settlement_df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"结算记录已保存: {filepath}")

    def load_settlement_record(self, year: int, month: int) -> Optional[pd.DataFrame]:
        """
        加载结算记录

        Args:
            year: 年份
            month: 月份

        Returns:
            结算数据DataFrame，不存在返回None
        """
        filename = f"settlement_{year}_{month:02d}.csv"
        filepath = os.path.join(self.data_dir, filename)

        if os.path.exists(filepath):
            # 检查文件是否为空
            if os.path.getsize(filepath) == 0:
                print(f"警告: 文件 {filepath} 是空的")
                return None

            # 检查文件内容是否只有少量字节（可能只有BOM或空行）
            if os.path.getsize(filepath) < 10:
                print(f"警告: 文件 {filepath} 内容太少，可能损坏")
                return None

            try:
                return pd.read_csv(filepath, encoding='utf-8-sig')
            except pd.errors.EmptyDataError:
                print(f"警告: 文件 {filepath} 无法解析（EmptyDataError）")
                return None
        else:
            return None

    def list_settlement_records(self) -> List[Dict]:
        """
        列出所有结算记录

        Returns:
            记录列表 [{'year': int, 'month': int, 'filepath': str}, ...]
        """
        records = []

        if not os.path.exists(self.data_dir):
            return records

        for filename in os.listdir(self.data_dir):
            if filename.startswith('settlement_') and filename.endswith('.csv'):
                try:
                    parts = filename.replace('settlement_', '').replace('.csv', '').split('_')
                    year = int(parts[0])
                    month = int(parts[1])
                    records.append({
                        'year': year,
                        'month': month,
                        'filepath': os.path.join(self.data_dir, filename)
                    })
                except:
                    continue

        # 按年月排序
        records.sort(key=lambda x: (x['year'], x['month']), reverse=True)
        return records

    def save_config(self, config: Dict):
        """
        保存配置

        Args:
            config: 配置字典
        """
        filepath = os.path.join(self.data_dir, 'config.json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def load_config(self) -> Optional[Dict]:
        """
        加载配置

        Returns:
            配置字典，不存在返回None
        """
        filepath = os.path.join(self.data_dir, 'config.json')
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def save_update_log(self, log_entry: Dict):
        """
        保存更新日志

        Args:
            log_entry: 日志条目
                {'timestamp': str, 'action': str, 'details': Dict}
        """
        filepath = os.path.join(self.data_dir, 'update_log.jsonl')

        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    def load_update_logs(self, limit: int = 100) -> List[Dict]:
        """
        加载更新日志

        Args:
            limit: 最多返回的日志条数

        Returns:
            日志列表
        """
        filepath = os.path.join(self.data_dir, 'update_log.jsonl')

        if not os.path.exists(filepath):
            return []

        logs = []
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    logs.append(json.loads(line))
                except:
                    continue

        # 返回最新的N条
        return logs[-limit:]


def format_number(number: float, decimals: int = 0) -> str:
    """
    格式化数字，添加千位分隔符

    Args:
        number: 数字
        decimals: 小数位数

    Returns:
        格式化后的字符串
    """
    if decimals > 0:
        return f"{number:,.{decimals}f}"
    else:
        return f"{int(number):,}"


def parse_video_date(date_str: str) -> Optional[datetime]:
    """
    解析视频日期字符串

    支持格式:
    - "20251114", "2025-11-14", "2025/11/14"
    - "20251114-1", "20251114-2" (同一天多个视频)
    - "20251114_01", "20251114a" (其他序号格式)

    Args:
        date_str: 日期字符串

    Returns:
        datetime对象，解析失败返回None
    """
    import re

    # 如果包含序号后缀，先提取日期部分
    # 匹配模式: 日期后面跟着 -/_ 或字母
    # 例如: 20251114-1, 20251114_01, 20251114a
    date_part = date_str

    # 尝试提取前8位数字（YYYYMMDD格式）
    match = re.match(r'^(\d{8})', date_str)
    if match:
        date_part = match.group(1)

    formats = [
        '%Y%m%d',
        '%Y-%m-%d',
        '%Y/%m/%d',
        '%Y.%m.%d'
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_part, fmt)
        except:
            continue

    return None


def get_month_range(year: int, month: int) -> tuple:
    """
    获取月份的日期范围

    Args:
        year: 年份
        month: 月份

    Returns:
        (start_date, end_date) - datetime对象元组
    """
    from calendar import monthrange

    start_date = datetime(year, month, 1)
    last_day = monthrange(year, month)[1]
    end_date = datetime(year, month, last_day, 23, 59, 59)

    return start_date, end_date


# 测试代码
if __name__ == "__main__":
    # 测试结算计算器
    calculator = SettlementCalculator()

    # 测试单个结算
    result = calculator.calculate_settlement(
        video_count=10,
        total_views=50000,
        is_large_ugc=True
    )
    print("结算测试:")
    print(f"视频数: {result['video_count']}")
    print(f"总播放量: {format_number(result['total_views'])}")
    print(f"底薪: ¥{result['base_pay']}")
    print(f"提成: ¥{result['commission']:.2f}")
    print(f"总计: ¥{result['total']:.2f}")

    # 测试数据存储
    storage = DataStorage()
    print("\n数据存储目录:", storage.data_dir)
