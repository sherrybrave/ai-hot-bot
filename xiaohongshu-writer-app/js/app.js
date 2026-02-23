// ========================================
// 小红书笔记生成器 - 主应用逻辑
// ========================================

// 状态管理
const state = {
    currentStep: 1,
    totalSteps: 6,
    referenceContent: '', // 新的单一输入
    referenceArticles: [], // 解析后的文章数组
    userIdea: '',
    selectedTitleIndex: 1,
    tags: ['#效率提升', '#职场经验', '#个人成长'],
    generatedContent: {
        titles: [],
        content: '',
        tags: []
    },
    freeTierRemaining: 2
};

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    initApp();
});

function initApp() {
    // 从 localStorage 读取免费额度
    const savedCount = localStorage.getItem('freeTierRemaining');
    if (savedCount !== null) {
        state.freeTierRemaining = parseInt(savedCount);
    }

    // 绑定导航按钮
    document.getElementById('nextBtn').addEventListener('click', handleNext);
    document.getElementById('prevBtn').addEventListener('click', handlePrev);

    // 绑定输入框（用于实时保存）
    document.getElementById('referenceContent').addEventListener('input', (e) => {
        state.referenceContent = e.target.value;
    });
    document.getElementById('userIdea').addEventListener('input', (e) => {
        state.userIdea = e.target.value;
    });

    // 标签输入框回车事件
    document.getElementById('tagInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            addTag();
        }
    });

    // 更新免费额度显示
    updateFreeTierDisplay();
}

// 处理下一步
function handleNext() {
    if (!validateCurrentStep()) {
        return;
    }

    if (state.currentStep < state.totalSteps) {
        state.currentStep++;
        updateStep();

        // 特殊处理步骤2（自动分析）和步骤4（自动生成）
        if (state.currentStep === 2) {
            startAnalysis();
        } else if (state.currentStep === 4) {
            startGeneration();
        }
    }
}

// 处理上一步
function handlePrev() {
    if (state.currentStep > 1) {
        state.currentStep--;
        updateStep();
    }
}

// 验证当前步骤
function validateCurrentStep() {
    switch(state.currentStep) {
        case 1:
            const content = document.getElementById('referenceContent').value.trim();
            if (!content) {
                alert('请输入参考文章内容或链接');
                return false;
            }

            // 解析文章内容
            state.referenceArticles = parseReferenceContent(content);

            if (state.referenceArticles.length === 0) {
                alert('请输入有效的参考文章内容');
                return false;
            }

            // 检查是否包含链接（未来可以调用 MCP 爬取）
            const hasLinks = state.referenceArticles.some(article =>
                article.includes('xiaohongshu.com') || article.includes('http')
            );

            if (hasLinks) {
                // TODO: 这里可以集成小红书 MCP 进行爬取
                console.log('检测到小红书链接，未来将使用 MCP 爬取内容');
            }

            break;
        case 3:
            const idea = document.getElementById('userIdea').value.trim();
            if (!idea) {
                alert('请输入你想写的内容');
                return false;
            }
            break;
    }
    return true;
}

// 解析参考文章内容
function parseReferenceContent(content) {
    // 先尝试按 --- 分隔
    const separator = '\n---\n';
    if (content.includes(separator)) {
        return content.split(separator).map(item => item.trim()).filter(item => item);
    }

    // 如果没有分隔符，作为单篇文章
    return [content.trim()];
}

// 重置步骤2的分析状态
function resetAnalysisState() {
    // 显示加载状态，隐藏结果
    document.getElementById('analyzingState').classList.remove('hidden');
    document.getElementById('analyzeResult').classList.add('hidden');
}

// 更新步骤显示
function updateStep() {
    // 更新进度条
    const progress = (state.currentStep / state.totalSteps) * 100;
    document.getElementById('progressFill').style.width = progress + '%';

    // 更新步骤指示器
    const steps = document.querySelectorAll('.step');
    steps.forEach((step, index) => {
        const stepNum = index + 1;
        step.classList.remove('active', 'completed');
        if (stepNum < state.currentStep) {
            step.classList.add('completed');
            step.querySelector('.step-circle').innerHTML = '✓';
        } else if (stepNum === state.currentStep) {
            step.classList.add('active');
            step.querySelector('.step-circle').innerHTML = stepNum;
        } else {
            step.querySelector('.step-circle').innerHTML = stepNum;
        }
    });

    // 更新主内容区域
    const stepContents = document.querySelectorAll('.step-content');
    stepContents.forEach((content, index) => {
        if (index + 1 === state.currentStep) {
            content.classList.remove('hidden');

            // 如果是步骤2，重置分析状态
            if (state.currentStep === 2) {
                resetAnalysisState();
            }
        } else {
            content.classList.add('hidden');
        }
    });

    // 更新按钮状态
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');

    if (state.currentStep === 1) {
        prevBtn.style.display = 'none';
    } else {
        prevBtn.style.display = 'block';
    }

    if (state.currentStep === state.totalSteps) {
        nextBtn.style.display = 'none';
    } else {
        nextBtn.style.display = 'block';
        nextBtn.textContent = state.currentStep === 2 ? '下一步 →' : '下一步 →';
    }

    // 滚动到顶部
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 开始分析（步骤2）
function startAnalysis() {
    const analyzeTexts = [
        '正在分析文章风格...',
        '提取写作框架...',
        '学习语言风格...',
        '识别表达习惯...',
        '分析完成！'
    ];

    const analyzeDetails = [
        '提取写作框架中...',
        '识别语气用词中...',
        '分析Emoji使用习惯中...',
        '总结段落结构中...'
    ];

    let step = 0;
    const interval = setInterval(() => {
        if (step < analyzeTexts.length) {
            document.getElementById('analyzeText').textContent = analyzeTexts[step];
            if (step < analyzeDetails.length) {
                document.getElementById('analyzeDetail').textContent = analyzeDetails[step];
            }
            step++;
        } else {
            clearInterval(interval);

            // 隐藏加载状态，展示结果
            setTimeout(() => {
                document.getElementById('analyzingState').classList.add('hidden');
                document.getElementById('analyzeResult').classList.remove('hidden');

                // 更新分析结果
                updateAnalyzeResult();
            }, 500);
        }
    }, 800);
}

// 更新分析结果（步骤2展示）
function updateAnalyzeResult() {
    // 这里应该根据实际分析结果更新
    // 暂时使用模拟数据
    document.getElementById('resultFramework').textContent = '信号列举-干货型';
    document.getElementById('resultFrameworkDesc').textContent = '这种框架适合分享实用技巧和方法论，通过列举多个要点来传递价值。';

    document.getElementById('resultTone').textContent = '轻松活泼';
    document.getElementById('resultVoice').textContent = '第一人称"我"';
    document.getElementById('resultToneDesc').textContent = '使用亲切的语气和第一人称叙述，像和朋友聊天一样分享经验。';

    document.getElementById('resultStructure').textContent = '总分总结构';
    document.getElementById('resultEmoji').textContent = '适当使用 Emoji';

    document.getElementById('resultHabit1').textContent = '常用"和大家分享"作为开场白';
    document.getElementById('resultHabit2').textContent = '喜欢用"第一个"、"第二个"等序数词';
    document.getElementById('resultHabit3').textContent = '经常使用"记住"、"建议"等提醒性词汇';
    document.getElementById('resultHabit4').textContent = '结尾习惯总结观点或给出行动建议';
}

// 更新步骤3的风格标签
function updateStyleTags() {
    // 这里应该根据实际分析结果更新
    // 暂时使用模拟数据
    document.getElementById('styleFramework').textContent = '信号列举-干货型';
    document.getElementById('styleTone').textContent = '轻松活泼';
    document.getElementById('styleStructure').textContent = '总分总结构';
    document.getElementById('styleEmoji').textContent = '适当使用Emoji';
}

// 开始生成（步骤4）
function startGeneration() {
    const generationSteps = [
        { id: 'genStep1', title: '提取框架', desc: '已识别"信号列举-干货型"框架' },
        { id: 'genStep2', title: '融合风格', desc: '正在学习你的表达方式...' },
        { id: 'genStep3', title: '生成内容', desc: '正在撰写正文...' },
        { id: 'genStep4', title: '推荐标题', desc: '正在生成爆款标题...' },
        { id: 'genStep5', title: '生成标签', desc: '正在推荐相关标签...' }
    ];

    const previewTexts = [
        '正在准备生成...',
        '📝 框架：信号列举-干货型\n\n第一个信号...',
        '📝 框架：信号列举-干货型\n\n今天和大家分享3个提高工作效率的方法...\n\n第一个技巧：用杠杆思维替代努力思维...',
        '📝 框架：信号列举-干货型\n\n今天和大家分享3个在互联网大厂工作的效率秘籍...\n\n第一个技巧：用杠杆思维替代努力思维。很多人觉得勤奋就能成功，但其实真正的高手都在用杠杆——用最小的投入获得最大的产出。\n\n第二个技巧：建立个人知识库。不要让有用的信息流失，把每个知识点都系统化整理，这样才能形成复利效应...',
        '今天和大家分享3个在互联网大厂工作的效率秘籍，这些都是我多年实践总结出来的精华。\n\n第一个技巧：用杠杆思维替代努力思维。很多人觉得勤奋就能成功，但其实真正的高手都在用杠杆——用最小的投入获得最大的产出。\n\n第二个技巧：建立个人知识库。不要让有用的信息流失，把每个知识点都系统化整理，这样才能形成复利效应。\n\n第三个技巧：学会说"不"。不是所有事情都值得做，学会判断优先级，把时间花在高价值的事情上。\n\n记住：效率不是做得更多，而是做得更对！'
    ];

    let currentStep = 0;

    function processStep() {
        if (currentStep < generationSteps.length) {
            const step = generationSteps[currentStep];

            // 更新当前步骤
            const stepEl = document.getElementById(step.id);
            stepEl.classList.add('active');

            // 更新已完成步骤
            for (let i = 0; i < currentStep; i++) {
                document.getElementById(generationSteps[i].id).classList.add('completed');
                document.getElementById(generationSteps[i].id).classList.remove('active');
            }

            // 更新步骤描述
            stepEl.querySelector('.progress-step-desc').textContent = step.desc;

            // 更新预览
            if (currentStep < previewTexts.length) {
                document.getElementById('realtimePreview').textContent = previewTexts[currentStep];
            }

            currentStep++;
            setTimeout(processStep, 1500);
        } else {
            // 生成完成，保存结果
            saveGeneratedContent();
            setTimeout(() => {
                updateStep5Content();
                handleNext();
            }, 1000);
        }
    }

    processStep();
}

// 保存生成的内容
function saveGeneratedContent() {
    state.generatedContent = {
        titles: [
            { text: '3个技巧让你效率翻倍', reason: '推荐：数字+痛点+收益' },
            { text: '大厂不说的效率秘籍', reason: '推荐：好奇心+权威感' },
            { text: '别再浪费时间了', reason: '推荐：情绪化+紧迫感' }
        ],
        content: `今天和大家分享3个在互联网大厂工作的效率秘籍，这些都是我多年实践总结出来的精华。

第一个技巧：用杠杆思维替代努力思维。很多人觉得勤奋就能成功，但其实真正的高手都在用杠杆——用最小的投入获得最大的产出。

第二个技巧：建立个人知识库。不要让有用的信息流失，把每个知识点都系统化整理，这样才能形成复利效应。

第三个技巧：学会说"不"。不是所有事情都值得做，学会判断优先级，把时间花在高价值的事情上。

记住：效率不是做得更多，而是做得更对！`,
        tags: ['#效率提升', '#职场经验', '#个人成长']
    };
}

// 更新步骤5的内容
function updateStep5Content() {
    // 更新标题选项
    for (let i = 0; i < 3; i++) {
        document.getElementById('titleOption' + i).textContent = state.generatedContent.titles[i].text;
        document.getElementById('titleReason' + i).textContent = state.generatedContent.titles[i].reason;
    }

    // 更新正文内容
    document.getElementById('editableContent').value = state.generatedContent.content;

    // 更新标签
    updateTagsDisplay();
}

// 选择标题
function selectTitle(element, index) {
    // 移除其他选中状态
    document.querySelectorAll('.title-card').forEach(card => {
        card.classList.remove('selected');
    });

    // 添加当前选中状态
    element.classList.add('selected');
    state.selectedTitleIndex = index;
}

// 添加标签
function addTag() {
    const input = document.getElementById('tagInput');
    const tag = input.value.trim();

    if (!tag) return;

    if (state.tags.length >= 5) {
        alert('最多只能添加5个标签');
        return;
    }

    // 添加 # 前缀
    const formattedTag = tag.startsWith('#') ? tag : '#' + tag;
    state.tags.push(formattedTag);

    input.value = '';
    updateTagsDisplay();
}

// 更新标签显示
function updateTagsDisplay() {
    const container = document.getElementById('selectedTags');
    container.innerHTML = '';

    state.tags.forEach((tag, index) => {
        const tagEl = document.createElement('span');
        tagEl.className = 'tag';
        tagEl.textContent = tag;
        tagEl.onclick = () => removeTag(index);
        container.appendChild(tagEl);
    });
}

// 删除标签
function removeTag(index) {
    state.tags.splice(index, 1);
    updateTagsDisplay();
}

// 复制内容
function copyContent() {
    const title = state.generatedContent.titles[state.selectedTitleIndex].text;
    const content = document.getElementById('editableContent').value;
    const tags = state.tags.join(' ');

    const fullContent = `${title}\n\n${content}\n\n${tags}`;

    navigator.clipboard.writeText(fullContent).then(() => {
        alert('已复制到剪贴板！');

        // 减少免费额度
        if (state.freeTierRemaining > 0) {
            state.freeTierRemaining--;
            localStorage.setItem('freeTierRemaining', state.freeTierRemaining);
            updateFreeTierDisplay();
        }
    }).catch(() => {
        alert('复制失败，请手动复制');
    });
}

// 重新生成
function regenerate() {
    if (state.freeTierRemaining <= 0) {
        alert('免费额度已用完，请升级到 Pro 版本');
        return;
    }

    if (confirm('确定要重新生成吗？这将消耗一次免费额度')) {
        state.currentStep = 4;
        updateStep();
        startGeneration();
    }
}

// 再写一篇
function startOver() {
    if (confirm('确定要开始新的一篇吗？')) {
        // 重置状态
        state.currentStep = 1;
        state.referenceContent = '';
        state.referenceArticles = [];
        state.userIdea = '';
        state.tags = ['#效率提升', '#职场经验', '#个人成长'];

        // 清空输入框
        document.getElementById('referenceContent').value = '';
        document.getElementById('userIdea').value = '';

        // 重置步骤
        updateStep();
    }
}

// 更新免费额度显示
function updateFreeTierDisplay() {
    document.getElementById('remainingCount').textContent = state.freeTierRemaining;

    const notice = document.getElementById('freeTierNotice');
    if (state.freeTierRemaining <= 0) {
        notice.innerHTML = '⚠️ 免费额度已用完 | <a href="#" style="color: inherit; text-decoration: underline;">升级到 Pro 版本</a> 解锁无限次生成';
    }
}
