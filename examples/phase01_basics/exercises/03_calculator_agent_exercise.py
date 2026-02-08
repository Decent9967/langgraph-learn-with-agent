#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
练习：计算器 Agent
理解 LLM 如何调用工具，构建一个完整的计算器 Agent

创建时间：2025-02-08
作者：LangGraph 学习项目
阶段：第一阶段 - 基础概念
类型：练习代码

依赖：
    - Python >= 3.10
    - langgraph >= 1.0.0
    - langchain-openai
    - pydantic
    - pyyaml

运行方式：
    python examples/phase01_basics/exercises/03_calculator_agent_exercise.py

学习要点：
    - 定义多个工具（乘法、加法、除法）
    - 使用 MessagesState 作为状态
    - 创建 LLM 节点并绑定工具
    - 使用 ToolNode 执行工具调用
    - 实现条件边判断是否需要调用工具
    - 构建完整的 Agent 循环
"""

import sys
import os

if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from typing_extensions import TypedDict, Annotated
from typing import Literal, Optional
import operator

from langchain.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from pydantic import BaseModel
import yaml


# ============ 步骤1：定义工具 ============
@tool
def multiply(a: int, b: int) -> int:
    """乘法：计算两个数的乘积"""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """加法：计算两个数的和"""
    return a + b

@tool
def divide(a: int, b: int) -> float:
    """除法：计算两个数的商"""
    return a / b

tools = [multiply, add, divide]


# ============ 步骤2：定义状态 ============
# TODO: 定义一个继承自 MessagesState 的状态类
# 提示：直接用 class CalculatorState(MessagesState): pass
#
class CalculatorState(MessagesState):
    pass


# ============ 步骤3：定义工具节点 ============
# ToolNode 会自动处理工具调用
tool_node = ToolNode(tools)


# ============ 步骤4：定义 LLM 节点 ============
# TODO: 创建一个真实的 LLM（使用智谱 API）
# 提示：
# 1. 用 ChatOpenAI 创建 LLM
# 2. base_url = "https://open.bigmodel.cn/api/paas/v4/"
# 3. model = "glm-4-flash"
# 4. api_key 从 config.yaml 读取，或者先写死测试
# 5. 用 bind_tools(tools) 绑定工具
class LLMModelConfig(BaseModel):
    model: str
    api_key: str
    base_url: Optional[str] = None
    temperature: float = 0


class LLMConfig(BaseModel):
    provider: str
    models: dict[str, LLMModelConfig]


def load_config(config_path: str = "config.yaml") -> LLMConfig:
    """读取配置文件"""
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    llm_data = data["llm"]
    return LLMConfig(**llm_data)


llm_config = load_config()
llm_model = llm_config.models[llm_config.provider]
llm = ChatOpenAI(
    model=llm_model.model,
    api_key=llm_model.api_key,
    base_url=llm_model.base_url,
    temperature=llm_model.temperature
)
llm_with_tools = llm.bind_tools(tools)


def llm_node(state):
    """
    LLM 节点：调用 LLM 做决策
    """
    # TODO: 在这里调用 LLM
    # 提示：
    # 1. 从 state 取出 messages
    # 2. 调用 llm_with_tools.invoke(messages)
    # 3. 返回 {"messages": [response]}
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


# ============ 步骤5：定义条件函数 ============
def should_continue(state) -> Literal["tools", END]:
    """
    判断是否继续调用工具
    检查最后一条消息是否有 tool_calls
    """
    # TODO: 检查最后一条消息是否有 tool_calls
    # 提示：
    # 1. 从 state 取出 messages
    # 2. 获取最后一条消息
    # 3. 检查是否有 tool_calls 属性且不为空
    # 4. 如果有，返回 "tools"；如果没有，返回 END
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    else:
        return END


# ============ 步骤6：构建图 ============
def main():
    # TODO: 创建 StateGraph 并添加节点
    #
    graph = StateGraph(CalculatorState)
    graph.add_node("llm", llm_node)
    graph.add_node("tools", tool_node)

    # TODO: 添加边
    # 提示：
    # 1. START -> llm
    # 2. llm -> 条件边（根据 should_continue 返回值决定）
    # 3. tools -> llm（工具执行完回到 LLM）
    #
    graph.add_edge(START, "llm")
    graph.add_conditional_edges("llm", should_continue)
    graph.add_edge("tools", "llm")

    # ============ 步骤7：编译并测试 ============
    # TODO: 编译图
    #
    app = graph.compile()

    print("\n=== 测试：3 乘以 5 ===")
    # TODO: 调用 app.invoke() 测试
    #
    try:
        result = app.invoke({"messages": [HumanMessage("3 乘以 5")]})

        print("\n最终消息列表：")
        for i, msg in enumerate(result["messages"]):
            msg_type = type(msg).__name__
            print(f"{i+1}. {msg_type}: {msg.content}")
            if hasattr(msg, "tool_calls"):
                print(f"   工具调用: {msg.tool_calls}")
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
