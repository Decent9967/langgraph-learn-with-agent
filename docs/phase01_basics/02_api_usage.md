# 第一阶段：API 使用讲义

> 学习时间：2025-02-08
> 状态：✅ 已掌握

---

## 1. 创建图

### StateGraph()

```python
from langgraph.graph import StateGraph, MessagesState

class MyState(MessagesState):
    pass

graph = StateGraph(MyState)  # ✅ 传入状态类
```

**参数**：
- 状态类（必须是 TypedDict 或继承自 MessagesState）

---

## 2. 添加节点

### add_node()

```python
def my_node(state: MyState):
    return {"messages": [...]}

graph.add_node("node_name", my_node)  # ✅ 节点名 + 函数
```

**参数**：
- 第一个参数：节点名称（字符串）
- 第二个参数：节点函数

---

## 3. 添加边

### 普通边：add_edge()

```python
# 连接两个节点
graph.add_edge("node_a", "node_b")

# 从起点开始
from langgraph.graph import START
graph.add_edge(START, "node_a")

# 到终点结束
from langgraph.graph import END
graph.add_edge("node_z", END)
```

### 条件边：add_conditional_edges()

```python
def route_func(state):
    if condition:
        return "node_x"
    else:
        return END

# 方式1：不传第三个参数（推荐）
graph.add_conditional_edges("node_a", route_func)

# 方式2：传列表
graph.add_conditional_edges("node_a", route_func, ["node_x", "node_y"])

# 方式3：传映射字典
graph.add_conditional_edges("node_a", route_func, {
    "node_x": "actual_node_x",
    "node_y": "actual_node_y"
})
```

**参数**：
1. 源节点名称
2. 条件函数（返回节点名字符串或 END）
3. 可选：路径映射

---

## 4. 编译图

### compile()

```python
app = graph.compile()
```

**作用**：
- 构建图结构
- 验证节点和边的连接
- 返回可执行的应用

---

## 5. 运行图

### invoke()

```python
from langchain_core.messages import HumanMessage

# 基础用法
result = app.invoke({"messages": [HumanMessage("用户输入")]})

# 获取结果
messages = result["messages"]
for msg in messages:
    print(f"{type(msg).__name__}: {msg.content}")
```

**参数**：
- 第一个参数：`input`（状态字典）
- 可选参数：
  - `config`: 运行配置
  - `context`: 上下文（关键字参数，必须在 `*` 后面）

**常见错误**：
```python
# ❌ 错误：context 不是第一个参数
app.invoke(context="...")

# ✅ 正确：第一个参数是 input
app.invoke({"messages": [...]})

# ✅ 正确：用关键字传递 context
app.invoke({"messages": [...]}, context=...)
```

---

## 6. 节点函数规范

### 返回值

```python
def my_node(state):
    # ✅ 正确：只返回需要更新的字段
    return {"messages": [new_msg]}

    # ❌ 错误：返回整个 State（除非必要）
    # return state
```

**原则**：
- 只返回需要更新的字段
- LangGraph 会自动合并到 State

### 访问 State

```python
def my_node(state):
    # 访问字段
    messages = state["messages"]

    # 获取最后一条消息
    last_msg = messages[-1]

    # 检查属性
    if hasattr(last_msg, "tool_calls"):
        ...
```

---

## 7. 条件函数规范

### 返回值

```python
from typing import Literal
from langgraph.graph import END

def should_continue(state) -> Literal["tools", END]:
    # 返回节点名或 END
    if has_tool_calls:
        return "tools"  # 节点名
    else:
        return END      # 结束
```

**类型注解**：
```python
# 方式1：Literal（推荐）
def route(state) -> Literal["node_a", "node_b", END]:
    ...

# 方式2：str
def route(state) -> str:
    ...
```

---

## 8. 完整示例

```python
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage, AIMessage

# 1. 定义状态
class MyState(MessagesState):
    pass

# 2. 定义节点
def node_a(state):
    return {"messages": [AIMessage(content="来自 A")]}

def node_b(state):
    return {"messages": [AIMessage(content="来自 B")]}

def route_func(state):
    last_msg = state["messages"][-1]
    if "继续" in last_msg.content:
        return "node_b"
    return END

# 3. 构建图
graph = StateGraph(MyState)
graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)

graph.add_edge(START, "node_a")
graph.add_conditional_edges("node_a", route_func)

# 4. 编译并运行
app = graph.compile()
result = app.invoke({"messages": [HumanMessage("开始")]})
```

---

## 9. API 快速参考

| API | 用途 | 示例 |
|-----|------|------|
| `StateGraph(StateClass)` | 创建图 | `graph = StateGraph(MyState)` |
| `add_node(name, func)` | 添加节点 | `graph.add_node("llm", llm_node)` |
| `add_edge(src, dst)` | 添加普通边 | `graph.add_edge(START, "llm")` |
| `add_conditional_edges(src, path, path_map=None)` | 添加条件边 | `graph.add_conditional_edges("llm", should_continue)` |
| `compile()` | 编译图 | `app = graph.compile()` |
| `invoke(input)` | 运行图 | `app.invoke({"messages": [...]})` |

---

## 10. 常见错误

### 错误1：参数名错误

```python
# ❌ 错误
app.invoke(context="...")

# ✅ 正确
app.invoke({"messages": [...]})
```

### 错误2：返回值错误

```python
# ❌ 错误：返回 None
def my_node(state):
    pass

# ✅ 正确：返回字典
def my_node(state):
    return {"messages": [...]}
```

### 错误3：类型注解错误

```python
# ❌ 错误：END 不能在 Literal 的 Union 类型中直接使用
def route(state) -> Literal["tools", END]:  # 某些版本可能报错
    ...

# ✅ 正确：用字符串 "__end__"
def route(state) -> Literal["tools", "__end__"]:
    ...
```

---

## 11. 练习检查清单

- [ ] 能正确使用 `StateGraph()` 创建图
- [ ] 能使用 `add_node()` 添加节点
- [ ] 能使用 `add_edge()` 添加普通边
- [ ] 能使用 `add_conditional_edges()` 添加条件边
- [ ] 能使用 `compile()` 编译图
- [ ] 能使用 `invoke()` 运行图
- [ ] 理解节点函数应该返回什么
- [ ] 能编写条件函数

---

**下一步**：学习 [03_tools_and_llm.md](./03_tools_and_llm.md) 📖
