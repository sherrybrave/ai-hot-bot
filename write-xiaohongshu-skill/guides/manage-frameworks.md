# 框架管理指南

## 框架类型总览

当前共有 11 种框架类型：

1. **problem-solution-list** - 问题-解决-列举型
2. **experience-list** - 感悟列举型
3. **rant-list** - 吐槽列举型
4. **truth-reveal-perspective** - 真相揭示-视角递进型
5. **signal-list-blessing** - 信号列举-祝福型
6. **personal-narrative** - 个人叙事型
7. **theory-application** - 理论-应用型
8. **game-metaphor** - 游戏比喻型
9. **industry-analysis** - 行业分析型
10. **social-observation** - 社会观察型
11. **viewpoint-argument** - 观点-论证型

## 如何添加新框架类型

### 判断是否需要创建

**不需要创建的情况**：
- 文章能归入现有类型（即使不完全匹配）
- 只是文风差异，不是结构差异

**需要创建的情况**：
- 文章结构与所有现有类型都不匹配
- 有全新的写作逻辑和结构
- 用户明确要求创建新类型

### 创建步骤

1. **定义框架类型**
   - 在 `classification.md` 中添加完整定义
   - 包含：判断标准、典型特征、适用主题、核心成功因素

2. **创建写作模板**
   - 在 `frameworks.md` 中添加框架模板
   - 包含：结构图、关键技巧、与其他框架的区别

3. **创建文件夹**
   ```bash
   mkdir -p references/articles/[新框架类型]
   mkdir -p ~/.claude/skills/write-xiaohongshu/references/articles/[新框架类型]
   ```

4. **更新 SKILL.md**
   - 更新框架类型数量
   - 在示例中添加新框架名称

5. **双路径同步**
   - 同步所有更新的文件

### 框架定义模板

在 `classification.md` 中添加：

```markdown
### [框架名称]

**判断标准**：
- 判断标准1
- 判断标准2
- 判断标准3

**典型特征**：
- 特征1
- 特征2
- 特征3

**适用主题**：
- 主题类型1
- 主题类型2
- 主题类型3

**示例文章**：[参考文章编号]

**核心成功因素**：
- ⭐⭐⭐⭐⭐ 成功因素1
- ⭐⭐⭐⭐⭐ 成功因素2
```

## 框架对比决策表

| 框架类型 | 核心特征 | 适用场景 | 判断关键词 |
|---------|---------|---------|-----------|
| problem-solution-list | 问题→解决方案 | 干货分享类 | 提出问题、列举方法 |
| experience-list | 话题→感悟列举 | 职场感悟类 | 感悟、收获、经验 |
| rant-list | 吐槽列举 | 吐槽发泄类 | 十大、至暗时刻 |
| truth-reveal-perspective | 真相揭示-多视角 | 揭示隐秘规则 | 停止X、不是X而是Y |
| signal-list-blessing | 信号列举-祝福 | 祝福类 | 晋升信号、好运、预示 |
| personal-narrative | 个人叙事 | 个人成长类 | 时间线、转折、规划 |
| theory-application | 理论→应用 | 方法论类 | 引用理论、拆解步骤 |

## 框架维护建议

### 定期回顾
- 每月检查框架使用频率
- 删除从未使用的框架类型
- 合并相似度过高的框架

### 持续优化
- 根据用户反馈优化框架定义
- 补充更多示例文章
- 完善写作模板

### 文档同步
- 每次添加框架后，更新相关文档
- 保持 classification.md 和 frameworks.md 一致性
- 更新 SKILL.md 中的框架数量
