#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
LLM 配置演示
学习如何配置不同的 LLM 提供商（OpenAI、Anthropic、Google、智谱等）

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
    python examples/phase01_basics/demos/03_llm_configuration_demo.py

学习要点：
    - 配置 OpenAI GPT 模型
    - 配置 Anthropic Claude 模型
    - 配置 Google Gemini 模型
    - 配置第三方兼容 OpenAI API 的模型（如智谱 GLM）
    - 使用环境变量和 .env 文件管理 API keys
    - 使用 init_chat_model 通用配置方法
"""

import sys
import os

if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()


def main():
    print("=" * 60)
    print("LLM 配置学习")
    print("=" * 60)

    # ========================================
    # 1. OpenAI 配置
    # ========================================
    print("\n【方式1：OpenAI 标准配置】")
    print("-" * 40)

    from langchain_openai import ChatOpenAI

    # 方式 A：使用环境变量 OPENAI_API_KEY
    # export OPENAI_API_KEY="sk-..."
    openai_env = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0
    )
    print("✅ OpenAI 环境变量方式")

    # 方式 B：直接传入 API key
    openai_direct = ChatOpenAI(
        model="gpt-4.1-mini",
        api_key="sk-...",  # 你的 API key
        temperature=0
    )
    print("✅ OpenAI 直接传入 API key")

    # 方式 C：使用自定义 base_url（适用于第三方兼容 OpenAI API）
    # 例如：智谱 AI、DeepSeek、Together AI 等
    openai_custom = ChatOpenAI(
        model="gpt-4.1-mini",  # 或第三方模型的名称
        api_key="your-api-key",
        base_url="https://api.example.com/v1",  # 第三方 API 地址
        temperature=0
    )
    print("✅ OpenAI 兼容第三方 API（使用 base_url）")

    # ========================================
    # 2. Anthropic 配置
    # ========================================
    print("\n【方式2：Anthropic (Claude) 配置】")
    print("-" * 40)

    from langchain_anthropic import ChatAnthropic

    # 方式 A：使用环境变量 ANTHROPIC_API_KEY
    # export ANTHROPIC_API_KEY="sk-ant-..."
    anthropic_env = ChatAnthropic(
        model="claude-sonnet-4-5-20250929",
        temperature=0
    )
    print("✅ Anthropic 环境变量方式")

    # 方式 B：直接传入 API key
    anthropic_direct = ChatAnthropic(
        model="claude-sonnet-4-5-20250929",
        api_key="sk-ant-...",  # 你的 API key
        temperature=0
    )
    print("✅ Anthropic 直接传入 API key")

    # ========================================
    # 3. Google 配置
    # ========================================
    print("\n【方式3：Google Gemini 配置】")
    print("-" * 40)

    from langchain_google_genai import ChatGoogleGenerativeAI

    # 方式 A：使用环境变量 GOOGLE_API_KEY
    # export GOOGLE_API_KEY="..."
    google_env = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0
    )
    print("✅ Google 环境变量方式")

    # 方式 B：直接传入 API key
    google_direct = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        api_key="...",  # 你的 API key
        temperature=0
    )
    print("✅ Google 直接传入 API key")

    # ========================================
    # 4. 智谱 AI (GLM) 配置 - 第三方兼容 OpenAI API
    # ========================================
    print("\n【方式4：智谱 AI (GLM) 配置】")
    print("-" * 40)

    # 智谱 AI 提供 OpenAI 兼容的 API
    # API 文档：https://open.bigmodel.cn/dev/api

    glm_model = ChatOpenAI(
        model="glm-4-plus",  # 或 glm-4-flash, glm-4-air 等
        api_key="your-zhipu-api-key",  # 智谱的 API key
        base_url="https://open.bigmodel.cn/api/paas/v4/",  # 智谱的 API 地址
        temperature=0
    )
    print("✅ 智谱 GLM 配置（使用 OpenAI 兼容模式）")

    # ========================================
    # 5. 通用配置方法：init_chat_model
    # ========================================
    print("\n【方式5：通用配置方法】")
    print("-" * 40)

    from langchain.chat_models import init_chat_model

    # 使用 init_chat_model 可以方便地切换不同的提供商
    model = init_chat_model(
        model="gpt-4.1-mini",
        model_provider="openai",  # 或 "anthropic", "google" 等
        api_key="your-api-key",    # 可选，不填则从环境变量读取
        # base_url="...",          # 可选，用于第三方 API
    )
    print("✅ 使用 init_chat_model 通用配置")

    # ========================================
    # 6. 最佳实践：使用 .env 文件
    # ========================================
    print("\n【最佳实践：使用 .env 文件管理 API keys】")
    print("-" * 40)

    print("""
在项目根目录创建 .env 文件：

# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Google
GOOGLE_API_KEY=...

# 智谱 AI (需要自定义，因为不是标准环境变量)
ZHIPU_API_KEY=...

然后在代码中：
    from dotenv import load_dotenv
    load_dotenv()

    # 自动从环境变量读取
    openai = ChatOpenAI(model="gpt-4.1-mini")
    anthropic = ChatAnthropic(model="claude-sonnet-4-5-20250929")

    # 智谱需要手动配置
    glm = ChatOpenAI(
        model="glm-4-plus",
        api_key=os.getenv("ZHIPU_API_KEY"),
        base_url="https://open.bigmodel.cn/api/paas/v4/"
    )
""")

    # ========================================
    # 7. 实际测试
    # ========================================
    print("\n" + "=" * 60)
    print("配置总结")
    print("=" * 60)

    print("""
【主流提供商配置对比】

提供商     | 类名                    | API Key 环境变量      | 特殊参数
----------|------------------------|---------------------|----------
OpenAI    | ChatOpenAI             | OPENAI_API_KEY      | base_url (第三方)
Anthropic | ChatAnthropic          | ANTHROPIC_API_KEY   | -
Google    | ChatGoogleGenerativeAI | GOOGLE_API_KEY      | -
智谱 GLM  | ChatOpenAI (兼容)       | 自定义               | base_url 必需

【第三方模型配置方法】
如果模型提供商提供 OpenAI 兼容 API：
    1. 使用 ChatOpenAI
    2. 设置 base_url 为提供商的 API 地址
    3. 设置 api_key 为提供商的密钥
    4. model 设置为提供商的模型名称

示例：
    ChatOpenAI(
        model="custom-model",
        api_key="provider-key",
        base_url="https://provider-api.com/v1"
    )
""")

    print("\n下一步：在你的计算器 Agent 中使用真实的 LLM！")


if __name__ == "__main__":
    main()
