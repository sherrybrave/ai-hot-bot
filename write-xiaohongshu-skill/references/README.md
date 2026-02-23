# 参考资料 - 索引和导航

欢迎来到 write-xiaohongshu skill 的参考资料库！

## 📁 文件夹结构

```
write-xiaohongshu-skill/
│
├── SKILL.md                   # 核心指令（必读）
│   - 使用场景、工作流程、用户风格
│   - 精简版，只保留核心内容
│
├── knowledge/                 # 知识库（持续进化）
│   ├── user-feedback.md      # 用户纠正和反馈
│   ├── success-patterns.md   # 成功模式和经验
│   ├── writing-style.md      # 文风学习和进化
│   ├── special-cases.md      # 特殊情况和处理
│   └── framework-insights.md # 框架使用心得
│
├── guides/                   # 操作指南
│   ├── add-reference-article.md    # 如何新增参考文章
│   ├── file-management.md         # 文件管理规范
│   └── manage-frameworks.md        # 如何管理框架类型
│
└── references/               # 参考资料（本文件夹）
    ├── classification.md     # 框架分类规则
    ├── frameworks.md         # 框架模板库
    ├── style-guide.md        # 用户文风指南
    └── articles/             # 参考文章库（50-60篇）
        ├── experience-list/
        ├── problem-solution-list/
        └── ...（11个框架类型）
```

## 🔍 knowledge/ vs references/ 的区别

**核心区别**：
- **knowledge/** = "如何用"（经验、教训、反思）
- **references/** = "用什么"（框架、文章、规则）

| 维度 | knowledge/ | references/ |
|------|-----------|------------|
| **性质** | 动态、持续进化 | 静态、相对稳定 |
| **内容** | 学习过程、经验教训 | 具体数据、资源 |
| **更新频率** | 每次任务后更新 | 按需更新 |
| **格式** | 有时间戳、反思、改进建议 | 结构化文档、模板 |
| **示例** | "用户纠正了文风 AI 味" | "框架的定义和结构" |

### 具体对比

**frameworks.md vs framework-insights.md**
- **frameworks.md**（参考）：框架的静态定义、结构模板、适用场景
- **framework-insights.md**（知识）：框架的使用心得、成功案例、避坑指南

**style-guide.md vs writing-style.md**
- **style-guide.md**（参考）：用户的文风特点、常用表达、金句库、写作禁忌
- **writing-style.md**（知识）：文风的进化历程、纠正记录、AI vs 人工对比

**classification.md vs knowledge（整体）**
- **classification.md**（参考）：框架类型的定义和判断标准
- **knowledge/**（知识）：学习如何正确使用这些框架类型

## 📚 各文件用途

### 核心文件

**SKILL.md**
- Skill 的核心指令
- 使用场景、工作流程、用户风格特点
- 精简版（132行），专注核心内容

### 参考资料（references/）

**classification.md** - 框架分类规则
- 11种框架类型的定义
- 框架类型判断标准
- 如何分类一篇文章

**frameworks.md** - 框架模板库
- 每种框架的写作模板
- 结构图、关键技巧
- 适用场景

**style-guide.md** - 用户文风指南
- 用户的语气、句式、表达习惯
- 常用表达、金句库
- **写作禁忌**（重要！）

**articles/** - 参考文章库
- 50-60篇小红书爆款笔记
- 按11种框架类型分类
- `my-*.md`（用户爆款）+ `others-*.md`（别人爆款）

### 知识库（knowledge/）

**user-feedback.md** - 用户纠正和反馈
- 记录每次用户给出的纠正
- 学习用户的真实需求
- 避免重复犯错

**success-patterns.md** - 成功模式和经验
- 提炼可复用的成功模式
- 标准化执行流程
- 记录最佳实践

**writing-style.md** - 文风学习和进化
- 用户的真实文风特点
- AI 常见错误 vs 用户真实风格
- 文风进化历程

**special-cases.md** - 特殊情况和处理
- 记录遇到的特殊情况
- 如何处理边界情况
- 特殊需求的解决方案

**framework-insights.md** - 框架使用心得
- 框架的使用经验
- 成功案例分析
- 避坑指南

### 操作指南（guides/）

**add-reference-article.md** - 如何新增参考文章
- 完整的7步流程
- 常见问题解答

**file-management.md** - 文件管理规范
- 双路径机制
- 文件夹结构
- 文件命名规范

**manage-frameworks.md** - 如何管理框架类型
- 当前11种框架类型总览
- 如何添加新框架
- 框架对比决策表

## 🎯 快速导航

**我想...**

- 写小红书笔记 → 阅读 [SKILL.md](../SKILL.md)
- 新增参考文章 → 阅读 [guides/add-reference-article.md](../guides/add-reference-article.md)
- 了解框架类型 → 阅读 [classification.md](classification.md)
- 学习写作框架 → 阅读 [frameworks.md](frameworks.md)
- 了解用户文风 → 阅读 [style-guide.md](style-guide.md)
- 查看历史经验 → 浏览 [knowledge/](../knowledge/)
- 管理文件 → 阅读 [guides/file-management.md](../guides/file-management.md)

## 💡 使用建议

1. **先读核心文件**：SKILL.md、classification.md、frameworks.md
2. **遇到问题查指南**：guides/ 下的操作指南
3. **积累经验看知识库**：knowledge/ 会持续进化
4. **保持参考文章质量**：只收藏真正有用的爆款笔记

---

**维护说明**：
- knowledge/ 和 guides/ 会随着使用持续更新
- references/ 相对稳定，按需更新
- 所有更新都要同步到全局路径
