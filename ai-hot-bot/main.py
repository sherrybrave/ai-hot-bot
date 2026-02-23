#!/usr/bin/env python3
"""
AI热推bot - 主程序
每天自动生成AI领域热门推文报告
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# 添加当前目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from twitter_api import TwitterFetcher
from zhipu_ai import ZhipuAnalyzer
from formatter import ReportFormatter


def load_accounts(file_path: str) -> list:
    """
    加载账号列表

    Args:
        file_path: 账号文件路径

    Returns:
        账号名列表
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        accounts = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return accounts


def main():
    """主函数"""
    print("=" * 60)
    print("🤖 AI热推bot - 启动")
    print("=" * 60)

    # 环境变量
    TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')
    ZHIPU_API_KEY = os.getenv('ZHIPU_API_KEY')

    # 检查环境变量
    if not TWITTER_BEARER_TOKEN:
        print("❌ 错误: 未设置 TWITTER_BEARER_TOKEN 环境变量")
        sys.exit(1)

    if not ZHIPU_API_KEY:
        print("❌ 错误: 未设置 ZHIPU_API_KEY 环境变量")
        sys.exit(1)

    # 配置参数
    ACCOUNTS_FILE = os.path.join(os.path.dirname(__file__), 'accounts.txt')
    HOURS_AGO = 48
    MIN_LIKES = 100
    TOP_N = 10

    # 创建输出目录
    reports_dir = Path(__file__).parent.parent / 'reports'
    reports_dir.mkdir(exist_ok=True)

    try:
        # 1. 加载账号列表
        print(f"\n📋 加载账号列表: {ACCOUNTS_FILE}")
        accounts = load_accounts(ACCOUNTS_FILE)
        print(f"✅ 成功加载 {len(accounts)} 个账号")

        # 2. 获取推文数据
        fetcher = TwitterFetcher(bearer_token=TWITTER_BEARER_TOKEN)
        all_tweets = fetcher.get_all_tweets(
            usernames=accounts,
            hours_ago=HOURS_AGO,
            min_likes=MIN_LIKES
        )

        if not all_tweets:
            print("\n⚠️  未找到符合条件的推文，程序退出")
            sys.exit(0)

        # 3. 排序并取 Top N
        print(f"\n📊 按互动量排序，取 Top {TOP_N}...")
        top_tweets = fetcher.sort_by_engagement(all_tweets)[:TOP_N]

        # 4. 生成 AI 解读
        analyzer = ZhipuAnalyzer(api_key=ZHIPU_API_KEY)
        ai_insight = analyzer.generate_insight(top_tweets, num_tweets=TOP_N)

        # 5. 格式化报告
        print(f"\n📝 生成 Markdown 报告...")
        formatter = ReportFormatter()
        report_date = datetime.now().strftime("%Y年%m月%d日")
        report_content = formatter.generate_report(
            top_tweets=top_tweets,
            ai_insight=ai_insight,
            report_date=report_date,
            hours_ago=HOURS_AGO,
            total_accounts=len(accounts),
            total_tweets=len(all_tweets)
        )

        # 6. 保存报告
        report_filename = f"ai-hot-report-{datetime.now().strftime('%Y-%m-%d')}.md"
        report_path = reports_dir / report_filename

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"✅ 报告已保存: {report_path}")

        # 7. 输出到控制台（用于 GitHub Actions 日志）
        print("\n" + "=" * 60)
        print("📋 报告内容预览：")
        print("=" * 60)
        print(report_content)
        print("=" * 60)

        print(f"\n✅ AI热推bot 运行完成！")

    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
