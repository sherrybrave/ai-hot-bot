# 文件管理规范

## 双路径机制

本 Skill 使用双路径机制，确保开发和运行环境同步：

### 项目路径
- **位置**：`~/Documents/AI/Claude Code/write-xiaohongshu-skill/`
- **用途**：IDE 编辑、版本控制、手动修改
- **特点**：方便在 IDE 中查看和编辑

### 全局路径
- **位置**：`~/.claude/skills/write-xiaohongshu/`
- **用途**：Skill 实际执行时使用
- **特点**：Claude Code 运行时读取

### 同步规则

**必须同步的文件**：
- SKILL.md
- references/ 下所有文件
- knowledge/ 下所有文件
- guides/ 下所有文件

**同步方式**：
```bash
# 同步单个文件
cp 项目路径文件 全局路径文件

# 同步整个文件夹
cp -r 项目路径文件夹/* 全局路径文件夹/

# 验证同步
diff 项目路径文件 全局路径文件
```

## 文件夹结构

```
write-xiaohongshu-skill/
├── SKILL.md                    # 核心指令（精简版）
│
├── knowledge/                  # 知识库（持续进化）
│   ├── user-feedback.md       # 用户纠正和反馈
│   ├── success-patterns.md    # 成功模式
│   ├── writing-style.md       # 文风学习
│   ├── special-cases.md       # 特殊情况
│   └── framework-insights.md  # 框架心得
│
├── guides/                    # 操作指南
│   ├── add-reference-article.md
│   ├── manage-frameworks.md
│   └── file-management.md
│
└── references/                # 参考资料
    ├── README.md              # 索引和导航
    ├── classification.md      # 框架分类规则
    ├── frameworks.md          # 框架模板库
    ├── style-guide.md         # 文风指南
    └── articles/              # 参考文章库
        ├── experience-list/
        ├── problem-solution-list/
        └── ...（11个框架类型）
```

## 文件命名规范

### 参考文章文件名

**你的文章**：`my-[序号].md`
- 例如：`my-01.md`、`my-02.md`

**别人的文章**：`others-[序号].md`
- 例如：`others-01.md`、`others-10.md`

**序号规则**：
- 每个框架类型独立编号
- 选择当前最大编号 +1
- 先查询是否被占用

### 框架类型文件夹名

使用描述性名称（小写，连字符分隔）：
- `problem-solution-list`
- `experience-list`
- `rant-list`
- `truth-reveal-perspective`
- `signal-list-blessing`
- `personal-narrative`
- `theory-application`
- （还有4种...）

## 维护建议

### 定期清理
- **文章规模**：总篇数 50-60 篇
- **时效性**：定期删除过时的框架和文章
- **新鲜度**：保持框架多样性，避免重复

### 质量筛选
- 只收藏**数据好**的笔记
- 优先收藏**框架清晰**的笔记
- 保留**风格差异大**的文章

### 版本控制
- 项目路径建议使用 Git 管理
- 定期提交变更
- 写清楚 commit message
