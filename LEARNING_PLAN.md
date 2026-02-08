# LangGraph 学习计划

> 本学习计划基于 [LangGraph 官方文档](https://docs.langchain.com/oss/python/langgraph) 制定

## 项目概述

**LangGraph** 是一个低级编排框架，用于构建有状态、长期运行的 Agent 应用。

- **当前版本**: LangGraph v1
- **编程语言**: Python 3.10+
- **核心原则**: "nodes do the work, edges tell what to do next"

---

## 核心概念

### 三大核心组件

| 组件 | 描述 | 代码示例 |
|------|------|----------|
| **State（状态）** | 共享数据结构，表示应用的当前快照 | `class MessagesState(TypedDict): ...` |
| **Nodes（节点）** | 函数，编码 Agent 的逻辑 | `def my_node(state: State) -> State: ...` |
| **Edges（边）** | 决定下一个执行哪个节点 | `graph.add_conditional_edges(...)` |

### 执行模型

LangGraph 基于**消息传递**算法（灵感来自 Google Pregel）：
- 执行分为离散的 "super-steps"
- 支持并行节点执行
- 当所有节点不活跃且无消息传输时终止

---

## 学习路径

### 第一阶段：基础概念（1-2周）

#### 1. 环境搭建
```bash
pip install -U langgraph langchain
```

#### 2. 核心概念理解
- [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph)
- [Graph API overview](https://docs.langchain.com/oss/python/langgraph/graph-api)

#### 3. 第一个 Agent：计算器
[Quickstart 教程](https://docs.langchain.com/oss/python/langgraph/quickstart)

```python
from langgraph.graph import StateGraph, START, END
from langchain.tools import tool

# 1. 定义工具
@tool
def multiply(a: int, b: int) -> int:
    """Multiply a and b"""
    return a * b

# 2. 定义状态
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

# 3. 构建图
agent = StateGraph(MessagesState)
agent.add_node("llm_call", llm_call)
agent.add_node("tool_node", tool_node)
agent.add_edge(START, "llm_call")
agent.add_conditional_edges("llm_call", should_continue)
agent = agent.compile()
```

**练习**:
- [ ] 复现计算器 Agent
- [ ] 添加新的数学运算工具
- [ ] 可视化图结构

---

### 第二阶段：核心功能（2-3周）

#### 4. 状态管理
- TypedDict 和类型提示
- Annotated 和 Reducer
- 自定义 reducer 函数

#### 5. 持久化与检查点
[Persistence 文档](https://docs.langchain.com/oss/python/langgraph/persistence)

```python
from langgraph.checkpoint.memory import MemorySaver

checkpointer = MemorySaver()
agent = agent_builder.compile(checkpointer=checkpointer)

# 使用 thread_id 保存和恢复状态
config = {"configurable": {"thread_id": "thread-1"}}
result = agent.invoke({"messages": [...]}, config)
```

**练习**:
- [ ] 实现带对话历史的 Agent
- [ ] 测试 thread 隔离
- [ ] 实现时间回溯

#### 6. 流式输出
- Token 级别的流式输出
- 事件流监控

#### 7. 人机协作
[Human-in-the-loop 文档](https://docs.langchain.com/oss/python/langgraph/human-in-the-loop)

```python
agent = agent_builder.compile(
    checkpointer=MemorySaver(),
    interrupt_before=["tool_node"]  # 在 tool_node 前暂停
)
```

**练习**:
- [ ] 实现工具调用审批流程
- [ ] 实现 approve / reject 工作流

---

### 第三阶段：进阶模式（3-4周）

#### 8. RAG Agent
[Agentic RAG 教程](https://docs.langchain.com/oss/python/langgraph/agentic-rag)

**项目实践**:
- [ ] 文档索引和向量存储
- [ ] 创建 retriever 工具
- [ ] 构建决策逻辑

#### 9. 多 Agent 系统
[Multi-agent patterns](https://docs.langchain.com/oss/python/learn)

| 模式 | 描述 | 使用场景 |
|------|------|----------|
| **Subagents** | 主 Agent 协调子 Agent | 专业分工任务 |
| **Handoffs** | 基于状态切换行为 | 客服场景 |
| **Router** | 路由到专门 Agent | 知识库查询 |
| **Skills** | 按需加载知识 | 上下文加载 |

**练习**:
- [ ] 实现 Router 模式
- [ ] 实现 Handoffs 模式
- [ ] 实现 Subagents 模式

#### 10. 并行执行
- Fan-out/fan-in 机制
- 并行节点执行
- Command 对象

---

### 第四阶段：生产实践（2-3周）

#### 11. 测试与调试
[Testing 文档](https://docs.langchain.com/oss/python/langgraph/test)

```python
# 测试单个节点
result = compiled_graph.nodes["node1"].invoke({"my_key": "initial"})
assert result["my_key"] == "expected_value"
```

#### 12. CLI 和部署
[LangGraph CLI](https://docs.langchain.com/langsmith/cli)

- LangGraph CLI 工具
- 本地 Agent Server
- API 端点

#### 13. 性能优化
- 状态设计最佳实践
- 减少 LLM 调用
- 并行化策略

---

### 第五阶段：综合项目（2-4周）

#### 项目选项

**A. 智能客服系统**
- 多 Agent 协作
- RAG 集成
- 人工审批流程

**B. 代码助手 Agent**
- 工具调用
- 多步骤推理
- 人机协作

**C. 数据分析 Agent**
- SQL 查询生成
- 数据可视化
- 报告生成

---

## 学习资源

### 官方文档
- [LangGraph Python Docs](https://docs.langchain.com/oss/python/langgraph)
- [LangChain Concepts](https://docs.langchain.com/oss/python/concepts)
- [LangSmith Deployment](https://docs.langchain.com/langsmith)

### 推荐学习顺序
1. Quickstart → Graph API → Persistence → Streaming → Human-in-the-loop
2. RAG Tutorial → Multi-agent Patterns
3. Testing → CLI & Deployment → Performance

---

## 验证标准

### 第一阶段
- [ ] 独立实现简单的工具调用 Agent
- [ ] 理解 State、Nodes、Edges 的作用

### 第二阶段
- [ ] 实现带持久化的对话 Agent
- [ ] 实现流式输出和人工审批

### 第三阶段
- [ ] 构建完整的 RAG 系统
- [ ] 实现至少两种多 Agent 模式

### 第四阶段
- [ ] 编写完整的测试套件
- [ ] 部署 Agent 到本地服务器

### 第五阶段
- [ ] 完成一个综合项目

---

## 实践建议

1. **边学边做**: 每个概念都要亲手实现
2. **可视化**: 使用 `get_graph().draw_mermaid_png()` 理解图结构
3. **追踪**: 集成 LangSmith 进行调试
4. **迭代**: 从简单开始，逐步增加复杂性
