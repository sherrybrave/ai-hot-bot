# PopPump 架构设计文档

> 项目名称：PopPump - 小红书爆款笔记写作Agent
> 版本：v1.0
> 最后更新：2025-02-08
> 开发周期：5天完整MVP

---

## 1. 技术栈选择及原因

### 1.1 前端技术栈

| 技术 | 版本/说明 | 选择原因 |
|------|-----------|----------|
| **HTML5** | 纯HTML，无框架 | 1. 项目规模适中，不需要复杂框架<br>2. 直接生成静态HTML，部署简单<br>3. SEO友好，加载速度快 |
| **CSS3** | 原生CSS + CSS Variables | 1. 使用frontend-design skill生成<br>2. CSS Variables实现主题切换<br>3. 避免构建工具复杂度 |
| **JavaScript (ES6+)** | Vanilla JS（无框架） | 1. 项目逻辑可控，不需要React/Vue<br>2. 减少依赖和学习成本<br>3. 直接操作DOM，性能足够 |
| **frontend-design skill** | Claude Code官方插件 | 1. 快速生成符合小红书风格的UI<br>2. 自动响应式设计<br>3. 统一设计语言 |

### 1.2 后端技术栈

| 技术 | 版本/说明 | 选择原因 |
|------|-----------|----------|
| **智谱GLM API** | GLM-4.7/4.6/4.5/4.5-Air | 1. 中文理解能力强<br>2. 价格便宜（用户已购买）<br>3. API稳定，响应速度快 |
| **Vercel Serverless Functions** | Node.js 18.x | 1. 无需独立服务器<br>2. 按请求计费，成本低<br>3. 与前端部署在同一平台 |
| **Firebase** | Firestore + Authentication | 1. 免费额度足够MVP阶段<br>2. 实时数据库，支持多端同步<br>3. 内置邮箱验证功能 |

### 1.3 部署与运维

| 技术 | 版本/说明 | 选择原因 |
|------|-----------|----------|
| **Vercel** | 静态托管 | 1. 免费额度足够MVP<br>2. 自动HTTPS+CDN<br>3. Git推送自动部署 |
| **Git** | 版本控制 | 1. 标准版本控制工具<br>2. 便于团队协作<br>3. Vercel集成 |

---

## 2. 项目目录结构

```
xiaohongshu-writer-app/
├── index.html                    # 旧版：6步向导式流程（已废弃）
├── index-v2.html                 # 新版：三栏式布局主页面
├── playground.html               # UI组件测试页面
├── PRD.md                        # 产品需求文档
├── ARCHITECTURE.md               # 架构设计文档（本文件）
│
├── css/
│   ├── style.css                 # 旧版样式
│   ├── three-column.css          # 三栏布局样式（1000+行）
│   └── variables.css             # CSS变量定义（可选）
│
├── js/
│   ├── app.js                    # 旧版6步向导逻辑（已废弃）
│   ├── app-v2.js                 # 新版三栏布局逻辑（待实现）
│   ├── api.js                    # API调用封装（智谱GLM）
│   ├── firebase.js               # Firebase初始化与配置
│   └── utils.js                  # 工具函数
│
├── api/                          # Vercel Serverless Functions
│   ├── generate.js               # 内容生成API
│   ├── analyze.js                # 风格分析API
│   └── activate.js               # 用户激活API（管理员）
│
├── assets/                       # 静态资源
│   ├── images/
│   │   ├── logo.svg
│   │   └── qr-code.png           # 微信收款码
│   └── icons/
│
└── firebase.json                 # Firebase配置文件
```

---

## 3. 核心模块说明

### 3.1 整体架构

```
┌──────────────────────────────────────────────────────────────┐
│                         Browser (客户端)                      │
├──────────────┬──────────────────────────────┬─────────────────┤
│              │                              │                 │
│  Left Sidebar│       Center Canvas          │ Right Sidebar   │
│              │                              │                 │
│  ┌──────────┐│  ┌──────────────────────┐   │┌───────────────┐│
│  │Knowledge ││  │  Multi-tab System    │   ││  Agent Chat   ││
│  │  Base    ││  │                      │   ││               ││
│  │          ││  │ • Welcome            │   ││ • Message     ││
│  │• 框架库   ││  │ • Style Learning     │   ││   History     ││
│  │• 风格库   ││  │ • Chat               │   ││ • Input Area  ││
│  │• 参考文章 ││  │ • Article Edit       │   │└───────────────┘│
│  │• 生成文章 ││  │                      │   │                 │
│  └──────────┘│  └──────────────────────┘   │                 │
│              │                              │                 │
└──────────────┴──────────────────────────────┴─────────────────┘
                            ↕ HTTPS
┌──────────────────────────────────────────────────────────────┐
│                      Vercel Platform                         │
├──────────────────────────────────────────────────────────────┤
│  Serverless Functions (/api/*)                               │
│  • generate.js → 调用智谱GLM生成内容                         │
│  • analyze.js → 分析文章风格和框架                           │
│  • activate.js → 管理员手动激活用户                           │
└──────────────────────────────────────────────────────────────┘
                            ↕ REST API
┌──────────────────────────────────────────────────────────────┐
│                     External Services                        │
├──────────────────┬──────────────────────┬────────────────────┤
│  智谱GLM API      │    Firebase          │    Email Service   │
│  • GLM-4.7       │  • Firestore         │  • 邮箱验证        │
│  • GLM-4.6       │  • Authentication    │                    │
│  • GLM-4.5       │  • Realtime DB       │                    │
└──────────────────┴──────────────────────┴────────────────────┘
```

### 3.2 前端模块

#### 3.2.1 左侧栏：知识库管理模块

**功能**：
- 展示和管理知识库内容（框架库、风格库、参考文章、生成文章）
- 树形结构展示，支持折叠/展开
- 点击知识库项目，在中间画布打开对应内容

**核心功能**：
```javascript
// js/app-v2.js
class KnowledgeBase {
  // 初始化知识树
  initKnowledgeTree()

  // 切换文件夹展开/折叠
  toggleFolder(element)

  // 打开框架
  openFramework(frameworkId)

  // 打开风格
  openStyle(styleId)

  // 打开参考文章
  openReference(refId)

  // 打开生成文章
  openArticle(articleId)

  // 添加参考文章
  addReference()
}
```

**数据结构**：
```javascript
const knowledgeData = {
  frameworks: [
    { id: 'signal-list', name: '信号列举-干货型', icon: '📋' },
    { id: 'story-telling', name: '故事讲述-情感型', icon: '📖' },
    // ... 更多框架
  ],
  styles: [
    { id: 'default', name: '风格#1 (默认)', icon: '✨' }
  ],
  references: [
    { id: 'ref1', name: '职场效率笔记', icon: '📄', content: '...' }
  ],
  generatedArticles: [
    { id: 'article1', name: '大厂效率秘籍', icon: '📝', content: '...' }
  ]
}
```

#### 3.2.2 中间栏：多标签画布系统

**功能**：
- 多标签页管理（欢迎、风格学习、对话、文章编辑）
- 动态添加/关闭标签页
- 标签页内容渲染

**核心功能**：
```javascript
class TabManager {
  // 创建新标签
  createTab(tabId, title, content)

  // 切换标签
  switchTab(tabId)

  // 关闭标签
  closeTab(tabId)

  // 新建对话
  newChat()

  // 渲染标签内容
  renderTabContent(tabId)
}

// 各标签页功能
class WelcomeTab { /* 欢迎页面 */ }
class StyleLearningTab { /* 风格学习 */ }
class ChatTab { /* 对话生成 */ }
class ArticleEditTab { /* 文章编辑 */ }
```

**标签页状态管理**：
```javascript
const tabs = [
  { id: 'welcome', title: '👋 欢迎', active: true, closable: false },
  { id: 'style-learning', title: '🎨 风格学习', active: false, closable: true },
  { id: 'chat', title: '💬 对话', active: false, closable: true },
  { id: 'article-edit', title: '📝 编辑', active: false, closable: true }
]
```

#### 3.2.3 右侧栏：Agent对话模块

**功能**：
- 显示Agent对话历史
- 用户输入框
- 发送消息
- 展示生成进度（多步骤可视化）

**核心功能**：
```javascript
class AgentChat {
  // 发送消息
  sendMessage(userInput)

  // 处理Agent响应
  handleAgentResponse(response)

  // 显示生成进度
  showGenerationProgress(steps)

  // 添加消息到历史
  addMessage(role, content)

  // 处理回车发送
  handleKeyPress(event)
}

// 生成进度步骤
const generationSteps = [
  { step: 1, title: '提取框架', desc: '已识别框架' },
  { step: 2, title: '融合风格', desc: '正在学习你的表达方式...' },
  { step: 3, title: '生成内容', desc: '正在撰写正文...' },
  { step: 4, title: '推荐标题', desc: '正在生成爆款标题...' },
  { step: 5, title: '生成标签', desc: '正在推荐相关标签...' }
]
```

### 3.3 后端模块

#### 3.3.1 内容生成API

**文件位置**：`/api/generate.js`

**功能**：
- 接收用户输入的idea和参考文章
- 调用智谱GLM API生成小红书笔记
- 返回生成的标题、正文、标签

**接口定义**：
```javascript
// POST /api/generate
// Request Body:
{
  "idea": "分享3个提高工作效率的方法",
  "referenceArticles": ["文章1内容", "文章2内容"],
  "frameworkId": "signal-list",
  "styleId": "default",
  "userId": "user@example.com"
}

// Response:
{
  "success": true,
  "data": {
    "titles": [
      { "text": "3个技巧让你效率翻倍", "reason": "数字+痛点+收益" },
      { "text": "大厂不说的效率秘籍", "reason": "好奇心+权威感" },
      { "text": "别再浪费时间了", "reason": "情绪化+紧迫感" }
    ],
    "content": "今天和大家分享...",
    "tags": ["#效率提升", "#职场经验", "#个人成长"]
  }
}
```

**核心逻辑**：
```javascript
import { generateContent } from '../js/api.js';

export default async function handler(req, res) {
  const { idea, referenceArticles, frameworkId, styleId, userId } = req.body;

  // 1. 验证用户额度
  const userQuota = await getUserQuota(userId);
  if (userQuota.remaining <= 0) {
    return res.status(403).json({ error: '额度已用完' });
  }

  // 2. 调用智谱GLM生成内容
  const generated = await generateContent(idea, referenceArticles, frameworkId);

  // 3. 扣减用户额度
  await decrementQuota(userId);

  // 4. 返回结果
  res.json({ success: true, data: generated });
}
```

#### 3.3.2 风格分析API

**文件位置**：`/api/analyze.js`

**功能**：
- 接收参考文章内容
- 调用智谱GLM分析文章风格
- 返回框架、语气、结构、表达习惯等

**接口定义**：
```javascript
// POST /api/analyze
// Request Body:
{
  "articles": ["文章1内容", "文章2内容"]
}

// Response:
{
  "success": true,
  "data": {
    "framework": "信号列举-干货型",
    "tone": "轻松活泼",
    "structure": "总分总结构",
    "emoji": "适当使用Emoji",
    "habits": [
      "常用'和大家分享'作为开场白",
      "喜欢用'第一个'、'第二个'等序数词"
    ]
  }
}
```

#### 3.3.3 用户激活API

**文件位置**：`/api/activate.js`

**功能**：
- 管理员手动激活用户
- 设置用户额度
- 记录激活历史

**接口定义**：
```javascript
// POST /api/activate (需要管理员密码)
// Request Body:
{
  "adminPassword": "ADMIN_PASSWORD",
  "email": "user@example.com",
  "plan": "monthly", // or "yearly"
  "quota": -1 // -1表示无限
}

// Response:
{
  "success": true,
  "data": {
    "email": "user@example.com",
    "plan": "monthly",
    "quota": -1,
    "activatedAt": "2025-02-08T10:00:00Z"
  }
}
```

### 3.4 数据存储模块

#### 3.4.1 Firebase数据结构

**用户集合 (users)**：
```javascript
{
  "email": "user@example.com",
  "emailVerified": false,
  "plan": "free", // free, monthly, yearly
  "quota": {
    "total": 3,      // 总次数
    "used": 0,       // 已使用次数
    "remaining": 3   // 剩余次数 (-1表示无限)
  },
  "createdAt": "2025-02-08T10:00:00Z",
  "activatedAt": null, // 激活时间（付费用户）
  "lastUsedAt": "2025-02-08T12:00:00Z"
}
```

**知识库集合 (knowledgeBase)**：
```javascript
{
  "userId": "user@example.com",
  "type": "framework", // framework, style, reference, article
  "name": "信号列举-干货型",
  "content": "...",
  "tags": ["干货", "方法论"],
  "createdAt": "2025-02-08T10:00:00Z"
}
```

**生成历史 (generations)**：
```javascript
{
  "userId": "user@example.com",
  "idea": "分享3个提高工作效率的方法",
  "generatedContent": {
    "title": "大厂不说的效率秘籍",
    "content": "...",
    "tags": ["#效率提升", "#职场经验"]
  },
  "frameworkId": "signal-list",
  "styleId": "default",
  "createdAt": "2025-02-08T12:00:00Z"
}
```

**激活历史 (activations)**：
```javascript
{
  "email": "user@example.com",
  "plan": "monthly",
  "amount": 29,
  "paymentMethod": "wechat",
  "activatedBy": "admin",
  "activatedAt": "2025-02-08T10:00:00Z"
}
```

---

## 4. 数据模型设计

### 4.1 用户状态模型

```javascript
// 浏览器localStorage
const localUserState = {
  email: "user@example.com",
  emailVerified: false,
  isLoggedIn: false,
  currentSession: "session-uuid"
}

// Firebase Firestore
const userDoc = {
  email: "user@example.com",
  emailVerified: false,
  plan: "free", // free | monthly | yearly
  quota: {
    total: 3,
    used: 0,
    remaining: 3
  },
  createdAt: Timestamp,
  activatedAt: Timestamp | null,
  lastUsedAt: Timestamp
}
```

### 4.2 内容生成模型

```javascript
// 生成请求
const generationRequest = {
  idea: "用户输入的想法",
  referenceArticles: ["参考文章1", "参考文章2"],
  frameworkId: "signal-list",
  styleId: "default",
  userId: "user@example.com"
}

// 生成响应
const generationResponse = {
  titles: [
    { text: "标题1", reason: "推荐理由" },
    { text: "标题2", reason: "推荐理由" },
    { text: "标题3", reason: "推荐理由" }
  ],
  content: "完整正文内容",
  tags: ["#标签1", "#标签2", "#标签3"]
}
```

### 4.3 知识库模型

```javascript
// 框架库
const framework = {
  id: "signal-list",
  name: "信号列举-干货型",
  icon: "📋",
  description: "适合分享实用技巧和方法论",
  pattern: "总分总结构，列举3-5个要点",
  examples: ["职场效率", "学习方法"]
}

// 风格库
const style = {
  id: "default",
  name: "风格#1",
  icon: "✨",
  tone: "轻松活泼",
  voice: "第一人称",
  emojiUsage: "适当使用",
  habits: [
    "常用'和大家分享'开场",
    "喜欢用序数词",
    "结尾总结观点"
  ]
}

// 参考文章
const referenceArticle = {
  id: "ref1",
  name: "职场效率笔记",
  icon: "📄",
  content: "文章正文内容",
  tags: ["职场", "效率"],
  createdAt: Timestamp
}

// 生成文章
const generatedArticle = {
  id: "article1",
  name: "大厂效率秘籍",
  icon: "📝",
  title: "大厂不说的效率秘籍",
  content: "正文内容",
  tags: ["#效率提升", "#职场经验"],
  frameworkId: "signal-list",
  styleId: "default",
  createdAt: Timestamp
}
```

---

## 5. 代码规范

### 5.1 文件命名规范

```
// HTML文件：小写字母，连字符分隔
index-v2.html
playground.html

// CSS文件：小写字母，连字符分隔
style.css
three-column.css

// JavaScript文件：小写字母，连字符分隔
app-v2.js
api.js
firebase.js
utils.js

// API函数：小写字母，连字符分隔
/api/generate.js
/api/analyze.js
/api/activate.js
```

### 5.2 JavaScript编码规范

#### 5.2.1 变量命名

```javascript
// 常量：UPPER_SNAKE_CASE
const MAX_FREE_QUOTA = 3;
const API_BASE_URL = 'https://open.bigmodel.cn/api/paas/v4/';

// 普通变量：camelCase
let remainingQuota = 3;
const userName = '夏树';

// 类名：PascalCase
class KnowledgeBase { }
class TabManager { }

// 私有方法：前缀下划线
class UserManager {
  _validateEmail(email) { }
  _updateQuota(userId) { }
}
```

#### 5.2.2 代码组织

```javascript
// ========================================
// 模块说明注释
// ========================================

// 1. 导入依赖
import { initializeApp } from 'firebase/app';

// 2. 常量定义
const CONSTANTS = {
  MAX_FREE_QUOTA: 3,
  SESSION_TIMEOUT: 3600000
};

// 3. 状态管理
const state = {
  currentTab: 'welcome',
  isLoggedIn: false,
  userData: null
};

// 4. 工具函数
function formatDate(date) {
  return date.toISOString();
}

// 5. 核心类
class UserManager {
  constructor() {
    this.user = null;
  }

  async login(email) {
    // 登录逻辑
  }
}

// 6. 初始化
document.addEventListener('DOMContentLoaded', function() {
  initApp();
});

function initApp() {
  // 初始化逻辑
}
```

#### 5.2.3 异步处理

```javascript
// 使用 async/await
async function generateContent(idea) {
  try {
    const response = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ idea })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('生成失败:', error);
    throw error;
  }
}
```

#### 5.2.4 错误处理

```javascript
// 统一错误处理
function handleError(error, context = '') {
  console.error(`${context}:`, error);

  // 用户友好提示
  const userMessages = {
    'QUOTA_EXCEEDED': '您的免费额度已用完，请升级到Pro版本',
    'NETWORK_ERROR': '网络连接失败，请检查网络设置',
    'API_ERROR': '服务暂时不可用，请稍后重试'
  };

  const message = userMessages[error.code] || '操作失败，请重试';
  alert(message);
}

// 使用示例
try {
  await generateContent(idea);
} catch (error) {
  handleError(error, '内容生成');
}
```

### 5.3 CSS编码规范

#### 5.3.1 命名规范

```css
/* BEM命名规范 */
.block { }
.block__element { }
.block--modifier { }

/* 示例 */
.knowledge-base { }
.knowledge-tree { }
.tree-item { }
.tree-item--active { }
.tree-item-header { }
.tree-children { }
```

#### 5.3.2 CSS Variables

```css
:root {
    /* 颜色系统 */
    --primary-color: #ff2442;
    --primary-light: #fff0f2;
    --text-primary: #1a1a1a;
    --text-secondary: #666666;
    --text-tertiary: #999999;
    --bg-primary: #ffffff;
    --bg-secondary: #f5f5f5;
    --border-color: #e5e7eb;

    /* 尺寸系统 */
    --left-sidebar-width: 260px;
    --right-sidebar-width: 320px;
    --header-height: 64px;

    /* 间距系统 */
    --spacing-xs: 0.5rem;    /* 8px */
    --spacing-sm: 0.75rem;   /* 12px */
    --spacing-md: 1rem;      /* 16px */
    --spacing-lg: 1.5rem;    /* 24px */
    --spacing-xl: 2rem;      /* 32px */

    /* 圆角系统 */
    --radius-sm: 4px;
    --radius-md: 8px;
    --radius-lg: 12px;

    /* 字体系统 */
    --font-size-sm: 0.875rem;
    --font-size-md: 1rem;
    --font-size-lg: 1.125rem;
    --font-size-xl: 1.5rem;
}
```

### 5.4 API接口规范

#### 5.4.1 统一响应格式

```javascript
// 成功响应
{
  "success": true,
  "data": { /* 实际数据 */ },
  "message": "操作成功"
}

// 错误响应
{
  "success": false,
  "error": {
    "code": "QUOTA_EXCEEDED",
    "message": "免费额度已用完"
  }
}
```

#### 5.4.2 错误码定义

```javascript
const ERROR_CODES = {
  // 用户相关
  UNAUTHORIZED: 'UNAUTHORIZED',              // 未登录
  EMAIL_NOT_VERIFIED: 'EMAIL_NOT_VERIFIED',  // 邮箱未验证
  USER_NOT_FOUND: 'USER_NOT_FOUND',          // 用户不存在

  // 额度相关
  QUOTA_EXCEEDED: 'QUOTA_EXCEEDED',          // 额度超限
  INVALID_PLAN: 'INVALID_PLAN',              // 无效套餐

  // 内容相关
  INVALID_INPUT: 'INVALID_INPUT',            // 输入无效
  GENERATION_FAILED: 'GENERATION_FAILED',    // 生成失败

  // 系统相关
  NETWORK_ERROR: 'NETWORK_ERROR',            // 网络错误
  API_ERROR: 'API_ERROR',                    // API错误
  INTERNAL_ERROR: 'INTERNAL_ERROR'           // 内部错误
};
```

### 5.5 Git提交规范

```bash
# 提交信息格式：<type>(<scope>): <subject>

# type类型：
# feat: 新功能
# fix: 修复bug
# docs: 文档更新
# style: 代码格式调整
# refactor: 重构
# test: 测试相关
# chore: 构建/工具变动

# 示例：
git commit -m "feat(knowledge-base): 添加知识库树形结构展示"
git commit -m "fix(api): 修复用户额度扣减bug"
git commit -m "docs(readme): 更新部署说明"
```

### 5.6 安全规范

```javascript
// 1. API密钥安全
// ✅ 正确：使用环境变量
const API_KEY = process.env.ZHIPU_API_KEY;

// ❌ 错误：硬编码在代码中
const API_KEY = 'sk-xxxxx';

// 2. 用户输入验证
function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

// 3. XSS防护
function sanitizeHTML(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

// 4. 敏感信息不提交到Git
// .gitignore
.env
firebase-service-account.json
```

---

## 6. 开发计划（5天MVP）

### Day 1：前端基础架构
- [x] 创建三栏式HTML结构
- [x] 编写三栏式CSS样式
- [ ] 实现标签页管理逻辑
- [ ] 实现知识库树形结构交互

### Day 2：核心功能逻辑
- [ ] 实现风格学习流程
- [ ] 实现Agent对话交互
- [ ] 实现文章编辑界面
- [ ] 集成智谱GLM API

### Day 3：后端API开发
- [ ] 开发内容生成API
- [ ] 开发风格分析API
- [ ] 实现用户激活API
- [ ] 部署到Vercel

### Day 4：Firebase集成
- [ ] 配置Firebase项目
- [ ] 实现邮箱验证功能
- [ ] 实现额度管理系统
- [ ] 保存生成历史到数据库

### Day 5：测试与上线
- [ ] 完整功能测试
- [ ] 优化用户体验
- [ ] 添加微信支付引导
- [ ] 正式部署上线

---

## 7. 成本估算

### 7.1 启动成本
- 域名：¥0 (使用vercel.app免费域名)
- Vercel托管：¥0 (免费额度足够)
- Firebase Spark Plan：¥0 (免费额度足够)
- 智谱GLM API：¥49 (用户已购买)
- **总计：¥49**

### 7.2 月度运营成本
- Vercel Pro：¥0 (Hobby计划免费)
- Firebase Blaze：¥0-50 (按使用量，初期免费额度足够)
- 智谱GLM API：¥49 (固定成本)
- **预计：¥50-100/月**

### 7.3 盈亏平衡点
- 月付用户：¥29/月 × 2用户 = ¥58
- 年付用户：¥199/年 ÷ 12月 ≈ ¥16.6/月 × 6用户 = ¥99.6
- **目标：10个付费用户/月即可覆盖成本**

---

## 8. 技术风险与应对

### 8.1 风险清单

| 风险项 | 影响 | 概率 | 应对措施 |
|--------|------|------|----------|
| 智谱API限流 | 高 | 中 | 实现请求队列，提示用户稍后重试 |
| Firebase超额费用 | 中 | 低 | 监控使用量，设置告警阈值 |
| 用户流失率高 | 高 | 中 | 优化用户体验，提供3次免费试用 |
| 生成质量不稳定 | 高 | 中 | A/B测试不同prompt，收集反馈优化 |
| Vercel部署失败 | 中 | 低 | 熟悉部署流程，本地测试充分 |

### 8.2 优化方向
1. **性能优化**：实现内容缓存，减少API调用
2. **用户体验**：添加生成动画，提升等待体验
3. **数据分析**：集成Google Analytics，分析用户行为
4. **A/B测试**：测试不同标题风格对点击率的影响

---

## 9. 附录

### 9.1 相关文档
- [PRD.md](./PRD.md) - 产品需求文档
- [Vercel部署指南](https://vercel.com/docs)
- [Firebase文档](https://firebase.google.com/docs)
- [智谱GLM API文档](https://open.bigmodel.cn/dev/api)

### 9.2 联系方式
- 产品负责人：夏树
- 开发周期：5天
- 上线时间：2025-02-13（预计）

---

**文档版本**：v1.0
**最后更新**：2025-02-08
**维护者**：Claude Code (夏树的AI助手)
