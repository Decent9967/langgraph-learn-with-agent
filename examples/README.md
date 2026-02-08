# LangGraph 学习进度

**开始日期**: 2025-02-08
**当前阶段**: 第一阶段 - 基础概念

---

## 📁 目录结构

```
examples/
├── phase01_basics/           # 第一阶段：基础概念
│   ├── exercises/            # 练习题（需要你填空）
│   │   ├── 02_first_graph.py
│   │   ├── 03_conditional_edges.py
│   │   └── 05_calculator_agent.py  ✅ 已完成
│   ├── demos/                 # 演示代码（直接运行看效果）
│   │   ├── 01_environment_check.py
│   │   ├── 04_simple_calculator.py
│   │   ├── 06_llm_configuration.py
│   │   ├── 07_real_calculator_agent.py
│   │   ├── 08_config_with_pydantic.py
│   │   └── 09_create_llm_from_config.py
│   └── quizzes/               # 测试题（复习用）
│       ├── 01_basics_quiz.md
│       └── 02_api_usage_quiz.md
│
├── phase02_core/             # 第二阶段：核心功能（待开始）
│
└── phase03_advanced/         # 第三阶段：进阶模式（待开始）
```

---

## 📊 第一阶段：基础概念（进行中）

### ✅ 已完成

| 文件 | 类型 | 内容 | 状态 |
|------|------|------|------|
| `01_environment_check.py` | demo | 环境检查 | ✅ 已运行 |
| `02_first_graph.py` | exercise | 第一个 LangGraph 图 | ✅ 已完成 |
| `03_conditional_edges.py` | exercise | 条件边练习 | ✅ 已完成 |
| `04_simple_calculator.py` | demo | 简单计算器演示 | ✅ 已讲解 |

### ⏳ 进行中/待完成

| 文件 | 类型 | 内容 | 状态 |
|------|------|------|------|
| `05_calculator_agent.py` | exercise | 计算器 Agent（填空） | ⏸️ 待完成 |
| `06_llm_configuration.py` | demo | LLM 配置教程 | ✅ 已讲解 |
| `07_real_calculator_agent.py` | demo | 真实计算器 Agent | ✅ 已讲解 |
| `08_config_with_pydantic.py` | demo | Pydantic 配置管理 | ✅ 已讲解 |
| `09_create_llm_from_config.py` | demo | 从配置创建 LLM | ✅ 已讲解 |

---

## 🎯 学习目标

### 第一阶段：基础概念（进行中）

- [x] 1. 环境搭建与安装
- [x] 2. 核心概念理解
  - [x] State（状态）
  - [x] Nodes（节点）
  - [x] Edges（边）
  - [x] Conditional Edges（条件边）
- [ ] 3. 第一个 Agent：计算器
  - [ ] 05_calculator_agent.py 填空练习
  - [ ] 运行真实的计算器 Agent

### 第二阶段：核心功能（未开始）

- [ ] 4. 状态管理与类型安全
- [ ] 5. 持久化与检查点
- [ ] 6. 流式输出
- [ ] 7. 人机协作（Human-in-the-loop）

### 第三阶段：进阶模式（未开始）

- [ ] 8. RAG Agent
- [ ] 9. 多 Agent 系统
- [ ] 10. 并行执行与复杂流程控制

---

## 📝 文件类型说明

- **demo（演示）**：完整的代码，直接运行学习概念
- **exercise（练习）**：有 TODO 的填空题，需要你动手完成

---

## 🔄 最后更新

**更新时间**: 2025-02-08
**下一步**: 完成 05_calculator_agent.py 练习
