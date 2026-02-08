# 第一阶段：基础概念

> 学习时间：2025-02-08 开始

---

## 📚 本阶段目标

掌握 LangGraph 的核心概念：
- State（状态）
- Nodes（节点）
- Edges（边）
- Conditional Edges（条件边）
- 工具（Tools）
- 第一个 Agent

---

## 📝 练习列表

### ✅ 已完成

#### 1. 环境检查
**文件**: `demos/01_environment_check.py`
**类型**: 演示
**状态**: ✅ 已完成

运行这个检查 Python 和依赖是否安装正确。

#### 2. 第一个图
**文件**: `exercises/01_first_graph_exercise.py`
**类型**: 练习（填空）
**状态**: ✅ 已完成

学习 State、Nodes、Edges 的基础概念。

**关键学习**：
- State 就像传送带上的包裹
- Nodes 是工人，做具体工作
- Edges 决定下一步去哪

#### 3. 条件边
**文件**: `exercises/02_conditional_edges_exercise.py`
**类型**: 练习（填空）
**状态**: ✅ 已完成

学习如何根据状态做判断，走不同的路径。

**关键学习**：
- 普通边 = 固定路线
- 条件边 = 根据状态动态选择
- `add_conditional_edges()` 用法

#### 4. LLM 配置
**文件**: `demos/03_llm_configuration_demo.py`
**类型**: 演示
**状态**: ✅ 已讲解

学习如何配置 OpenAI、Anthropic、Google 和第三方模型（智谱）。

**关键学习**：
- 第三方模型用 `ChatOpenAI` + `base_url`
- API key 管理

#### 5. Pydantic 配置管理
**文件**: `demos/05_config_with_pydantic_demo.py`
**类型**: 演示
**状态**: ✅ 已讲解

学习用 Pydantic + YAML 管理配置。

**关键学习**：
- `BaseModel` = 数据模型基类（不是 AI 模型）
- `**data` = 解包字典
- `Optional[str]` = 可选字段
- `dict[str, LLMModelConfig]` = 字典类型注解

---

### ⏳ 待完成

#### 6. 计算器 Agent（重要！）✅
**文件**: `exercises/03_calculator_agent_exercise.py`
**类型**: 练习（填空）
**状态**: ✅ 已完成 (2025-02-08)

这是**第一个真正的 Agent**！

**完成内容**：
1. ✅ 定义状态（State）
2. ✅ 定义 LLM 节点
3. ✅ 定义条件函数
4. ✅ 构建图（连接边）
5. ✅ 使用 YAML + Pydantic 配置管理
6. ✅ 调用真实 LLM（智谱 GLM）

**前置知识**：
- ✅ 已经学过 State、Nodes、Edges
- ✅ 已经学过条件边
- ✅ 已经学过工具（@tool）
- ✅ 已经学过 ToolNode
- ✅ 已经学过 LLM 配置

---

## 📋 练习检查清单

完成练习后，应该能回答：

- [ ] State 的作用是什么？
- [ ] Nodes 和 Edges 的区别是什么？
- [ ] 条件边什么时候用？
- [ ] `@tool` 装饰器的作用？
- [ ] ToolNode 自动做什么？
- [ ] 如何配置第三方 LLM（如智谱）？
- [ ] Pydantic 的 BaseModel 是什么？

---

## 🎯 完成标准

**第一阶段验证标准**：
- [ ] 独立实现一个简单的工具调用 Agent
- [ ] 理解并解释 State、Nodes、Edges 的作用
- [ ] 能够根据 YAML 配置切换不同的 LLM
