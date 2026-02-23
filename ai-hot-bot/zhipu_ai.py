"""
智谱 AI 解读模块
使用智谱 GLM API 生成 AI 热点解读
"""

from zhipuai import ZhipuAI
from typing import List, Dict


class ZhipuAnalyzer:
    """智谱 AI 分析器"""

    def __init__(self, api_key: str):
        """
        初始化智谱 AI 客户端

        Args:
            api_key: 智谱 GLM API Key
        """
        self.client = ZhipuAI(api_key=api_key)

    def generate_insight(self, top_tweets: List[Dict], num_tweets: int = 10) -> str:
        """
        生成 AI 热点解读

        Args:
            top_tweets: Top N 热门推文列表
            num_tweets: 分析前N条推文

        Returns:
            AI 生成的解读文本
        """
        # 准备推文摘要
        tweets_summary = ""
        for i, tweet in enumerate(top_tweets[:num_tweets], 1):
            tweets_summary += f"\n{i}. @{tweet['username']}: {tweet['text'][:200]}..."

        # 构建提示词
        prompt = f"""你是一位资深的AI行业分析师。以下是过去48小时内AI领域（Twitter/X平台）最热门的{num_tweets}条推文：

{tweets_summary}

请分析这些热点内容，用专业但易懂的语言写一段200-300字的解读，包括：
1. 核心趋势和关键信息
2. 重要的产品发布/技术突破
3. 行业动态和值得关注的方向

请直接输出解读内容，不要有开场白和结束语。"""

        try:
            print("\n🤖 正在调用智谱 GLM 生成 AI 解读...")
            response = self.client.chat.completions.create(
                model="glm-4-flash",  # 使用快速模型
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )

            insight = response.choices[0].message.content.strip()
            print("✅ AI 解读生成完成")
            return insight

        except Exception as e:
            print(f"⚠️  AI 解读生成失败: {e}")
            return "（AI 解读暂时不可用，请稍后查看）"

    def generate_title(self, top_tweets: List[Dict]) -> str:
        """
        生成今日热点的标题

        Args:
            top_tweets: 热门推文列表

        Returns:
            生成的标题
        """
        # 提取关键词
        keywords = []
        for tweet in top_tweets[:5]:
            text = tweet['text'].lower()
            # 简单关键词提取（实际可以用更复杂的方法）
            if 'gpt' in text or 'openai' in text:
                keywords.append('OpenAI')
            if 'claude' in text or 'anthropic' in text:
                keywords.append('Anthropic')
            if 'gemini' in text or 'google' in text:
                keywords.append('Google')
            if 'llama' in text or 'meta' in text:
                keywords.append('Meta')
            if 'agent' in text:
                keywords.append('AI Agent')

        # 去重
        unique_keywords = list(dict.fromkeys(keywords))

        if unique_keywords:
            return f"今日AI热点：{', '.join(unique_keywords[:3])}"
        return "今日AI热点速递"
