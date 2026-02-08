#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
练习：条件边
根据数字大小走不同的路，掌握条件边的使用

创建时间：2025-02-08
作者：LangGraph 学习项目
阶段：第一阶段 - 基础概念
类型：练习代码

依赖：
    - Python >= 3.10
    - langgraph >= 1.0.0

运行方式：
    python examples/phase01_basics/exercises/02_conditional_edges_exercise.py

学习要点：
    - 定义条件函数决定路由
    - 使用 add_conditional_edges 添加条件边
    - 根据状态值动态选择不同的节点
    - 理解条件边的返回值和节点映射关系
"""

import sys
import os

if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# ============ 步骤1：定义状态 ============
class NumberState(TypedDict):
    number: int  # 存储一个数字
    result: str  # 处理结果


# ============ 步骤2：定义节点 ============

def small_handler(state: NumberState) -> dict:
    """处理小数字（< 10）"""
    print(f"✅ 小数字处理器收到: {state['number']}")
    return {"result": "这个数字很小"}


def large_handler(state: NumberState) -> dict:
    """处理大数字（>= 10）"""
    print(f"✅ 大数字处理器收到: {state['number']}")
    return {"result": "这个数字很大"}


# ============ 步骤3：定义条件函数 ============
def route_by_size(state: NumberState) -> str:
    """
    TODO: 根据数字大小决定路由
    如果 number < 10，返回 "small"
    如果 number >= 10，返回 "large"
    """
    # 你的代码写在这里
    if state['number'] < 10:
        return "small"
    else:
        return "large"


# ============ 步骤4：构建图 ============
def main():
    graph = StateGraph(NumberState)

    # TODO: 添加两个处理节点
    # 节点名: "small" 对应 small_handler
    # 节点名: "large" 对应 large_handler
    graph.add_node("small", small_handler)
    graph.add_node("large", large_handler)

    # TODO: 添加条件边
    # 从 START 出发，使用 route_by_size 函数判断
    # 可能的去向: ["small", "large"]
    graph.add_conditional_edges(START, route_by_size, ["small", "large"])

    # TODO: 连接两个处理节点到 END
    # graph.add_edge("small", END)
    # graph.add_edge("large", END)
    graph.add_edge("small", END)
    graph.add_edge("large", END)

    # ============ 步骤5：编译并测试 ============
    app = graph.compile()

    print("\n=== 测试1：输入小数字 5 ===")
    result1 = app.invoke({"number": 5})
    print(f"结果: {result1}\n")

    print("=== 测试2：输入大数字 15 ===")
    result2 = app.invoke({"number": 15})
    print(f"结果: {result2}\n")


if __name__ == "__main__":
    main()
