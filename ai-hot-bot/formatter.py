"""
格式化输出模块
将推文数据格式化为 Markdown 报告
"""

from datetime import datetime, timedelta
from typing import List, Dict


class ReportFormatter:
    """报告格式化器"""

    @staticmethod
    def format_number(num: int) -> str:
        """
        格式化数字（例如：15200 -> 15.2K）

        Args:
            num: 数字

        Returns:
            格式化后的字符串
        """
        if num >= 1000000:
            return f"{num / 1000000:.1f}M"
        elif num >= 1000:
            return f"{num / 1000:.1f}K"
        else:
            return str(num)

    @staticmethod
    def format_timestamp(created_at) -> str:
        """
        格式化时间戳

        Args:
            created_at: 推文创建时间

        Returns:
            格式化后的时间字符串
        """
        if isinstance(created_at, str):
            return created_at
        return created_at.strftime("%Y-%m-%d %H:%M UTC")

    @staticmethod
    def truncate_text(text: str, max_length: int = 280) -> str:
        """
        截断过长的文本

        Args:
            text: 原文本
            max_length: 最大长度

        Returns:
            截断后的文本
        """
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."

    @staticmethod
    def generate_report(
        top_tweets: List[Dict],
        ai_insight: str,
        report_date: str = None,
        hours_ago: int = 48,
        total_accounts: int = 0,
        total_tweets: int = 0
    ) -> str:
        """
        生成完整的 Markdown 报告

        Args:
            top_tweets: Top N 热门推文
            ai_insight: AI 解读
            report_date: 报告日期
            hours_ago: 时间范围（小时）
            total_accounts: 监控账号总数
            total_tweets: 符合条件的推文总数

        Returns:
            Markdown 格式的报告
        """
        if not report_date:
            report_date = datetime.now().strftime("%Y年%m月%d日")

        # 计算时间范围
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours_ago)
        time_range = f"{start_time.strftime('%Y-%m-%d %H:%M')} ~ {end_time.strftime('%Y-%m-%d %H:%M')}"

        # 开始生成报告
        report_lines = [
            "# 🤖 AI热报",
            "",
            f"**日期**：{report_date}",
            f"**数据范围**：{time_range} ({hours_ago}小时)",
            "",
            "---",
            "",
            "## 📊 今日热点解读",
            "",
            ai_insight,
            "",
            "---",
            "",
            "## 🔥 Top 10 热门推文",
            ""
        ]

        # 生成每条推文的内容
        for i, tweet in enumerate(top_tweets, 1):
            emoji_map = {
                1: "1️⃣", 2: "2️⃣", 3: "3️⃣", 4: "4️⃣", 5: "5️⃣",
                6: "6️⃣", 7: "7️⃣", 8: "8️⃣", 9: "9️⃣", 10: "🔟"
            }

            report_lines.extend([
                f"### {emoji_map.get(i, i)} 第{i}名",
                "",
                f"**发帖账号**：[@{tweet['username']}](https://twitter.com/{tweet['username']})",
                f"**发帖时间**：{ReportFormatter.format_timestamp(tweet['created_at'])}",
                "",
                "**帖子原文**：",
                "",
                f"> {ReportFormatter.truncate_text(tweet['text'])}",
                "",
                "**原帖互动**："
            ])

            # 互动数据
            metrics = [
                f"👍 Like: {ReportFormatter.format_number(tweet['like_count'])}",
                f"🔁 Repost: {ReportFormatter.format_number(tweet['retweet_count'])}",
                f"💬 Reply: {ReportFormatter.format_number(tweet['reply_count'])}"
            ]

            if tweet.get('impression_count', 0) > 0:
                metrics.append(f"👀 View: {ReportFormatter.format_number(tweet['impression_count'])}")

            report_lines.append(" | ".join(metrics))
            report_lines.extend([
                "",
                f"🔗 **原推链接**：{tweet['url']}",
                "",
                "---",
                ""
            ])

        # 添加统计信息
        report_lines.extend([
            "## 📈 数据统计",
            "",
            f"- 🔍 监控账号数：{total_accounts} 个",
            f"- 📝 符合条件推文：{total_tweets} 条",
            f"- ⏰ 筛选条件：点赞 ≥ 100",
            f"- 📅 时间范围：最近 {hours_ago} 小时",
            "",
            "---",
            "",
            f"⏰ **生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
            "",
            "🤖 由 **AI热推bot** 自动生成 | 数据来源：Twitter/X"
        ])

        return "\n".join(report_lines)
