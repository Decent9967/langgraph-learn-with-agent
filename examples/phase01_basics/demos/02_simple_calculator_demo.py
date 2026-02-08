#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简单计算器演示
展示如何定义工具和使用 ToolNode

创建时间：2025-02-08
作者：LangGraph 学习项目
阶段：第一阶段 - 基础概念
类型：演示代码

依赖：
    - Python >= 3.10
    - langgraph >= 1.0.0

运行方式：
    python examples/phase01_basics/demos/02_simple_calculator_demo.py

学习要点：
    - 使用 @tool 装饰器定义工具
    - 理解工具的 name、description 和 args 属性
    - 定义带有 Annotated 的状态
    - 创建和使用 ToolNode
"""

import sys
import os

if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from typing_extensions import TypedDict, Annotated
from langchain.tools import tool
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode


def main():
    # ============ 步骤1：定义工具 ============
    @tool
    def multiply(a: int, b: int) -> int:
        """乘法：计算两个数的乘积"""
        return a * b

    # 看看工具长什么样
    print("=== 工具信息 ===")
    print(f"工具名称: {multiply.name}")
    print(f"工具描述: {multiply.description}")
    print(f"工具参数: {multiply.args}")

    # ============ 步骤2：定义状态 ============
    class CalculatorState(TypedDict):
        messages: Annotated[list, lambda x, y: x + y]  # 消息会累加

    # ============ 步骤3：定义工具节点 ============
    # ToolNode 是 LangGraph 内置的，专门执行工具调用
    tool_node = ToolNode([multiply])

    print("\n=== 工具节点创建成功 ===")
    print(f"工具节点包含 {len(tool_node.tools)} 个工具")


if __name__ == "__main__":
    main()
