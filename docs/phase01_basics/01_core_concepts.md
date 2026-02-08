# 第一阶段：核心概念讲义

> 学习时间：2025-02-08
> 状态：✅ 已掌握

---

## 1. State（状态）

### 什么是 State？

**类比**：传送带上的包裹 📦

- State 就像传送带上的包裹
- 包裹里装着信息（消息列表）
- 包裹在各个工人（节点）之间传递

### MessagesState

LangGraph 提供的预定义状态类：

```python
from langgraph.graph import MessagesState

class MessagesState(TypedDict):
    messages: list[AnyMessage]  # 已定义好！
```

**包含的字段**：
- `messages`: 消息列表
  - `HumanMessage`（用户消息）
  - `AIMessage`（AI回复，可能包含 tool_calls）
  - `ToolMessage`（工具执行结果）

### 如何定义自己的状态？

```python
from langgraph.graph import MessagesState

class CalculatorState(MessagesState):
    pass  # 直接继承，使用默认的 messages 字段

# 如果需要额外字段
class CalculatorState(MessagesState):
    calculation_count: int  # 添加计数器
```

---

## 2. Nodes（节点）

### 什么是 Node？

**类比**：工厂里的工人 👷

- 接收包裹（State）
- 做一些工作
- 把处理后的包裹放回传送带

### Node 的结构

```python
def my_node(state: MyState):
    """节点函数：接收状态，返回更新"""
    # 1. 从 state 取数据
    messages = state["messages"]

    # 2. 做一些处理
    # ...

    # 3. 返回需要更新的字段
    return {"messages": [new_message]}
```

**关键点**：
- ✅ 只返回需要更新的字段（不是整个 State）
- ✅ 返回值是字典
- ✅ 字典的键必须和 State 的字段匹配

---

## 3. Edges（边）

### 什么是 Edge？

**类比**：传送带的路径 🛤️

- 决定包裹下一步去哪里
- 分为两种：普通边和条件边

### 普通边（Fixed Edge）

固定路线，无条件：

```python
graph.add_edge("node_a", "node_b")  # 从 A 到 B，固定路线
```

### 条件边（Conditional Edge）

根据状态动态选择：

```python
def route_function(state):
    # 根据状态返回不同的节点名
    if some_condition:
        return "node_x"
    else:
        return "node_y"

graph.add_conditional_edges("node_a", route_function)
```

---

## 4. 消息类型

### HumanMessage（用户消息）

```python
from langchain_core.messages import HumanMessage

msg = HumanMessage(content="3 乘以 5 等于多少？")
```

### AIMessage（AI回复）

```python
from langchain_core.messages import AIMessage

# 普通回复
msg = AIMessage(content="答案是 15")

# 带工具调用
msg = AIMessage(
    content="",
    tool_calls=[{
        "name": "multiply",
        "args": {"a": 3, "b": 5},
        "id": "call_001"
    }]
)
```

**关键字段**：
- `content`: 文本内容
- `tool_calls`: 要调用的工具列表（可选）

### ToolMessage（工具结果）

```python
from langchain_core.messages import ToolMessage

msg = ToolMessage(
    content=15,
    tool_call_id="call_001"  # 必须匹配 AIMessage 的 id
)
```

**关键字段**：
- `content`: 工具执行结果
- `tool_call_id`: 匹配 tool_call 的唯一标识

---

## 5. tool_calls 和 tool_call_id

### tool_calls

LLM 决定调用工具时，在 AIMessage 中包含：

```python
tool_calls=[{
    "name": "multiply",           # 工具名称
    "args": {"a": 3, "b": 5},     # 工具参数
    "id": "call_001"              # 唯一标识
}]
```

### tool_call_id

**作用**：匹配工具调用和结果

```python
# AIMessage 创建 tool_call，id="call_001"
AIMessage(tool_calls=[{"id": "call_001", ...}])

# ToolMessage 返回结果，tool_call_id="call_001"
ToolMessage(content=15, tool_call_id="call_001")
```

**为什么需要？**
- 一次可能调用多个工具
- 需要知道哪个结果对应哪个调用

---

## 6. ToolNode

### 什么是 ToolNode？

LangGraph 提供的预定义节点，自动执行工具：

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode(tools)
```

### ToolNode 自动做什么？

1. 接收 State
2. 检查最后一条消息的 `tool_calls`
3. 调用对应的工具
4. 将结果包装成 `ToolMessage`
5. 返回更新的 State

### ToolNode 需要什么边？

**两种边都需要**：

```python
# 1. 普通边：工具执行完回到 LLM
graph.add_edge("tools", "llm")

# 2. 条件边：LLM 决定是否调用工具
graph.add_conditional_edges("llm", should_continue)
```

---

## 7. 完整流程图

```
用户输入 "3乘以5"
    ↓
HumanMessage(content="3乘以5")
    ↓
LLM 节点
    ↓
AIMessage(
    content="",
    tool_calls=[{"name": "multiply", "args": {"a": 3, "b": 5}, "id": "call_001"}]
)
    ↓
should_continue 检测到 tool_calls
    ↓
去 ToolNode
    ↓
执行 multiply(3, 5) → 15
    ↓
ToolMessage(content=15, tool_call_id="call_001")
    ↓
回到 LLM 节点
    ↓
AIMessage(content="3乘以5等于15")
    ↓
should_continue 检测不到 tool_calls
    ↓
END
```

---

## 8. 类型注解基础

### 常见类型

```python
# 基础类型
x: int           # 整数
x: str           # 字符串
x: bool          # 布尔
x: float         # 浮点数

# 容器类型
x: list[int]     # 整数列表
x: dict[str, int]  # 键是字符串，值是整数
x: tuple[str, int]  # 元组：(字符串, 整数)

# 联合类型（Python 3.10+）
x: str | int     # 字符串 或 整数
x: str | None    # 字符串 或 None（等价于 Optional[str]）

# 旧写法（Python 3.9）
from typing import Union, Optional
x: Union[str, int]      # 等价于 str | int
x: Optional[str]        # 等价于 str | None
```

### 函数类型注解

```python
def process(state: MyState) -> dict[str, Any]:
    # 接收 MyState，返回字典
    pass
```

---

## 9. 检查对象属性

### hasattr() 方法

检查对象是否有某个属性：

```python
if hasattr(obj, "tool_calls") and obj.tool_calls:
    # obj 有 tool_calls 属性，且不为空
    pass
```

**为什么需要？**
- 不是所有消息类型都有 `tool_calls` 字段
- `hasattr()` 安全地检查属性是否存在

---

## 10. 练习检查清单

完成学习后，应该能回答：

- [ ] State 的作用是什么？
- [ ] MessagesState 包含哪些字段？
- [ ] Nodes 和 Edges 的区别是什么？
- [ ] 条件边什么时候用？
- [ ] `tool_calls` 和 `tool_call_id` 的作用？
- [ ] ToolNode 自动做什么？
- [ ] 如何检查对象是否有某个属性？

---

**下一步**：学习 [02_api_usage.md](./02_api_usage.md) 📖
