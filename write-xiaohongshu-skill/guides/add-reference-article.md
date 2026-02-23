# 新增参考文章指南

当用户要求"新增参考文章"时，按以下流程执行。

## 完整流程

### Step 1: 分析文章结构

阅读文章，判断：
- 开头手法（故事/问题/数据/观点...）
- 主体结构（并列列举/递进深入/对比...）
- 结尾方式（总结/呼吁/建议...）

### Step 2: 确定框架类型

1. 读取 `references/classification.md`
2. 对照框架类型定义，找到最匹配的类型
3. 如果无法匹配现有类型：
   - 询问用户是否创建新框架类型
   - 或选择最接近的类型，并在备注中说明

**常见框架类型**（11种）：
- `problem-solution-list`：问题→解决方案（方法论导向）
- `experience-list`：话题→感悟列举（思考/反思导向）
- `rant-list`：吐槽列举型
- `truth-reveal-perspective`：真相揭示-视角递进型
- `signal-list-blessing`：信号列举-祝福型
- `personal-narrative`：个人叙事型
- `theory-application`：理论-应用型
- （还有4种...）

### Step 3: 确定文件编号

**重要**：先检查编号是否被占用！

```bash
# 查找所有 others-*.md 文件
find references/articles -name "others-*.md" | sort

# 查找所有 my-*.md 文件
find references/articles -name "my-*.md" | sort
```

- 别人的文章：`others-[编号].md`
- 你的文章：`my-[编号].md`
- 选择当前最大编号 +1

### Step 4: 创建文章文件

在对应框架类型的文件夹下创建文件：
```bash
references/articles/[框架类型]/others-[编号].md
```

使用以下模板：

```markdown
# 文章标题

**分类**：[框架类型]
**主题**：[文章主题]
**风格**：[文章风格]
**来源**：小红书 @[作者名]
**添加时间**：2026-MM-DD

---

[文章正文]

---

**备注**：
- 框架特点：[记录这篇文章的框架特点]
- 核心亮点：[记录值得学习的亮点]
```

### Step 5: 更新相关文档

**如果是新的框架类型**，需要更新以下文件：

1. **classification.md**
   - 添加新框架类型定义
   - 包含：判断标准、典型特征、适用主题、核心成功因素

2. **frameworks.md**
   - 添加新框架的写作模板
   - 包含：结构图、关键技巧、与现有框架的区别

3. **SKILL.md**
   - 更新框架类型数量
   - 在示例中添加新框架类型名称

**如果是现有框架类型**：
- 只需创建文章文件，无需更新其他文档

### Step 6: 双路径同步

**重要**：必须同步两个路径！

1. **项目路径**（用于 IDE 编辑）：
   ```bash
   ~/Documents/AI/Claude Code/write-xiaohongshu-skill/
   ```

2. **全局路径**（skill 实际使用）：
   ```bash
   ~/.claude/skills/write-xiaohongshu/
   ```

同步以下内容：
- 新创建的文章文件
- 更新的 classification.md、frameworks.md、SKILL.md

验证同步：
```bash
diff 项目路径文件 全局路径文件
```

### Step 7: 向用户报告完成情况

完成后，告诉用户：
1. 文章归档位置（框架类型 + 编号）
2. 是否创建了新框架类型
3. 更新了哪些文件
4. 双路径同步状态

## 常见问题

**Q: 如何判断框架类型？**
A: 阅读 `references/classification.md`，对照定义进行匹配。如果不确定，询问用户。

**Q: 文件编号冲突怎么办？**
A: 使用 `find` 命令查找所有现有编号，选择最大编号 +1。

**Q: 需要创建新框架类型吗？**
A: 只有在现有类型都不匹配时才创建。先询问用户意见。

**Q: 如何同步两个路径？**
A: 使用 `cp` 命令复制文件，然后用 `diff` 验证。
