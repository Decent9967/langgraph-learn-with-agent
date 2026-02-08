#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
从配置创建 LLM 演示
根据 YAML 配置动态创建不同的 LLM 实例

创建时间：2025-02-08
作者：LangGraph 学习项目
阶段：第一阶段 - 基础概念
类型：演示代码

依赖：
    - Python >= 3.10
    - pydantic >= 2.0
    - pyyaml
    - langchain-openai

运行方式：
    python examples/phase01_basics/demos/06_create_llm_from_config_demo.py

学习要点：
    - 从 YAML 配置文件读取 LLM 配置
    - 根据配置动态创建 LLM 实例
    - 使用 Pydantic 进行配置验证
    - 支持多个 LLM 提供商的配置切换
"""

import sys
import os

if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import yaml
from pydantic import BaseModel
from typing import Optional
from langchain_openai import ChatOpenAI


# ========================================
# 配置模型（简化版，直接放这里）
# ========================================

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
    config = LLMConfig(**llm_data)
    return config


# ========================================
# 从配置创建 LLM
# ========================================

def get_llm_from_config(config_path: str = "config.yaml"):
    """
    从配置文件创建 LLM

    Returns:
        配置好的 LLM 实例
    """
    # 1. 读取配置
    config = load_config(config_path)

    # 2. 获取当前提供商的配置
    provider_name = config.provider
    model_config = config.models[provider_name]

    print(f"正在初始化 {provider_name} LLM...")
    print(f"  模型: {model_config.model}")

    # 3. 创建 LLM
    if provider_name in ["zhipu", "openai"]:
        # 使用 ChatOpenAI（支持 OpenAI 兼容 API）
        llm = ChatOpenAI(
            model=model_config.model,
            api_key=model_config.api_key,
            base_url=model_config.base_url,
            temperature=model_config.temperature
        )
    else:
        raise ValueError(f"暂不支持的提供商: {provider_name}")

    print(f"✅ {provider_name} LLM 初始化成功！")
    return llm


# ========================================
# 测试
# ========================================

def main():
    print("=" * 60)
    print("测试：从配置创建 LLM")
    print("=" * 60)

    try:
        # 创建 LLM
        llm = get_llm_from_config()

        # 测试调用
        print("\n测试调用 LLM...")
        response = llm.invoke("你好！")
        print(f"LLM 回复: {response.content[:100]}...")

    except Exception as e:
        print(f"\n错误：{e}")
        print("\n提示：")
        print("1. 请检查 config.yaml 是否存在")
        print("2. 请检查是否填入了正确的 API key")


if __name__ == "__main__":
    main()
