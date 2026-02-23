"""
Twitter API v2 封装模块
用于获取指定账号的推文数据
"""

import tweepy
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os


class TwitterFetcher:
    """Twitter 数据获取器"""

    def __init__(self, bearer_token: str):
        """
        初始化 Twitter API 客户端

        Args:
            bearer_token: Twitter API Bearer Token
        """
        self.client = tweepy.Client(bearer_token=bearer_token)

    def get_user_id(self, username: str) -> Optional[str]:
        """
        根据用户名获取用户ID

        Args:
            username: Twitter 用户名（不含@）

        Returns:
            用户ID，如果获取失败返回 None
        """
        try:
            user = self.client.get_user(username=username)
            if user.data:
                return user.data.id
            return None
        except Exception as e:
            print(f"⚠️  获取用户 @{username} ID失败: {e}")
            return None

    def get_user_tweets(self, username: str, hours_ago: int = 48, min_likes: int = 100) -> List[Dict]:
        """
        获取指定用户最近N小时内的推文（点赞数 ≥ 指定值）

        Args:
            username: Twitter 用户名
            hours_ago: 获取多少小时内的推文
            min_likes: 最小点赞数

        Returns:
            推文列表
        """
        try:
            # 先获取用户ID
            user_id = self.get_user_id(username)
            if not user_id:
                return []

            # 计算时间范围
            start_time = datetime.utcnow() - timedelta(hours=hours_ago)

            # 获取推文
            tweets = self.client.get_users_tweets(
                id=user_id,
                start_time=start_time,
                tweet_fields=['created_at', 'public_metrics', 'text', 'author_id'],
                max_results=100,
                exclude=['retweets', 'replies']  # 排除转发和回复
            )

            if not tweets.data:
                return []

            # 筛选并格式化数据
            filtered_tweets = []
            for tweet in tweets.data:
                metrics = tweet.public_metrics

                # 检查点赞数
                if metrics['like_count'] >= min_likes:
                    filtered_tweets.append({
                        'username': username,
                        'tweet_id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'like_count': metrics['like_count'],
                        'retweet_count': metrics['retweet_count'],
                        'reply_count': metrics['reply_count'],
                        'quote_count': metrics['quote_count'],
                        'impression_count': metrics.get('impression_count', 0),
                        'url': f"https://twitter.com/{username}/status/{tweet.id}"
                    })

            print(f"✅ @{username}: 找到 {len(filtered_tweets)} 条符合条件的推文")
            return filtered_tweets

        except Exception as e:
            print(f"⚠️  获取 @{username} 推文失败: {e}")
            return []

    def get_all_tweets(self, usernames: List[str], hours_ago: int = 48, min_likes: int = 100) -> List[Dict]:
        """
        获取所有指定账号的推文

        Args:
            usernames: 用户名列表
            hours_ago: 获取多少小时内的推文
            min_likes: 最小点赞数

        Returns:
            所有推文列表
        """
        all_tweets = []

        print(f"\n🔍 开始获取 {len(usernames)} 个账号的推文...")
        print(f"📅 时间范围: 最近 {hours_ago} 小时")
        print(f"❤️  筛选条件: 点赞 ≥ {min_likes}\n")

        for i, username in enumerate(usernames, 1):
            print(f"[{i}/{len(usernames)}] 正在获取 @{username}...", end=" ")
            tweets = self.get_user_tweets(username, hours_ago, min_likes)
            all_tweets.extend(tweets)

        print(f"\n✅ 总共找到 {len(all_tweets)} 条符合条件的推文")
        return all_tweets

    def sort_by_engagement(self, tweets: List[Dict]) -> List[Dict]:
        """
        按互动量排序推文

        Args:
            tweets: 推文列表

        Returns:
            排序后的推文列表
        """
        def calculate_engagement(tweet):
            return (
                tweet['like_count'] * 1 +
                tweet['retweet_count'] * 2 +
                tweet['reply_count'] * 1.5 +
                tweet['quote_count'] * 1.5
            )

        sorted_tweets = sorted(tweets, key=calculate_engagement, reverse=True)
        return sorted_tweets
