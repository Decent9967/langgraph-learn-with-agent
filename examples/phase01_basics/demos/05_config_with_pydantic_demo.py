#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pydantic 配置管理演示
使用 Pydantic 读取 YAML 配置文件

创建时间：2025-02-08
作者：LangGraph 学习项目
阶段：第一阶段 - 基础概念
类型：演示代码

依赖：
    - Python >= 3.10
    - pydantic >= 2.0
    - pyyaml

运行方式：
    python examples/phase01_basics/demos/05_config_with_pydantic_demo.py

学习要点：
    - 使用 Pydantic 定义配置模型
    - 从 YAML 文件读取配置
    - 自动验证配置格式和类型
    - IDE 代码提示和类型检查
"""

import sys
import os

if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import yaml
from pydantic import BaseModel
from typing import Optional


# ========================================
# 步骤1：定义 Pydantic 模型（配置结构）
# ========================================

class LLMModelConfig(BaseModel):
    """单个 LLM 的配置"""
    model: str
    api_key: str
    base_url: Optional[str] = None
    temperature: float = 0


class LLMConfig(BaseModel):
    """LLM 配置"""
    provider: str
    models: dict[str, LLMModelConfig]


# ========================================
# 步骤2：读取 YAML 并转换成 Pydantic 模型
# ========================================

def load_config(config_path: str = "config.yaml") -> LLMConfig:
    """读取配置文件"""
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # YAML 文件里是 llm: {...}，所以需要取 data["llm"]
    llm_data = data["llm"]

    # 转换成 Pydantic 模型（会自动验证）
    config = LLMConfig(**llm_data)
    return config


# ========================================
# 步骤3：使用配置
# ========================================

def main():
    print("=" * 60)
    print("测试 Pydantic 配置管理")
    print("=" * 60)

    try:
        # 读取配置
        config = load_config()

        print(f"\n✅ 配置文件读取成功！")
        print(f"当前提供商: {config.provider}")

        # 获取当前提供商的配置
        current_provider_config = config.models[config.provider]
        print(f"模型名称: {current_provider_config.model}")
        print(f"API Key: {current_provider_config.api_key[:20]}...")  # 只显示前20个字符
        if current_provider_config.base_url:
            print(f"Base URL: {current_provider_config.base_url}")

        print("\n" + "=" * 60)
        print("Pydantic 的好处：")
        print("-" * 60)
        print("1. ✅ 自动验证配置格式")
        print("2. ✅ IDE 有代码提示")
        print("3. ✅ 类型检查")
        print("4. ✅ 配置结构清晰")

    except Exception as e:
        print(f"\n❌ 错误：{e}")
        print("提示：请检查 config.yaml 文件是否存在且格式正确")


if __name__ == "__main__":
    main()
