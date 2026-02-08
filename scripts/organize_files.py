#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
代码文件批量整理脚本

功能：
1. 为所有 Python 文件添加标准头部注释
2. 清理冗余代码（如多余的 pass 语句）
3. 统一代码格式
"""

import os
import re
from pathlib import Path

# 标准头部注释模板
HEADER_TEMPLATE = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
{title}
{'=' * len(title)}

{description}

创建时间：2025-02-XX
作者：LangGraph 学习项目
阶段：第一阶段 - 基础概念
类型：{file_type}

依赖：
    - Python >= 3.10
    - langgraph >= 1.0.0
    - langchain >= 0.3.0
{extra_deps}

运行方式：
    python {filename}

预期输出：
    {output_desc}

学习要点：
    {learning_points}

相关文档：
    {related_docs}
"""

# 文件元数据
FILE_METADATA = {
    "01_environment_check.py": {
        "title": "环境检查脚本",
        "description": "验证 LangGraph 和依赖包是否正确安装",
        "file_type": "演示代码",
        "extra_deps": "",
        "output_desc": "- Python 版本信息\\n- 已安装包的版本列表\\n- 类型注解支持检查\\n- LangGraph 核心组件导入测试",
        "learning_points": "- 了解 LangGraph 的依赖结构\\n- 验证开发环境配置",
        "related_docs": "docs/phase01_basics/01_core_concepts.md"
    },
    "02_simple_calculator_demo.py": {
        "title": "简单计算器（无 LLM）",
        "description": "演示基本的工具定义和 ToolNode 使用",
        "file_type": "演示代码",
        "extra_deps": "",
        "output_desc": "- 工具调用演示\\n- 计算结果输出",
        "learning_points": "- 理解 @tool 装饰器\\n- 理解 ToolNode 的作用",
        "related_docs": "docs/phase01_basics/03_tools_and_llm.md"
    },
    "03_llm_configuration_demo.py": {
        "title": "LLM 配置演示",
        "description": "展示如何配置不同的 LLM 提供商",
        "file_type": "演示代码",
        "extra_deps": "- langchain-openai\\n- langchain-anthropic\\n- langchain-google",
        "output_desc": "- 不同 LLM 的配置示例\\n- 模型调用演示",
        "learning_points": "- 配置 OpenAI、Anthropic、Google、智谱\\n- 理解 base_url 和 api_key 的作用",
        "related_docs": "docs/phase01_basics/03_tools_and_llm.md"
    },
    "04_real_calculator_agent_demo.py": {
        "title": "真实计算器 Agent",
        "description": "使用真实 LLM 的计算器 Agent",
        "file_type": "演示代码",
        "extra_deps": "- langchain-openai",
        "output_desc": "- 用户输入\\n- LLM 工具调用\\n- 计算结果",
        "learning_points": "- 理解完整的工具调用流程\\n- LLM 与 ToolNode 的协作",
        "related_docs": "docs/phase01_basics/05_complete_example.md"
    },
    "05_config_with_pydantic_demo.py": {
        "title": "Pydantic 配置管理",
        "description": "使用 Pydantic 管理配置",
        "file_type": "演示代码",
        "extra_deps": "- pydantic",
        "output_desc": "- 配置模型定义\\n - 配置加载演示",
        "learning_points": "- 理解 Pydantic BaseModel\\n- 理解数据验证",
        "related_docs": "docs/phase01_basics/03_tools_and_llm.md"
    },
    "06_create_llm_from_config_demo.py": {
        "title": "从配置创建 LLM",
        "description": "从 YAML 配置文件创建 LLM 实例",
        "file_type": "演示代码",
        "extra_deps": "- pydantic\\n- yaml",
        "output_desc": "- LLM 实例创建\\n- 配置信息输出",
        "learning_points": "- 理解 YAML 配置\\n- 理解 **data 解包",
        "related_docs": "docs/phase01_basics/03_tools_and_llm.md"
    },
    "01_first_graph_exercise.py": {
        "title": "创建第一个图（练习）",
        "description": "练习创建基本的 LangGraph 图",
        "file_type": "练习代码",
        "extra_deps": "",
        "output_desc": "- 节点执行顺序\\n- 状态传递过程",
        "learning_points": "- 掌握 StateGraph 使用\\n- 掌握 add_node 和 add_edge\\n- 理解状态传递",
        "related_docs": "docs/phase01_basics/02_api_usage.md"
    },
    "02_conditional_edges_exercise.py": {
        "title": "条件边练习",
        "description": "练习使用条件边实现动态路由",
        "file_type": "练习代码",
        "extra_deps": "",
        "output_desc": "- 条件路由演示\\n- 不同条件下的执行路径",
        "learning_points": "- 掌握 add_conditional_edges\\n- 理解条件函数的返回值",
        "related_docs": "docs/phase01_basics/02_api_usage.md"
    },
    "03_calculator_agent_exercise.py": {
        "title": "计算器 Agent（练习）",
        "description": "独立完成一个计算器 Agent",
        "file_type": "练习代码",
        "extra_deps": "- langchain-openai",
        "output_desc": "- 用户交互\\n- 工具调用\\n- 结果返回",
        "learning_points": "- 综合运用 State、Nodes、Edges\\n- 实现完整的工具调用流程",
        "related_docs": "docs/phase01_basics/05_complete_example.md"
    },
}


def clean_code(content: str) -> str:
    """清理代码：移除冗余的 pass 语句"""
    # 移除 return 或 break 后的 pass 语句
    lines = content.split('\n')
    cleaned_lines = []

    for i, line in enumerate(lines):
        cleaned_lines.append(line)

        # 如果当前行是 return、break 等，下一行是 pass（可能带缩进），跳过
        if line.strip().startswith(('return', 'break', 'continue', 'yield')):
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line == 'pass':
                    # 跳过添加下一行的 pass
                    continue

        # 如果当前行只是 pass，且前面已经有 return/break，跳过
        if line.strip() == 'pass' and i > 0:
            prev_line = lines[i - 1].strip()
            if prev_line.startswith(('return', 'break', 'continue', 'yield')):
                continue

    return '\n'.join(cleaned_lines)


def add_header(content: str, filename: str) -> str:
    """添加标准头部注释"""
    # 获取文件元数据
    metadata = FILE_METADATA.get(filename, {})

    if not metadata:
        # 如果没有元数据，使用默认模板
        header = f'''#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
{filename}
{'=' * len(filename)}

LangGraph 学习项目 - 第一阶段

创建时间：2025-02-XX
作者：LangGraph 学习项目

运行方式：
    python {filename}

相关文档：
    docs/phase01_basics/
"""
'''
    else:
        # 使用模板生成头部
        header = HEADER_TEMPLATE.format(
            title=metadata["title"],
            description=metadata["description"],
            file_type=metadata["file_type"],
            extra_deps=metadata["extra_deps"],
            filename=filename,
            output_desc=metadata["output_desc"],
            learning_points=metadata["learning_points"],
            related_docs=metadata["related_docs"]
        )

    # 移除原有的头部注释（如果存在）
    lines = content.split('\n')

    # 找到第一个代码行（非注释、非空行）
    first_code_line = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith('#') and not stripped.startswith('"""') and not stripped.startswith("'''"):
            first_code_line = i
            break

    # 保留原有的 docstring（如果有）
    import_start = -1
    import_end = -1
    for i, line in enumerate(lines):
        if '"""' in line or "'''" in line:
            if import_start == -1:
                import_start = i
            elif import_end == -1:
                import_end = i
                break

    # 组装新文件内容
    if import_start >= 0 and import_end > 0:
        # 保留原有 docstring
        old_docstring = '\n'.join(lines[import_start:import_end+1])
        new_content = header + '\n' + old_docstring + '\n' + '\n'.join(lines[import_end+1:])
    else:
        # 直接添加新头部
        new_content = header + '\n' + content

    return new_content


def process_file(filepath: Path):
    """处理单个文件"""
    print(f"处理文件: {filepath.name}")

    # 读取文件
    content = filepath.read_text(encoding='utf-8')

    # 添加头部注释
    content = add_header(content, filepath.name)

    # 清理代码
    content = clean_code(content)

    # 写回文件
    filepath.write_text(content, encoding='utf-8')

    print(f"  ✅ 完成")


def main():
    """主函数"""
    # 处理 demos 目录
    demos_dir = Path("examples/phase01_basics/demos")
    print("\n" + "="*50)
    print("处理 demos/ 目录")
    print("="*50)

    for py_file in sorted(demos_dir.glob("*.py")):
        process_file(py_file)

    # 处理 exercises 目录
    exercises_dir = Path("examples/phase01_basics/exercises")
    print("\n" + "="*50)
    print("处理 exercises/ 目录")
    print("="*50)

    for py_file in sorted(exercises_dir.glob("*.py")):
        process_file(py_file)

    print("\n" + "="*50)
    print("✅ 所有文件处理完成！")
    print("="*50)


if __name__ == "__main__":
    main()
