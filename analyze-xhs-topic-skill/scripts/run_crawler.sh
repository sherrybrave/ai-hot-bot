#!/bin/bash
# 小红书爬虫执行脚本
# 使用 MediaCrawler 爬取指定关键词的热门笔记

set -e

# 检查参数
if [ $# -lt 1 ]; then
    echo "用法: $0 <关键词> [数量]"
    echo "示例: $0 裸辞 20"
    exit 1
fi

KEYWORD="$1"
COUNT="${2:-20}"  # 默认爬取20篇

# MediaCrawler 项目路径
MEDIA_CRAWLER_PATH="/Users/it/Documents/AI/Claude Code/MediaCrawler"

# 检查 MediaCrawler 是否存在
if [ ! -d "$MEDIA_CRAWLER_PATH" ]; then
    echo "错误: MediaCrawler 项目不存在于 $MEDIA_CRAWLER_PATH"
    exit 1
fi

# 进入项目目录
cd "$MEDIA_CRAWLER_PATH"

# 配置爬取数量
# 临时修改配置文件中的 CRAWLER_MAX_NOTES_COUNT
sed -i.bak "s/CRAWLER_MAX_NOTES_COUNT = .*/CRAWLER_MAX_NOTES_COUNT = $COUNT/" config/base_config.py

# 恢复备份的函数
cleanup() {
    mv config/base_config.py.bak config/base_config.py 2>/dev/null || true
}

# 设置退出时清理
trap cleanup EXIT

# 配置关键词
sed -i.bak "s/KEYWORDS = \".*\"/KEYWORDS = \"$KEYWORD\"/" config/base_config.py

# 运行爬虫
echo "开始爬取关键词: $KEYWORD"
echo "爬取数量: $COUNT"
echo "---"

export PATH="$HOME/.local/bin:$PATH"
uv run main.py --platform xhs --lt qrcode --type search

echo "---"
echo "爬取完成！"
echo "数据保存在: $MEDIA_CRAWLER_PATH/data/xhs/json/"
