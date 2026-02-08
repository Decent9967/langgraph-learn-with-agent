#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LangGraph 学习平台 - Web 应用

创建时间：2025-02-08
作者：LangGraph 学习项目
功能：提供讲义浏览和测试题答题功能
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
import markdown
from pygments import highlight
from pygments.lexers import PythonLexer, get_lexer_by_name
from pygments.formatters import HtmlFormatter

app = Flask(__name__)

# 配置
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# 项目路径
BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / 'docs'
QUIZZES_DIR = BASE_DIR / 'examples' / 'phase01_basics' / 'quizzes'
ANSWERS_FILE = QUIZZES_DIR / 'answers.json'


# ==================== 辅助函数 ====================

def build_navigation():
    """构建动态导航树"""
    nav = {
        'lectures': [],
        'quizzes': []
    }

    # 扫描讲义
    for phase_dir in sorted(DOCS_DIR.glob('phase*')):
        phase_name = extract_phase_name(phase_dir)
        lectures = []

        for md_file in sorted(phase_dir.glob('*.md')):
            if md_file.name == 'README.md':
                continue

            title = extract_title(md_file)
            lectures.append({
                'file': str(md_file.relative_to(BASE_DIR)),
                'title': title,
                'phase': phase_name
            })

        if lectures:
            nav['lectures'].append({
                'phase': phase_name,
                'items': lectures
            })

    # 扫描测试题
    examples_dir = BASE_DIR / 'examples'
    for phase_dir in sorted(examples_dir.glob('phase*')):
        phase_name = extract_phase_name(phase_dir)
        quizzes_dir = phase_dir / 'quizzes'

        if not quizzes_dir.exists():
            continue

        quizzes = []
        for quiz_file in sorted(quizzes_dir.glob('*.md')):
            title = extract_quiz_title(quiz_file)
            question_count = count_questions(quiz_file)

            quizzes.append({
                'file': str(quiz_file.relative_to(BASE_DIR)),
                'title': title,
                'count': question_count,
                'phase': phase_name
            })

        if quizzes:
            nav['quizzes'].append({
                'phase': phase_name,
                'items': quizzes
            })

    return nav


def extract_phase_name(phase_dir):
    """从目录名提取阶段名称"""
    name = phase_dir.name
    # phase01_basics -> 第一阶段：基础概念
    match = re.match(r'phase(\d+)_(.+)', name)
    if match:
        num = match.group(1)
        eng_name = match.group(2).replace('_', ' ').title()
        return f"第{num}阶段：{eng_name}"
    return name


def extract_title(md_file):
    """从 Markdown 文件提取标题"""
    content = md_file.read_text(encoding='utf-8')
    # 查找第一个一级标题
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1)
    return md_file.stem


def extract_quiz_title(quiz_file):
    """从测试题文件提取标题"""
    content = quiz_file.read_text(encoding='utf-8')
    # 查找标题（通常是文件名的友好格式）
    stem = quiz_file.stem
    # 05_quiz_set1_basics -> 基础知识强化（第1套）
    match = re.match(r'\d+_quiz_(set\d+)_(.+)', stem)
    if match:
        set_name = match.group(1)
        topic = match.group(2).replace('_', ' ')
        return f"{topic}（{set_name}）"
    return stem


def count_questions(quiz_file):
    """统计题目数量

    使用与 parse_quiz() 相同的灵活匹配模式，支持：
    - ### 题目1：
    - ### 问题1：
    - ### Question 1:
    - ### [类型:choice] 题目1：
    """
    content = quiz_file.read_text(encoding='utf-8')
    # 移除总结和答案汇总部分，避免误匹配
    content_only = re.split(r'##+\s*(?:正确答案汇总|测试总结|自我评估|完成时间)', content, flags=re.IGNORECASE)[0]
    # 匹配所有格式的题目标题（与 parse_quiz 一致）
    questions = re.findall(
        r'###\s*(?:\[类型:\w+\])?\s*(?:题目|Question|问题)\s*\d+[:：]?\s*',
        content_only,
        re.IGNORECASE
    )
    return len(questions)


def parse_quiz(quiz_path):
    """解析测试题文件，提取题目、选项、答案和解析

    支持的题型：
    - choice: 选择题（A/B/C/D选项）
    - open: 开放性问题（文本答案）
    """
    full_path = BASE_DIR / quiz_path
    content = full_path.read_text(encoding='utf-8')

    questions = []

    # 先移除总结部分和答案汇总部分
    content_only = re.split(r'##+\s*(?:正确答案汇总|测试总结|自我评估|完成时间)', content, flags=re.IGNORECASE)[0]

    # 提取题目块（支持 ### 题目、### 问题、### Question，带题型标记）
    # 格式：### [类型:choice] 题目1：xxx
    # 使用 findall 找到所有题目位置，然后提取题目内容
    question_pattern = r'###\s*(?:\[类型:(\w+)\])?\s*(?:题目|Question|问题)\s*\d+[:：]?\s*'

    # 找到所有匹配的题目标记及其位置
    matches = list(re.finditer(question_pattern, content_only, re.IGNORECASE))

    # 提取每个题目标记之后的内容块（直到下一个题目或文件结束）
    question_blocks = []
    for i, match in enumerate(matches):
        start = match.end()
        # 下一个题目的开始位置，或文件末尾
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content_only)
        block = content_only[start:end]
        question_blocks.append(block)

    for idx, block in enumerate(question_blocks, 1):

        lines = block.strip().split('\n')

        # 检测题型（从第一行的类型标记或自动推断）
        question_type = None
        question_text = None
        options = {}
        correct_answer = None
        explanation = None

        # 检查是否有类型标记
        if lines and lines[0].strip():
            first_line = lines[0].strip()
            type_match = re.match(r'^\[类型:(\w+)\]', first_line)
            if type_match:
                question_type = type_match.group(1)
                lines = lines[1:]  # 跳过类型标记行
            elif first_line.startswith('[类型:'):
                # 类型标记单独一行
                question_type = re.search(r'(\w+)', first_line).group(1)
                lines = lines[1:]

        # 查找题目文本（第一行非空、非选项、非答案标记的行）
        for line in lines:
            line_stripped = line.strip()
            # 跳过类型标记、答案行、你的答案行等
            if (line_stripped and
                not line_stripped.startswith('[') and
                not any(x in line_stripped for x in ['**正确答案', '**你的答案', '正确答案', '你的答案', '**解析', '解析：'])):
                # 移除 markdown 加粗标记
                question_text = line_stripped.replace('**', '').strip()
                break

        if not question_text:
            continue

        # 如果没有显式指定题型，自动推断
        if not question_type:
            # 扫描是否有选项（A. B. C. D. 开头）
            has_options = False
            for line in lines:
                if re.match(r'^[A-D]\.\s*(?!.*___)', line.strip()):
                    has_options = True
                    break
            question_type = 'choice' if has_options else 'open'

        # 解析选项（仅选择题）
        if question_type == 'choice':
            for line in lines:
                line_stripped = line.strip()
                # 匹配选项：A. 文本（排除"你的答案：___A"格式）
                match = re.match(r'^([A-D])\.\s*(.+)', line_stripped)
                if match:
                    letter = match.group(1)
                    text = match.group(2)
                    # 跳过"你的答案：___A"这种格式
                    if not text.startswith('___') and not text.startswith('**你的答案'):
                        options[letter] = text

        # 解析正确答案和解析
        answer_section = []
        in_answer_section = False
        for line in lines:
            line_stripped = line.strip()

            # 检测进入答案解析区
            if any(x in line_stripped for x in ['**正确答案', '正确答案：', '正确答案:']):
                in_answer_section = True
                answer_section.append(line_stripped)
                continue

            if in_answer_section:
                # 收集答案解析内容，直到下一个题目或结束
                if line_stripped.startswith('**你的掌握情况') or line_stripped.startswith('你的掌握情况'):
                    break
                answer_section.append(line_stripped)

        # 从答案区提取正确答案
        answer_text = ' '.join(answer_section)
        if question_type == 'choice':
            # 提取字母答案
            answer_match = re.search(r'[A-D]', answer_text)
            if answer_match:
                correct_answer = answer_match.group(0)

        # 构建解析文本
        if answer_section:
            # 移除标记，保留纯文本
            explanation_lines = []
            for al in answer_section:
                # 移除各种标记
                clean_line = al.replace('**正确答案**', '').replace('**解析**', '')
                clean_line = re.sub(r'^\*\*正确答案\*\*[:：]\s*', '', clean_line)
                clean_line = clean_line.replace('👆', '').strip()
                if clean_line and len(clean_line) > 1:  # 过滤单字符
                    explanation_lines.append(clean_line)

            if explanation_lines:
                explanation = '\n'.join(explanation_lines[:5])  # 限制长度

        # 添加题目
        questions.append({
            'id': f'q{idx}',
            'number': idx,
            'type': question_type,
            'text': question_text,
            'options': options if question_type == 'choice' else {},
            'correct_answer': correct_answer,
            'explanation': explanation or ''
        })

    # 构建返回数据
    answers = {}
    explanations = {}

    for q in questions:
        if q['correct_answer']:
            answers[q['id']] = q['correct_answer']
        if q['explanation']:
            explanations[q['id']] = q['explanation']

    return {
        'title': extract_quiz_title(full_path),
        'questions': questions,
        'answers': answers,
        'explanations': explanations
    }


def load_answers():
    """加载已保存的答案"""
    if ANSWERS_FILE.exists():
        return json.loads(ANSWERS_FILE.read_text(encoding='utf-8'))
    return {'last_updated': None, 'quizzes': {}}


def save_answers(answers):
    """保存答案到文件"""
    ANSWERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    ANSWERS_FILE.write_text(
        json.dumps(answers, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )


def render_markdown(md_content):
    """将 Markdown 转换为 HTML（带代码高亮）"""
    # 转换 Markdown
    html = markdown.markdown(md_content, extensions=['fenced_code', 'tables'])

    # 代码高亮处理（简单版本）
    # 更复杂的处理在前端 JS 中完成

    return html


# ==================== 路由 ====================

@app.route('/')
def index():
    """首页"""
    nav = build_navigation()
    return render_template('home.html', nav=nav)


@app.route('/lecture/<path:filepath>')
def lecture(filepath):
    """讲义页面"""
    full_path = BASE_DIR / filepath

    if not full_path.exists():
        return "文件不存在", 404

    content = full_path.read_text(encoding='utf-8')
    title = extract_title(full_path)
    html_content = render_markdown(content)

    nav = build_navigation()

    return render_template('lecture.html',
                          title=title,
                          content=html_content,
                          nav=nav,
                          current_file=filepath)


@app.route('/quizzes')
def quiz_list():
    """测试题列表"""
    nav = build_navigation()
    return render_template('quiz_list.html', nav=nav)


@app.route('/quiz/<path:filepath>')
def quiz(filepath):
    """测试题页面（默认一题一页模式）"""
    full_path = BASE_DIR / filepath

    if not full_path.exists():
        return "文件不存在", 404

    quiz_data = parse_quiz(filepath)

    # 加载已保存的答案
    answers_data = load_answers()
    saved_answers = answers_data.get('quizzes', {}).get(filepath, {}).get('answers', {})

    nav = build_navigation()

    return render_template('quiz_single.html',
                          quiz_file=filepath,
                          quiz=quiz_data,
                          saved_answers=saved_answers,
                          nav=nav)


@app.route('/quiz/<path:filepath>/all')
def quiz_all(filepath):
    """测试题页面（全部显示模式）"""
    full_path = BASE_DIR / filepath

    if not full_path.exists():
        return "文件不存在", 404

    quiz_data = parse_quiz(filepath)

    # 加载已保存的答案
    answers_data = load_answers()
    saved_answers = answers_data.get('quizzes', {}).get(filepath, {}).get('answers', {})

    nav = build_navigation()

    return render_template('quiz_all.html',
                          quiz_file=filepath,
                          quiz=quiz_data,
                          saved_answers=saved_answers,
                          nav=nav)


# ==================== API ====================

@app.route('/api/navigation')
def api_navigation():
    """获取导航数据（动态）"""
    return jsonify(build_navigation())


@app.route('/api/answers/<path:filepath>')
def api_get_answers(filepath):
    """获取某套测试题的已保存答案"""
    answers_data = load_answers()
    saved = answers_data.get('quizzes', {}).get(filepath, {}).get('answers', {})
    return jsonify(saved)


@app.route('/api/save', methods=['POST'])
def api_save():
    """实时保存单个答案"""
    data = request.json
    quiz_file = data.get('quiz_file')
    question_id = data.get('question_id')
    answer = data.get('answer')

    if not all([quiz_file, question_id, answer]):
        return jsonify({'error': '缺少必要参数'}), 400

    # 加载现有答案
    answers_data = load_answers()

    # 更新答案
    if quiz_file not in answers_data['quizzes']:
        answers_data['quizzes'][quiz_file] = {'answers': {}}

    answers_data['quizzes'][quiz_file]['answers'][question_id] = answer
    answers_data['last_updated'] = datetime.now().isoformat()

    # 保存
    save_answers(answers_data)

    return jsonify({'status': 'ok', 'saved_at': answers_data['last_updated']})


@app.route('/api/submit', methods=['POST'])
def api_submit():
    """提交答案，返回结果"""
    data = request.json
    quiz_file = data.get('quiz_file')
    user_answers = data.get('answers', {})

    if not quiz_file:
        return jsonify({'error': '缺少测试题文件'}), 400

    # 解析测试题
    quiz_data = parse_quiz(quiz_file)

    # 对比答案
    results = []
    correct_count = 0

    for q in quiz_data['questions']:
        q_id = q['id']
        user_answer = user_answers.get(q_id)
        correct_answer = quiz_data['answers'].get(q_id)

        # 选择题才判断对错
        is_correct = False
        if q.get('type') == 'choice' and correct_answer:
            is_correct = (user_answer == correct_answer)
            if is_correct:
                correct_count += 1

        results.append({
            'id': q_id,
            'number': q['number'],
            'type': q.get('type', 'choice'),
            'text': q['text'],
            'options': q.get('options', {}),
            'user_answer': user_answer,
            'correct_answer': correct_answer,
            'is_correct': is_correct,
            'explanation': q.get('explanation', '')
        })

    total = len(results)
    score = {
        'correct': correct_count,
        'total': total,
        'percentage': round(correct_count / total * 100, 1) if total > 0 else 0
    }

    return jsonify({
        'results': results,
        'score': score
    })


# ==================== 静态文件 ====================

@app.route('/static/<path:filename>')
def serve_static(filename):
    """提供静态文件"""
    return send_from_directory('static', filename)


# ==================== 主程序 ====================

if __name__ == '__main__':
    print("=" * 60)
    print(" LangGraph 学习平台")
    print(" 访问地址: http://localhost:5000")
    print(" 按 Ctrl+C 停止服务")
    print("=" * 60)

    app.run(debug=True, host='0.0.0.0', port=5000)
