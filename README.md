# 🤖 AI热推bot

> 每天 8:00 自动生成 AI 领域热门推文报告

## ✨ 功能

- 🔍 **自动抓取**：每天自动抓取 50+ AI 领域重要账号的最新推文
- 📊 **智能筛选**：筛选过去 48 小时内点赞 ≥ 100 的热门推文
- 🤖 **AI 解读**：使用智谱 GLM 分析热点趋势
- 📈 **Top 10 排行**：按互动量排序，输出最热门的 10 条推文
- ⏰ **定时运行**：每天早上 8:00（北京时间）自动运行
- 📝 **格式精美**：生成易读的 Markdown 报告

## 📁 项目结构

```
.
├── .github/
│   └── workflows/
│       └── daily-report.yml    # GitHub Actions 定时任务
├── ai-hot-bot/
│   ├── main.py                 # 主程序
│   ├── twitter_api.py          # Twitter API 封装
│   ├── zhipu_ai.py             # 智谱 AI 解读
│   ├── formatter.py            # 报告格式化
│   ├── accounts.txt            # 监控账号列表
│   └── requirements.txt        # Python 依赖
├── reports/                    # 生成的报告
│   └── ai-hot-report-YYYY-MM-DD.md
└── README.md
```

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone https://github.com/sherrybrave/ai-hot-bot.git
cd ai-hot-bot
```

### 2. 安装依赖

```bash
pip install -r ai-hot-bot/requirements.txt
```

### 3. 配置环境变量

在 GitHub 仓库设置中添加以下 Secrets：

- `TWITTER_BEARER_TOKEN`: Twitter API Bearer Token
- `ZHIPU_API_KEY`: 智谱 GLM API Key

**获取方式：**
- Twitter API: https://developer.twitter.com/
- 智谱 GLM: https://open.bigmodel.cn/

### 4. 启用 GitHub Actions

1. 推送代码到 GitHub
2. 在仓库的 "Actions" 页面启用 GitHub Actions
3. 每天北京时间 8:00 自动运行

## 📊 监控账号

目前监控以下 AI 领域重要账号：

**官方账号：**
- @OpenAI, @AnthropicAI, @GoogleDeepMind, @xai, @MetaAI

**行业领袖：**
- @sama (Sam Altman), @karpathy (Andrej Karpathy), @ylecun (Yann LeCun)

**完整列表：** 查看 [`ai-hot-bot/accounts.txt`](ai-hot-bot/accounts.txt)

## 📝 报告示例

```markdown
# 🤖 AI热报 - 2025年2月23日

## 📊 今日热点解读
昨日AI领域最热门的话题集中在大模型应用落地...

## 🔥 Top 10 热门推文

### 1️⃣ 第1名
**发帖账号**：@OpenAI
**发帖时间**：2025-02-23 06:30 UTC
**帖子原文**：...
**原帖互动**：👍 Like: 15.2K | 🔁 Repost: 3.8K | 💬 Reply: 892
🔗 **原推链接**：https://twitter.com/OpenAI/status/123456789
...
```

## 🛠️ 本地运行

```bash
cd ai-hot-bot
export TWITTER_BEARER_TOKEN="your_token"
export ZHIPU_API_KEY="your_key"
python main.py
```

## 📡 OpenClaw 集成

OpenClaw 可以从 GitHub 自动获取最新报告：

**报告文件路径：**
```
https://raw.githubusercontent.com/sherrybrave/ai-hot-bot/main/reports/ai-hot-report-2025-02-23.md
```

**最新报告（总是指向最新日期）：**
```
https://raw.githubusercontent.com/sherrybrave/ai-hot-bot/main/reports/ai-hot-report-latest.md
```

## 🔄 手动触发

在 GitHub Actions 页面点击 "Run workflow" 可以手动触发报告生成。

## 📄 License

MIT

## 👤 作者

Created by [sherrybrave](https://github.com/sherrybrave)

---

🤖 由 **AI热推bot** 自动生成 | 数据来源：Twitter/X
