// ==================== 测试题功能 ====================

// 全局变量
let currentMode = 'single'; // 'single' 或 'all'
let currentQuestionIndex = 1; // 当前题目索引（从1开始）
let answeredCount = 0;
const totalQuestions = document.querySelectorAll('.question-card').length;

// 页面加载时
document.addEventListener('DOMContentLoaded', () => {
    updateProgress();
    updateNavigation();
});

// ==================== 题目导航 ====================

function goToQuestion(index) {
    // 隐藏当前题目
    document.querySelectorAll('.question-card').forEach(card => {
        card.classList.remove('active');
    });

    // 显示目标题目
    const targetCard = document.getElementById(`question-${index}`);
    if (targetCard) {
        targetCard.classList.add('active');
        currentQuestionIndex = index;

        // 更新导航
        updateNavigation();

        // 滚动到题目顶部
        targetCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

function prevQuestion() {
    if (currentQuestionIndex > 1) {
        goToQuestion(currentQuestionIndex - 1);
    }
}

function nextQuestion() {
    if (currentQuestionIndex < totalQuestions) {
        goToQuestion(currentQuestionIndex + 1);
    }
}

function updateNavigation() {
    // 更新导航信息
    document.getElementById('navInfo').textContent = `${currentQuestionIndex} / ${totalQuestions}`;

    // 更新按钮状态
    document.getElementById('prevBtn').disabled = (currentQuestionIndex === 1);
    document.getElementById('nextBtn').disabled = (currentQuestionIndex === totalQuestions);

    // 更新导航网格的高亮
    document.querySelectorAll('.question-nav-item').forEach(item => {
        item.classList.remove('active');
        if (parseInt(item.dataset.questionIndex) === currentQuestionIndex) {
            item.classList.add('active');
        }
    });
}

// ==================== 模式切换 ====================

function switchMode(mode) {
    currentMode = mode;
    const buttons = document.querySelectorAll('.mode-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    const questionCards = document.querySelectorAll('.question-card');
    const questionNav = document.getElementById('questionNav');

    if (mode === 'all') {
        // 全部显示模式
        questionCards.forEach(card => {
            card.classList.remove('single-mode');
            card.classList.add('all-mode');
            card.classList.add('active'); // 显示所有题目
        });
        questionNav.classList.remove('single-mode-nav');
    } else {
        // 一题一页模式
        questionCards.forEach(card => {
            card.classList.remove('all-mode');
            card.classList.add('single-mode');
            card.classList.remove('active'); // 隐藏所有题目
        });
        // 只显示当前题目
        goToQuestion(currentQuestionIndex);
        questionNav.classList.add('single-mode-nav');
    }
}

// ==================== 答案保存 ====================

async function saveAnswer(questionId, answer) {
    try {
        const response = await fetch('/api/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                quiz_file: QUIZ_FILE,
                question_id: questionId,
                answer: answer
            })
        });

        if (response.ok) {
            const data = await response.json();
            console.log('已保存:', data.saved_at);

            // 更新进度
            updateProgress();

            // 显示保存提示
            showSaveNotification(questionId);
        }
    } catch (error) {
        console.error('保存失败:', error);
    }
}

async function saveOpenAnswer(questionId, answer) {
    // 开放性问题使用防抖保存，避免每次输入都保存
    if (window.saveTimeout) {
        clearTimeout(window.saveTimeout);
    }

    window.saveTimeout = setTimeout(async () => {
        await saveAnswer(questionId, answer);
    }, 1000); // 1秒后保存
}

function toggleExplanation(questionId) {
    const explanationBox = document.getElementById(`explanation-${questionId}`);
    if (explanationBox) {
        const isHidden = explanationBox.style.display === 'none';
        explanationBox.style.display = isHidden ? 'block' : 'none';
    }
}

function showSaveNotification(questionId) {
    const statusEl = document.getElementById(`status-${questionId}`);
    if (statusEl) {
        statusEl.textContent = '✓ 已保存';
        statusEl.style.color = 'var(--success-color)';

        setTimeout(() => {
            statusEl.textContent = '';
        }, 2000);
    }
}

// ==================== 进度更新 ====================

function updateProgress() {
    const total = document.querySelectorAll('.question-card').length;

    // 统计已答题数（包括选择题和开放题）
    let answered = 0;
    document.querySelectorAll('.question-card').forEach((card, index) => {
        const questionId = card.dataset.questionId;
        const hasRadioAnswer = card.querySelector(`input[type="radio"]:checked`);
        const textarea = card.querySelector('textarea');
        const hasOpenAnswer = textarea && textarea.value.trim();

        const isAnswered = hasRadioAnswer || hasOpenAnswer;

        // 更新题目导航的状态
        const navItem = document.querySelector(`.question-nav-item[data-question-index="${index + 1}"]`);
        if (navItem) {
            if (isAnswered) {
                navItem.classList.add('answered');
            } else {
                navItem.classList.remove('answered');
            }
        }

        if (isAnswered) {
            answered++;
        }
    });

    answeredCount = answered;

    document.getElementById('answeredCount').textContent = answered;
    document.getElementById('totalCount').textContent = total;

    const percentage = (answered / total) * 100;
    document.getElementById('progressFill').style.width = `${percentage}%`;
}

// ==================== 提交答案 ====================

async function submitQuiz() {
    const answered = document.querySelectorAll('input[type="radio"]:checked').length;
    const total = document.querySelectorAll('.question-card').length;

    if (answered === 0) {
        alert('请先回答至少一道题！');
        return;
    }

    if (!confirm(`你已完成 ${answered}/${total} 题，确定要提交答案吗？`)) {
        return;
    }

    // 收集答案
    const questions = document.querySelectorAll('.question-card');
    const answers = {};

    questions.forEach(q => {
        const questionId = q.dataset.questionId;
        const selected = q.querySelector(`input[type="radio"]:checked`);

        if (selected) {
            answers[questionId] = selected.value;
        }
    });

    try {
        const response = await fetch('/api/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                quiz_file: QUIZ_FILE,
                answers: answers
            })
        });

        if (response.ok) {
            const data = await response.json();
            showResults(data);
        }
    } catch (error) {
        console.error('提交失败:', error);
        alert('提交失败，请重试');
    }
}

function showResults(data) {
    const resultArea = document.getElementById('resultArea');
    const scoreSummary = document.getElementById('scoreSummary');
    const resultDetails = document.getElementById('resultDetails');

    // 统计选择题得分（开放性问题不计分）
    const choiceResults = data.results.filter(r => r.type === 'choice');
    const choiceCorrect = choiceResults.filter(r => r.is_correct).length;
    const choiceTotal = choiceResults.length;

    // 显示分数
    if (choiceTotal > 0) {
        const percentage = choiceTotal > 0 ? Math.round(choiceCorrect / choiceTotal * 100) : 0;
        scoreSummary.innerHTML = `
            <div class="score-card">
                <h3>选择题得分：${choiceCorrect}/${choiceTotal} (${percentage}%)</h3>
                <p style="margin-top: 0.5rem; color: var(--text-secondary);">
                    ${data.results.length - choiceResults.length > 0 ? `还有 ${data.results.length - choiceResults.length} 道开放性问题（不计分）` : ''}
                </p>
            </div>
        `;
    } else {
        scoreSummary.innerHTML = `
            <div class="score-card">
                <h3>提交成功！</h3>
                <p style="margin-top: 0.5rem; color: var(--text-secondary);">
                    这套题包含 ${data.results.length} 道开放性问题，请查看详细答案和解析。
                </p>
            </div>
        `;
    }

    // 显示详细结果
    let detailsHTML = '<div class="result-details-list">';

    data.results.forEach((result, index) => {
        const isChoice = result.type === 'choice';
        const isCorrect = result.is_correct;
        const statusClass = isChoice && isCorrect ? 'correct' : (isChoice && !isCorrect ? 'incorrect' : 'open');
        const statusIcon = isChoice ? (isCorrect ? '✓' : '✗') : '📝';

        detailsHTML += `
            <div class="result-item ${statusClass}">
                <div class="result-header">
                    <span class="result-number">题目 ${result.number}</span>
                    <span class="result-status">${statusIcon}</span>
                </div>
                <div class="result-question">${result.text}</div>

                ${isChoice ? `
                <div class="result-answer">
                    <strong>你的答案：</strong>${result.user_answer || '未作答'}
                    <span class="result-correct">${isCorrect ? '✓' : '✗'} 正确答案：${result.correct_answer}</span>
                </div>
                ` : `
                <div class="result-answer">
                    <strong>你的答案：</strong>${result.user_answer || '未作答'}
                </div>
                `}

                ${result.explanation ? `<div class="result-explanation"><strong>✨ 解析：</strong>${result.explanation}</div>` : ''}
            </div>
        `;
    });

    detailsHTML += '</div>';
    resultDetails.innerHTML = detailsHTML;

    // 显示结果区域
    resultArea.style.display = 'block';
    resultArea.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // 在一题一页模式下，隐藏题目导航；全部显示模式下，隐藏题目
    if (currentMode === 'single') {
        document.getElementById('questionNav').style.display = 'none';
        document.getElementById('questionsContainer').style.display = 'none';
    } else {
        document.getElementById('questionsContainer').style.display = 'none';
    }
}

// ==================== 辅助功能 ====================

function showQuizList() {
    window.location.href = '/quizzes';
}
