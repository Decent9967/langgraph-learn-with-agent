#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
练习：第一个 LangGraph 程序
创建一个简单的两节点图，理解状态如何在节点间传递

创建时间：2025-02-08
作者：LangGraph 学习项目
阶段：第一阶段 - 基础概念
类型：练习代码

依赖：
    - Python >= 3.10
    - langgraph >= 1.0.0

运行方式：
    python examples/phase01_basics/exercises/01_first_graph_exercise.py

学习要点：
    - 定义 TypedDict 状态
    - 创建节点函数处理状态
    - 使用 StateGraph 构建图
    - 添加节点和边
    - 编译并运行图
"""

import sys
import os

if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


# ============ 步骤1：定义状态 ============
# 状态就像一个传送带上的包裹，每个节点都能看到和修改它
class MyState(TypedDict):
    message: str   # 存储消息
    count: int     # 存储计数


# ============ 步骤2：定义节点 ============
# 节点就是工厂里的工人，每个工人做一件事

def node_a(state: MyState) -> dict:
    """节点A：读取消息，设置计数为1"""
    print(f"节点A收到: {state['message']}")
    # TODO: 返回更新后的状态，把 count 设置为 1
    return {"message": state["message"], "count": 1}


def node_b(state: MyState) -> dict:
    """节点B：读取计数，修改消息"""
    print(f"节点B收到，count是: {state['count']}")
    # TODO: 返回更新后的状态，把 message 改为"完成"
    return {"message": "完成", "count": state["count"]}


# ============ 步骤3：构建图 ============
# 图就是整个工厂的流程图

# 创建图的画布
graph = StateGraph(MyState)

# 添加节点
# TODO: 添加 node_a 和 node_b
graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)

# 连接节点
# TODO: 连接 START -> node_a -> node_b -> END
graph.add_edge(START, "node_a")
graph.add_edge("node_a", "node_b")
graph.add_edge("node_b", END)

# ============ 步骤4：编译并运行 ============

def main():
    # 编译图（准备运行）
    app = graph.compile()

    # 运行！传入初始状态
    print("\n=== 开始运行 ===")
    result = app.invoke({"message": "开始", "count": 0})

    print("\n=== 最终结果 ===")
    print(result)


if __name__ == "__main__":
    main()
