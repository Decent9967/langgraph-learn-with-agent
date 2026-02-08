#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LangGraph 学习项目 - 主入口

这是一个系统学习 LangGraph 框架的项目。

创建时间：2025-02-08
作者：LangGraph 学习项目
阶段：主程序
类型：项目入口

运行方式：
    python main.py

学习要点：
    - 了解项目结构
    - 查看可用示例和练习
"""

import os
import sys
from pathlib import Path

# Set UTF-8 encoding for Windows console
if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def print_header():
    """打印项目标题"""
    print("=" * 70)
    print(" " * 15 + "LangGraph 学习项目")
    print(" " * 10 + "从零开始学习 LangGraph 框架")
    print("=" * 70)
    print()


def print_info():
    """打印项目信息"""
    print("📖 项目简介")
    print("-" * 70)
    print("这是一个系统学习 LangGraph 框架的项目，通过：")
    print("  📚 系统化讲义 - 按阶段整理的学习文档")
    print("  💻 动手实践 - 从简单到复杂的练习代码")
    print("  ✅ 测试验证 - 多套测试题确保掌握程度")
    print()


def print_structure():
    """打印项目结构"""
    print("📁 项目结构")
    print("-" * 70)
    print("langgraph-learn/")
    print("├── docs/                   # 📚 讲义文档")
    print("│   └── phase01_basics/     # 第一阶段讲义")
    print("│")
    print("├── examples/               # 💻 示例和练习")
    print("│   ├── demos/              # 演示代码")
    print("│   ├── exercises/          # 练习代码")
    print("│   └── quizzes/            # 测试题")
    print("│")
    print("├── config.yaml             # LLM 配置文件")
    print("├── main.py                 # 项目入口（本文件）")
    print("├── LEARNING_PLAN.md        # 学习计划")
    print("├── PROGRESS.md             # 学习进度跟踪")
    print("└── README.md               # 项目说明文档")
    print()


def print_examples():
    """打印可用的示例和练习"""
    examples_dir = Path("examples/phase01_basics")

    print("🎯 第一阶段：基础概念 ✅ 已完成")
    print("-" * 70)

    # 列出演示
    demos_dir = examples_dir / "demos"
    if demos_dir.exists():
        print("📺 演示代码 (demos/):")
        for demo_file in sorted(demos_dir.glob("*.py")):
            print(f"  - {demo_file.name}")
        print()

    # 列出练习
    exercises_dir = examples_dir / "exercises"
    if exercises_dir.exists():
        print("✏️  练习代码 (exercises/):")
        for exercise_file in sorted(exercises_dir.glob("*.py")):
            print(f"  - {exercise_file.name}")
        print()

    # 列出测试
    quizzes_dir = examples_dir / "quizzes"
    if quizzes_dir.exists():
        print("📝 测试题 (quizzes/):")
        for quiz_file in sorted(quizzes_dir.glob("*.py")):
            print(f"  - {quiz_file.name}")
        print()


def print_usage():
    """打印使用说明"""
    print("🚀 使用方法")
    print("-" * 70)
    print("运行示例：")
    print("  python examples/phase01_basics/demos/01_environment_check.py")
    print()
    print("运行练习：")
    print("  python examples/phase01_basics/exercises/03_calculator_agent_exercise.py")
    print()
    print("运行测试：")
    print("  python examples/phase01_basics/quizzes/05_quiz_basics.py")
    print()
    print("查看文档：")
    print("  - 主文档: README.md")
    print("  - 学习计划: LEARNING_PLAN.md")
    print("  - 学习进度: PROGRESS.md")
    print()


def print_progress():
    """打印学习进度"""
    print("📊 学习进度")
    print("-" * 70)

    progress_file = Path("PROGRESS.md")
    if progress_file.exists():
        content = progress_file.read_text(encoding='utf-8')
        # 提取第一阶段成绩
        for line in content.split('\n'):
            if '第一阶段' in line or '96.7%' in line or '已完成' in line:
                print(f"  {line.strip()}")
    print()


def main():
    """主函数"""
    print_header()
    print_info()
    print_structure()
    print_examples()
    print_usage()
    print_progress()

    print("=" * 70)
    print("💡 提示：运行具体示例时，请确保已配置 config.yaml 中的 API key")
    print("=" * 70)


if __name__ == "__main__":
    main()
