"""
Twitter 爬虫模块 - 使用 requests 直接爬取 Twitter 前端
不需要 API Key，直接模拟浏览器请求
"""

import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re
import json
from urllib.parse import quote


class TwitterScraper:
    """Twitter 爬虫类"""

    def __init__(self):
        """初始化爬虫"""
        self.session = requests.Session()
        # 设置 User-Agent 模拟浏览器
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
        })

        # Twitter 的 Guest Token 获取
        self.guest_token = None
        self._get_guest_token()

    def _get_guest_token(self):
        """获取 Twitter Guest Token"""
        try:
            response = self.session.post(
                'https://api.twitter.com/1.1/guest/activate.json',
                headers={
                    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3DZ1lq6wVV5Y7Rk5lQ7x5q5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y5Y'
                }
            )
            if response.status_code == 200:
                data = response.json()
                self.guest_token = data.get('guest_token')
                print(f"✅ 获取 Guest Token 成功")
        except Exception as e:
            print(f"⚠️  获取 Guest Token 失败: {e}")

    def get_user_tweets(self, username: str, hours_ago: int = 48, min_likes: int = 100) -> List[Dict]:
        """
        获取指定用户的推文

        Args:
            username: Twitter 用户名
            hours_ago: 多少小时内的推文
            min_likes: 最小点赞数

        Returns:
            推文列表
        """
        if not self.guest_token:
            print("⚠️  无 Guest Token，跳过")
            return []

        try:
            # 构建查询 URL
            url = f"https://api.twitter.com/2/graphql/7wj Z1zO7zq-j-Z2j-Z1j-Z2j-Z1j-Z2j-Z1j-Z2j-Z1j-Z2j-Z1j-Z2j-Z1j-Z2j-Z1j-Z2j-Z1j-Z2j"

            # 使用更简单的方法：直接请求用户主页
            user_url = f"https://twitter.com/{username}"
            response = self.session.get(user_url)

            if response.status_code == 200:
                # 尝试从 HTML 中提取推文数据
                tweets = self._parse_tweets_from_html(response.text, username, hours_ago, min_likes)
                return tweets
            else:
                print(f"⚠️  获取 @{username} 主页失败: {response.status_code}")
                return []

        except Exception as e:
            print(f"⚠️  获取 @{username} 推文出错: {e}")
            return []

    def _parse_tweets_from_html(self, html: str, username: str, hours_ago: int, min_likes: int) -> List[Dict]:
        """
        从 HTML 中解析推文数据（简化版本）
        """
        tweets = []

        try:
            # 尝试找到包含推文数据的 script 标签
            pattern = r'"tweet":{"([^"]+)":"([^"]+)"'
            matches = re.findall(pattern, html)

            # 这个解析比较复杂，暂时返回空列表
            # 实际上需要更复杂的解析逻辑
            pass

        except Exception as e:
            pass

        return tweets


class TwitterNitterScraper:
    """使用 Nitter 实例的爬虫（更简单）"""

    def __init__(self, nitter_instance: str = "nitter.net"):
        """初始化 Nitter 爬虫"""
        self.base_url = f"https://{nitter_instance}"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def get_user_tweets(self, username: str, hours_ago: int = 48, min_likes: int = 100) -> List[Dict]:
        """获取用户推文"""
        try:
            url = f"{self.base_url}/{username}"
            response = self.session.get(url, timeout=10)

            if response.status_code != 200:
                print(f"⚠️  获取 @{username} 失败")
                return []

            # 解析 HTML 获取推文
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            tweets = []
            tweet_elements = soup.find_all('div', class_='timeline-item')

            for tweet_el in tweet_elements:
                try:
                    # 提取推文内容
                    text_el = tweet_el.find('div', class_='tweet-content')
                    if not text_el:
                        continue
                    text = text_el.get_text(strip=True)

                    # 提取点赞数
                    likes_el = tweet_el.find('span', class_='likes-count')
                    likes = int(likes_el.get_text()) if likes_el else 0

                    if likes < min_likes:
                        continue

                    # 提取时间
                    time_el = tweet_el.find('span', class_='tweet-time')
                    tweet_time = datetime.utcnow()  # 默认当前时间

                    # 提取推文链接
                    link_el = tweet_el.find('a', class_='tweet-link')
                    tweet_url = f"https://twitter.com/{username}/status/12345"  # 占位

                    tweets.append({
                        'username': username,
                        'tweet_id': 'placeholder',
                        'text': text,
                        'created_at': tweet_time,
                        'like_count': likes,
                        'retweet_count': 0,
                        'reply_count': 0,
                        'quote_count': 0,
                        'impression_count': 0,
                        'url': tweet_url
                    })

                except Exception as e:
                    continue

            return tweets

        except Exception as e:
            print(f"⚠️  爬取 @{username} 出错: {e}")
            return []


# 使用模拟数据的简化版本
class TwitterMockScraper:
    """模拟数据爬虫（用于测试）"""

    def __init__(self):
        """初始化"""
        pass

    def get_user_tweets(self, username: str, hours_ago: int = 48, min_likes: int = 100) -> List[Dict]:
        """生成模拟推文数据"""
        # 模拟一些热门推文
        mock_tweets = [
            {
                'username': username,
                'tweet_id': f'{username}_001',
                'text': f'🚀 Excited to announce our new AI model! This is a game changer for the industry. #AI #MachineLearning',
                'created_at': datetime.utcnow() - timedelta(hours=12),
                'like_count': 15234,
                'retweet_count': 3842,
                'reply_count': 892,
                'quote_count': 445,
                'impression_count': 1200000,
                'url': f'https://twitter.com/{username}/status/123456789'
            },
            {
                'username': username,
                'tweet_id': f'{username}_002',
                'text': f'Just published a paper on scaling laws for large language models. The results are fascinating! Link below 👇',
                'created_at': datetime.utcnow() - timedelta(hours=24),
                'like_count': 8756,
                'retweet_count': 2103,
                'reply_count': 456,
                'quote_count': 234,
                'impression_count': 560000,
                'url': f'https://twitter.com/{username}/status/123456790'
            }
        ]

        # 只返回符合条件的推文
        return [t for t in mock_tweets if t['like_count'] >= min_likes]

    def sort_by_engagement(self, tweets: List[Dict]) -> List[Dict]:
        """按互动量排序推文"""
        def calculate_engagement(tweet):
            return (
                tweet['like_count'] * 1 +
                tweet['retweet_count'] * 2 +
                tweet['reply_count'] * 1.5 +
                tweet['quote_count'] * 1.5
            )

        sorted_tweets = sorted(tweets, key=calculate_engagement, reverse=True)
        return sorted_tweets
