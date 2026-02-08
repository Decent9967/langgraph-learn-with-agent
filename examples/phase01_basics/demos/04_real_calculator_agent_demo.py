#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
真实计算器 Agent 演示
使用真实 LLM 构建可以进行数学计算的 Agent

创建时间：2025-02-08
作者：LangGraph 学习项目
阶段：第一阶段 - 基础概念
类型：演示代码

依赖：
    - Python >= 3.10
    - langgraph >= 1.0.0
    - langchain-openai
    - langchain-anthropic
    - langchain-google-genai
    - python-dotenv

运行方式：
    python examples/phase01_basics/demos/04_real_calculator_agent_demo.py --provider zhipu
    python examples/phase01_basics/demos/04_real_calculator_agent_demo.py --provider openai

学习要点：
    - 定义多个工具并绑定到 LLM
    - 使用 MessagesState 作为状态
    - 实现条件边判断是否需要调用工具
    - 构建完整的 Agent 循环（LLM -> 工具 -> LLM）
    - 支持多个 LLM 提供商的配置
"""

import sys
import os

if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()

from typing_extensions import TypedDict, Annotated
from typing import Literal
import operator

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage


# ========================================
# 步骤1：定义工具
# ========================================

@tool
def multiply(a: int, b: int) -> int:
    """乘法：计算两个整数的乘积，用于数学运算"""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """加法：计算两个整数的和，用于数学运算"""
    return a + b

@tool
def divide(a: float, b: float) -> float:
    """除法：计算两个数的商，注意除数不能为0"""
    if b == 0:
        return "错误：除数不能为0"
    return a / b

tools = [multiply, add, divide]


# ========================================
# 步骤2：配置 LLM
# ========================================

def get_llm(provider="zhipu"):
    """
    获取配置好的 LLM

    Args:
        provider: 提供商名称，可选值：
            - "openai": OpenAI GPT
            - "anthropic": Anthropic Claude
            - "google": Google Gemini
            - "zhipu": 智谱 GLM (默认)
    """
    if provider == "openai":
        return ChatOpenAI(
            model="gpt-4.1-mini",
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    elif provider == "anthropic":
        return ChatAnthropic(
            model="claude-sonnet-4-5-20250929",
            temperature=0,
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    elif provider == "google":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            temperature=0,
            api_key=os.getenv("GOOGLE_API_KEY")
        )
    elif provider == "zhipu":
        # 智谱使用 OpenAI 兼容模式
        return ChatOpenAI(
            model="glm-4-flash",  # 或 glm-4-plus, glm-4-air
            temperature=0,
            api_key=os.getenv("ZHIPU_API_KEY"),
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )
    else:
        raise ValueError(f"不支持的提供商: {provider}")


# ========================================
# 步骤3：定义状态
# ========================================

class CalculatorState(MessagesState):
    pass


# ========================================
# 步骤4：定义节点
# ========================================

def create_llm_node(llm):
    """创建 LLM 节点函数"""
    def llm_node(state: CalculatorState):
        messages = state["messages"]
        # 调用 LLM
        response = llm.invoke(messages)
        return {"messages": [response]}
    return llm_node


# ========================================
# 步骤5：定义条件函数
# ========================================

def should_continue(state: CalculatorState) -> Literal["tools", END]:
    """判断是否继续调用工具"""
    messages = state["messages"]
    last_message = messages[-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END


# ========================================
# 步骤6：构建图
# ========================================

def create_calculator_agent(provider="zhipu"):
    """创建计算器 Agent"""

    # 获取配置好的 LLM
    llm = get_llm(provider)

    # 把工具绑定到 LLM
    llm_with_tools = llm.bind_tools(tools)

    # 创建 LLM 节点
    llm_node = create_llm_node(llm_with_tools)

    # 创建工具节点
    tool_node = ToolNode(tools)

    # 构建图
    graph = StateGraph(CalculatorState)

    # 添加节点
    graph.add_node("llm", llm_node)
    graph.add_node("tools", tool_node)

    # 添加边
    graph.add_edge(START, "llm")
    graph.add_conditional_edges("llm", should_continue, ["tools", END])
    graph.add_edge("tools", "llm")

    # 编译
    return graph.compile()


# ========================================
# 步骤7：测试
# ========================================

def test_calculator(provider="zhipu"):
    """测试计算器 Agent"""

    print(f"\n{'='*60}")
    print(f"使用 {provider} 创建计算器 Agent")
    print(f"{'='*60}\n")

    # 创建 Agent
    agent = create_calculator_agent(provider)

    # 测试用例
    test_cases = [
        "3 乘以 5 等于多少？",
        "10 加上 20 等于多少？",
        "100 除以 4 等于多少？",
    ]

    for question in test_cases:
        print(f"\n问题：{question}")
        print("-" * 40)

        try:
            # 调用 Agent
            result = agent.invoke({"messages": [HumanMessage(question)]})

            # 打印最终回答
            final_message = result["messages"][-1]
            print(f"回答：{final_message.content}")

        except Exception as e:
            print(f"❌ 错误：{e}")
            print(f"提示：请检查 .env 文件中的 {provider.upper()}_API_KEY")

        print()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="测试计算器 Agent")
    parser.add_argument(
        "--provider",
        type=str,
        default="zhipu",
        choices=["openai", "anthropic", "google", "zhipu"],
        help="选择 LLM 提供商"
    )
    args = parser.parse_args()

    test_calculator(args.provider)

    print("\n提示：")
    print("1. 复制 .env.example 为 .env")
    print("2. 填入对应提供商的 API key")
    print("3. 运行：python examples/phase01_basics/demos/04_real_calculator_agent_demo.py --provider zhipu")


if __name__ == "__main__":
    main()
