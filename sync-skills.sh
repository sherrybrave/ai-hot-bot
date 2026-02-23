#!/bin/bash
# Skill 同步脚本
# 自动在两个位置同步更新 skill 文件
#
# 使用方法：
#   ./sync-skills.sh analyze-xhs-topic-skill
#   ./sync-skills.sh write-xihongshu-skill

set -e

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# 检查参数
if [ $# -lt 1 ]; then
    echo -e "${RED}错误: 缺少 skill 名称${NC}"
    echo ""
    echo "用法: $0 <skill-name>"
    echo ""
    echo "示例:"
    echo "  $0 analyze-xhs-topic-skill"
    echo "  $0 write-xiaohongshu-skill"
    echo ""
    echo "可用的 skills:"
    echo "  - analyze-xhs-topic-skill (小红书选题分析)"
    echo "  - write-xiaohongshu-skill (写小红书笔记)"
    exit 1
fi

SKILL_NAME="$1"

# 定义路径
PROJECT_DIR="/Users/it/Documents/AI/Claude Code/${SKILL_NAME}"

# 特殊处理 write-xiaohongshu-skill（软链接）
if [ "$SKILL_NAME" = "write-xiaohongshu-skill" ]; then
    GLOBAL_DIR="/Users/it/.agents/skills/write-xiaohongshu"
else
    GLOBAL_DIR="/Users/it/.claude/skills/${SKILL_NAME}"
fi

# 检查 skill 是否存在
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}错误: 项目目录不存在: ${PROJECT_DIR}${NC}"
    exit 1
fi

if [ ! -d "$GLOBAL_DIR" ]; then
    echo -e "${RED}错误: 全局目录不存在: ${GLOBAL_DIR}${NC}"
    exit 1
fi

# 显示同步信息
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}  Skill 同步工具${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "Skill 名称: ${GREEN}${SKILL_NAME}${NC}"
echo ""
echo -e "${YELLOW}项目位置${NC}: ${PROJECT_DIR}"
echo -e "${YELLOW}全局位置${NC}: ${GLOBAL_DIR}"
echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# 同步函数
sync_file() {
    local file="$1"
    local project_file="${PROJECT_DIR}/${file}"
    local global_file="${GLOBAL_DIR}/${file}"

    # 检查文件是否存在
    if [ ! -f "$project_file" ] && [ ! -f "$global_file" ]; then
        echo -e "${YELLOW}⚠️  跳过: ${file} (两边都不存在)${NC}"
        return
    fi

    # 判断哪个文件是最新的
    if [ -f "$project_file" ] && [ -f "$global_file" ]; then
        if [ "$project_file" -nt "$global_file" ]; then
            # 项目文件更新，复制到全局
            echo -e "${GREEN}→${NC} 全局 ← 项目: ${file}"
            cp "$project_file" "$global_file"
        elif [ "$global_file" -nt "$project_file" ]; then
            # 全局文件更新，复制到项目
            echo -e "${GREEN}←${NC} 项目 ← 全局: ${file}"
            cp "$global_file" "$project_file"
        else
            echo -e "${BLUE}✓${NC} 已同步: ${file}"
        fi
    elif [ -f "$project_file" ]; then
        # 只有项目文件存在
        echo -e "${GREEN}→${NC} 全局 ← 项目: ${file}"
        cp "$project_file" "$global_file"
    elif [ -f "$global_file" ]; then
        # 只有全局文件存在
        echo -e "${GREEN}←${NC} 项目 ← 全局: ${file}"
        cp "$global_file" "$project_file"
    fi
}

# 同步 SKILL.md
echo -e "${BLUE}正在同步 SKILL.md...${NC}"
sync_file "SKILL.md"
echo ""

# 同步 references 目录
if [ -d "${PROJECT_DIR}/references" ] || [ -d "${GLOBAL_DIR}/references" ]; then
    echo -e "${BLUE}正在同步 references/...${NC}"

    # 确保目标目录存在
    mkdir -p "${GLOBAL_DIR}/references"
    mkdir -p "${PROJECT_DIR}/references"

    # 同步 references 目录下的所有文件
    for ref_file in "${PROJECT_DIR}/references/"* "${GLOBAL_DIR}/references/"*; do
        if [ -f "$ref_file" ]; then
            filename=$(basename "$ref_file")
            sync_file "references/${filename}"
        fi
    done
    echo ""
fi

# 同步 scripts 目录
if [ -d "${PROJECT_DIR}/scripts" ] || [ -d "${GLOBAL_DIR}/scripts" ]; then
    echo -e "${BLUE}正在同步 scripts/...${NC}"

    # 确保目标目录存在
    mkdir -p "${GLOBAL_DIR}/scripts"
    mkdir -p "${PROJECT_DIR}/scripts"

    # 同步 scripts 目录下的所有文件
    for script_file in "${PROJECT_DIR}/scripts/"* "${GLOBAL_DIR}/scripts/"*; do
        if [ -f "$script_file" ]; then
            filename=$(basename "$script_file")
            sync_file "scripts/${filename}"

            # 保持脚本可执行权限
            chmod +x "${PROJECT_DIR}/scripts/${filename}" 2>/dev/null || true
            chmod +x "${GLOBAL_DIR}/scripts/${filename}" 2>/dev/null || true
        fi
    done
    echo ""
fi

# 同步 assets 目录
if [ -d "${PROJECT_DIR}/assets" ] || [ -d "${GLOBAL_DIR}/assets" ]; then
    echo -e "${BLUE}正在同步 assets/...${NC}"

    # 确保目标目录存在
    mkdir -p "${GLOBAL_DIR}/assets"
    mkdir -p "${PROJECT_DIR}/assets"

    # 递归同步 assets 目录下的所有文件
    # 注意: assets 通常存储生成的报告，只同步目录结构，不覆盖已有文件
    if [ -d "${PROJECT_DIR}/assets" ]; then
        find "${PROJECT_DIR}/assets" -type d | while read dir; do
            relative_path="${dir#${PROJECT_DIR}/assets/}"
            mkdir -p "${GLOBAL_DIR}/assets/${relative_path}"
        done
    fi

    if [ -d "${GLOBAL_DIR}/assets" ]; then
        find "${GLOBAL_DIR}/assets" -type d | while read dir; do
            relative_path="${dir#${GLOBAL_DIR}/assets/}"
            mkdir -p "${PROJECT_DIR}/assets/${relative_path}"
        done
    fi

    echo -e "${BLUE}✓${NC} assets 目录结构已同步"
    echo ""
fi

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ 同步完成！${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}提示:${NC} 两个位置已完全同步"
