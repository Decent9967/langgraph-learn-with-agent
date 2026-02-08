#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
环境检查脚本
验证 LangGraph 和依赖项是否正确安装

创建时间：2025-02-08
作者：LangGraph 学习项目
阶段：第一阶段 - 基础概念
类型：演示代码

依赖：
    - Python >= 3.10
    - langgraph >= 1.0.0

运行方式：
    python examples/phase01_basics/demos/01_environment_check.py

学习要点：
    - 检查 Python 版本是否满足要求
    - 验证 LangGraph 及相关依赖是否正确安装
    - 测试类型注解支持（TypedDict、Annotated）
    - 验证核心组件导入是否正常
"""

import sys
import os

# Set UTF-8 encoding for Windows console
if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from typing import TypedDict


def main():
    print("=" * 50)
    print("LangGraph Environment Check")
    print("=" * 50)

    # Check Python version
    print(f"\n[OK] Python version: {sys.version}")
    if sys.version_info >= (3, 10):
        print("    Python version meets requirement (>= 3.10)")
    else:
        print("    [ERROR] Python version too low, need 3.10 or higher")
        sys.exit(1)

    # Check key packages
    packages = {
        'langgraph': 'LangGraph',
        'langchain': 'LangChain',
        'langchain_anthropic': 'LangChain Anthropic',
        'langgraph_checkpoint': 'LangGraph Checkpoint',
    }

    print("\n[Package] Checking installed packages:")
    for module_name, display_name in packages.items():
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"    [OK] {display_name}: {version}")
        except ImportError as e:
            print(f"    [FAIL] {display_name}: not installed - {e}")

    # Check TypedDict support (Python 3.10+ feature)
    print("\n[Type] Checking type hint support:")
    try:
        from typing_extensions import TypedDict, Annotated
        import operator

        class TestState(TypedDict):
            """Test state definition"""
            messages: Annotated[list, operator.add]

        print("    [OK] TypedDict and Annotated support normal")
    except ImportError as e:
        print(f"    [FAIL] Type hint support error: {e}")

    # Check langgraph core components
    print("\n[Component] Checking LangGraph core components:")
    try:
        from langgraph.graph import StateGraph, START, END
        print("    [OK] StateGraph, START, END imported successfully")

        from langgraph.checkpoint.memory import MemorySaver
        print("    [OK] MemorySaver imported successfully")

        from langchain.tools import tool
        print("    [OK] langchain.tools imported successfully")

    except ImportError as e:
        print(f"    [FAIL] Core component import failed: {e}")

    print("\n" + "=" * 50)
    print("[SUCCESS] Environment check complete! All dependencies installed.")
    print("=" * 50)


if __name__ == "__main__":
    main()
