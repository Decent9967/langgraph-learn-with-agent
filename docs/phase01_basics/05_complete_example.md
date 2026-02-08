# 第一阶段：完整示例讲义

> 学习时间：2025-02-08
> 状态：✅ 已掌握

---

## 项目：计算器 Agent

**目标**：构建一个能进行加减乘除的 AI Agent

---

## 完整代码

```python
"""
我的第一个 AI Agent - 计算器
目标：理解 LLM 如何调用工具
"""

import sys
import os
if os.name == 'nt':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from typing import Literal
from typing_extensions import TypedDict

from langchain.tools import tool
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from pydantic import BaseModel
from typing import Optional
import yaml

# ============ 步骤1：定义工具 ============
@tool
def multiply(a: int, b: int) -> int:
    """乘法：计算两个数的乘积"""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """加法：计算两个数的和"""
    return a + b

@tool
def divide(a: int, b: int) -> float:
    """除法：计算两个数的商"""
    return a / b

tools = [multiply, add, divide]

# ============ 步骤2：定义状态 ============
class CalculatorState(MessagesState):
    """计算器状态：继承 MessagesState，使用默认的 messages 字段"""
    pass

# ============ 步骤3：定义工具节点 ============
tool_node = ToolNode(tools)

# ============ 步骤4：配置 LLM ============
class LLMModelConfig(BaseModel):
    """LLM 模型配置"""
    model: str
    api_key: str
    base_url: Optional[str] = None
    temperature: float = 0

class LLMConfig(BaseModel):
    """LLM 配置"""
    provider: str
    models: dict[str, LLMModelConfig]

def load_config(config_path: str = "config.yaml") -> LLMConfig:
    """读取配置文件"""
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    llm_data = data["llm"]
    return LLMConfig(**llm_data)

# 加载配置
llm_config = load_config()
llm_model = llm_config.models[llm_config.provider]

# 创建 LLM 并绑定工具
llm = ChatOpenAI(
    model=llm_model.model,
    api_key=llm_model.api_key,
    base_url=llm_model.base_url,
    temperature=llm_model.temperature
)
llm_with_tools = llm.bind_tools(tools)

# ============ 步骤5：定义节点 ============
def llm_node(state):
    """
    LLM 节点：调用 LLM 做决策
    """
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

def should_continue(state) -> Literal["tools", END]:
    """
    条件函数：判断是否继续调用工具
    """
    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END

# ============ 步骤6：构建图 ============
graph = StateGraph(CalculatorState)

# 添加节点
graph.add_node("llm", llm_node)
graph.add_node("tools", tool_node)

# 添加边
graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", should_continue)
graph.add_edge("tools", "llm")

# ============ 步骤7：编译并测试 ============
app = graph.compile()

# 测试
print("\n=== 测试1：3 乘以 5 ===")
result = app.invoke({"messages": [HumanMessage("3 乘以 5 等于多少？")]})

print("\n最终消息列表：")
for i, msg in enumerate(result["messages"]):
    msg_type = type(msg).__name__
    print(f"{i+1}. {msg_type}: {msg.content}")
    if hasattr(msg, "tool_calls"):
        print(f"   工具调用: {msg.tool_calls}")

print("\n=== 测试2：10 除以 2 ===")
result2 = app.invoke({"messages": [HumanMessage("10 除以 2 等于多少？")]})

print("\n最终消息列表：")
for i, msg in enumerate(result2["messages"]):
    msg_type = type(msg).__name__
    print(f"{i+1}. {msg_type}: {msg.content}")
    if hasattr(msg, "tool_calls"):
        print(f"   工具调用: {msg.tool_calls}")
```

---

## 执行流程详解

### 测试1：`3 乘以 5`

#### 第1步：用户输入
```python
HumanMessage(content="3 乘以 5 等于多少？")
```

#### 第2步：LLM 节点
```python
llm_with_tools.invoke([HumanMessage(...)])
```

**LLM 的输入**：
- 工具列表：`multiply`, `add`, `divide`
- 用户消息："3 乘以 5 等于多少？"

**LLM 的输出**：
```python
AIMessage(
    content="",
    tool_calls=[{
        "name": "multiply",
        "args": {"a": 3, "b": 5},
        "id": "call_001"
    }]
)
```

#### 第3步：条件判断
```python
last_message = state["messages"][-1]
# last_message 是 AIMessage，有 tool_calls
hasattr(last_message, "tool_calls")  # True
last_message.tool_calls              # 不为空
# 返回 "tools"
```

#### 第4步：ToolNode 执行
```python
multiply(a=3, b=5)  # 返回 15
```

**ToolNode 的输出**：
```python
ToolMessage(
    content=15,
    tool_call_id="call_001"
)
```

#### 第5步：回到 LLM 节点
```python
llm_with_tools.invoke([
    HumanMessage("3 乘以 5 等于多少？"),
    AIMessage(tool_calls=[...]),
    ToolMessage(content=15, tool_call_id="call_001")
])
```

**LLM 看到工具结果**，生成最终回复：
```python
AIMessage(content="3 乘以 5 等于 15")
```

#### 第6步：条件判断
```python
last_message = state["messages"][-1]
# last_message 是 AIMessage，没有 tool_calls
hasattr(last_message, "tool_calls")  # True
last_message.tool_calls              # 空列表
# 返回 END
```

#### 第7步：结束

**最终消息列表**：
```python
[
    HumanMessage("3 乘以 5 等于多少？"),
    AIMessage(tool_calls=[...]),
    ToolMessage(content=15),
    AIMessage(content="3 乘以 5 等于 15")
]
```

---

## 配置文件

### config.yaml

```yaml
llm:
  # 默认使用的 LLM 提供商
  provider: zhipu

  # 各个提供商的配置
  models:
    zhipu:
      model: glm-4-flash
      api_key: your-zhipu-api-key
      base_url: https://open.bigmodel.cn/api/paas/v4/
      temperature: 0

    openai:
      model: gpt-4o-mini
      api_key: your-openai-api-key
      temperature: 0
```

---

## 关键知识点总结

### 1. 工具调用

```python
# 定义工具
@tool
def multiply(a: int, b: int) -> int:
    return a * b

# 绑定工具
llm_with_tools = llm.bind_tools([multiply])

# 执行工具
tool_node = ToolNode([multiply])
```

### 2. 状态管理

```python
# 定义状态
class CalculatorState(MessagesState):
    pass

# 访问状态
messages = state["messages"]

# 更新状态
return {"messages": [new_msg]}
```

### 3. 条件路由

```python
# 条件函数
def should_continue(state):
    if has_tool_calls:
        return "tools"
    return END

# 添加条件边
graph.add_conditional_edges("llm", should_continue)
```

### 4. 配置管理

```python
# Pydantic 模型
class LLMModelConfig(BaseModel):
    model: str
    api_key: str
    base_url: Optional[str] = None

# 读取配置
config = load_config()
llm = ChatOpenAI(**config.model_dump())
```

---

## 扩展练习

### 练习1：添加更多工具

添加一个取模运算：
```python
@tool
def modulo(a: int, b: int) -> int:
    """取模：计算 a 除以 b 的余数"""
    return a % b

tools = [multiply, add, divide, modulo]
```

### 练习2：添加状态字段

```python
class CalculatorState(MessagesState):
    calculation_count: int  # 计算次数

def llm_node(state):
    response = llm_with_tools.invoke(state["messages"])
    count = state.get("calculation_count", 0) + 1
    return {"messages": [response], "calculation_count": count}
```

### 练习3：切换 LLM 提供商

修改 `config.yaml`：
```yaml
llm:
  provider: openai  # 从 zhipu 改为 openai
```

不需要修改代码！

---

## 常见问题

### Q1: LLM 不调用工具？

**可能原因**：
1. 工具的文档字符串不清晰
2. 用户输入不明确
3. LLM 配置问题

**解决方法**：
```python
# 检查工具定义
@tool
def multiply(a: int, b: int) -> int:
    """乘法：计算两个数的乘积"""  # ← 确保描述清晰
    return a * b

# 测试 LLM 是否知道工具
print(llm_with_tools.invoke("你有哪些工具？"))
```

### Q2: ToolNode 报错？

**可能原因**：
1. 工具执行失败
2. 参数类型错误

**解决方法**：
```python
# 添加错误处理
@tool
def divide(a: int, b: int) -> float:
    """除法：计算两个数的商"""
    if b == 0:
        return "错误：除数不能为0"
    return a / b
```

### Q3: 如何调试？

**方法1：打印消息**
```python
def llm_node(state):
    print(f"LLM 节点输入: {state['messages']}")
    response = llm_with_tools.invoke(state["messages"])
    print(f"LLM 节点输出: {response}")
    return {"messages": [response]}
```

**方法2：查看消息列表**
```python
result = app.invoke({"messages": [HumanMessage("...")]})

for i, msg in enumerate(result["messages"]):
    print(f"{i+1}. {type(msg).__name__}: {msg.content}")
    if hasattr(msg, "tool_calls"):
        print(f"   工具调用: {msg.tool_calls}")
```

---

## 学习成果检查

完成这个项目后，你应该：

- [ ] 理解 LangGraph 的核心概念（State、Nodes、Edges）
- [ ] 能定义和使用工具（`@tool`、`bind_tools()`、`ToolNode`）
- [ ] 能构建完整的工具调用 Agent
- [ ] 能使用 Pydantic + YAML 管理配置
- [ ] 能阅读和理解源码
- [ ] 能调试和优化 Agent

---

**恭喜你完成第一阶段的学习！** 🎉

你已经掌握了 LangGraph 的核心概念，可以开始第二阶段的学习了！

---

**下一步**：探索更复杂的应用场景
- RAG Agent
- 多 Agent 系统
- 人机协作（Human-in-the-loop）
