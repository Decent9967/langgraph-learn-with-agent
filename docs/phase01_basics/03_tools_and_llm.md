# 第一阶段：工具和 LLM 讲义

> 学习时间：2025-02-08
> 状态：✅ 已掌握

---

## 1. 定义工具

### @tool 装饰器

```python
from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """乘法：计算两个数的乘积"""
    return a * b

@tool
def add(a: int, b: int) -> int:
    """加法：计算两个数的和"""
    return a + b

# 工具列表
tools = [multiply, add, divide]
```

### 工具的结构

```python
@tool
def function_name(param1: type1, param2: type2) -> return_type:
    """函数文档字符串（LLM 会看到这个）"""
    # 函数实现
    return result
```

**关键点**：
- 函数名：工具的名称
- 类型注解：告诉 LLM 参数类型
- 文档字符串：描述工具用途（重要！）
- 返回值：工具执行结果

---

## 2. LLM 配置

### OpenAI（官方）

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key="sk-...",
    temperature=0
)
```

### Anthropic

```python
from langchain_anthropic import ChatAnthropic

llm = ChatAnthropic(
    model="claude-3-5-sonnet-20241022",
    api_key="sk-ant-...",
    temperature=0
)
```

### Google

```python
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    api_key="...",
    temperature=0
)
```

### 第三方提供商（如智谱）

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="glm-4-flash",
    api_key="your-zhipu-api-key",
    base_url="https://open.bigmodel.cn/api/paas/v4/",  # ← 关键！
    temperature=0
)
```

**关键点**：
- 使用 `ChatOpenAI`（兼容 OpenAI API）
- 设置 `base_url` 为第三方 API 地址
- 其他参数相同

---

## 3. bind_tools() - 绑定工具

### 基础用法

```python
# 创建 LLM
llm = ChatOpenAI(...)

# 绑定工具
llm_with_tools = llm.bind_tools(tools)

# 使用
response = llm_with_tools.invoke(messages)
```

### bind_tools() 的作用

告诉 LLM 有哪些工具可用：

```python
# 没有 bind_tools
llm.invoke("3乘以5")  # LLM 只能文字回答

# 有 bind_tools
llm_with_tools.invoke("3乘以5")  # LLM 可能返回 tool_calls
```

### 工作原理

```
LLM + bind_tools(tools)
    ↓
LLM 知道工具列表：
  - multiply(a, b)
  - add(a, b)
  - divide(a, b)
    ↓
用户输入："3乘以5"
    ↓
LLM 返回：
AIMessage(
    content="",
    tool_calls=[{
        "name": "multiply",
        "args": {"a": 3, "b": 5},
        "id": "call_001"
    }]
)
```

---

## 4. LLM 节点实现

### 完整的 LLM 节点

```python
def llm_node(state):
    """
    LLM 节点：调用 LLM 做决策
    """
    # 1. 获取消息列表
    messages = state["messages"]

    # 2. 调用 LLM（带工具）
    response = llm_with_tools.invoke(messages)

    # 3. 返回更新的消息列表
    return {"messages": [response]}
```

### 简化版本

```python
def llm_node(state):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}
```

---

## 5. ToolNode 使用

### 创建 ToolNode

```python
from langgraph.prebuilt import ToolNode

tool_node = ToolNode(tools)
```

### ToolNode 自动做什么？

```python
# 输入：State 包含 AIMessage（有 tool_calls）
state = {
    "messages": [
        AIMessage(
            content="",
            tool_calls=[{
                "name": "multiply",
                "args": {"a": 3, "b": 5},
                "id": "call_001"
            }]
        )
    ]
}

# ToolNode 执行后返回：
result = {
    "messages": [
        ToolMessage(
            content=15,
            tool_call_id="call_001"
        )
    ]
}
```

---

## 6. 完整的工具调用流程

### 流程图

```
1. 用户输入
   HumanMessage("3乘以5")
       ↓
2. LLM 节点
   llm_with_tools.invoke(messages)
       ↓
3. LLM 决定调用工具
   AIMessage(
       tool_calls=[{"name": "multiply", "args": {"a": 3, "b": 5}, "id": "call_001"}]
   )
       ↓
4. 条件判断
   should_continue() 检测到 tool_calls
       ↓
5. ToolNode 执行
   multiply(3, 5) → 15
       ↓
6. 返回工具结果
   ToolMessage(content=15, tool_call_id="call_001")
       ↓
7. 回到 LLM 节点
   LLM 看到工具结果，生成最终回复
       ↓
8. LLM 回答
   AIMessage(content="3乘以5等于15")
       ↓
9. 条件判断
   should_continue() 没有检测到 tool_calls
       ↓
10. END
```

### 代码实现

```python
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from langchain.tools import tool
from langchain_openai import ChatOpenAI

# 1. 定义工具
@tool
def multiply(a: int, b: int) -> int:
    return a * b

tools = [multiply]

# 2. 定义状态
class CalculatorState(MessagesState):
    pass

# 3. 创建 LLM 并绑定工具
llm = ChatOpenAI(model="glm-4-flash", ...)
llm_with_tools = llm.bind_tools(tools)

# 4. 定义节点
def llm_node(state):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

tool_node = ToolNode(tools)

# 5. 定义条件函数
def should_continue(state):
    last_msg = state["messages"][-1]
    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
        return "tools"
    return END

# 6. 构建图
graph = StateGraph(CalculatorState)
graph.add_node("llm", llm_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", should_continue)
graph.add_edge("tools", "llm")

# 7. 编译并运行
app = graph.compile()
result = app.invoke({"messages": [HumanMessage("3乘以5")]})
```

---

## 7. 配置管理（YAML + Pydantic）

### 配置文件结构

```yaml
llm:
  provider: zhipu

  models:
    zhipu:
      model: glm-4-flash
      api_key: your-api-key
      base_url: https://open.bigmodel.cn/api/paas/v4/
      temperature: 0

    openai:
      model: gpt-4o-mini
      api_key: your-openai-key
      temperature: 0
```

### Pydantic 模型

```python
from pydantic import BaseModel
from typing import Optional
import yaml

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
```

### 使用配置

```python
# 加载配置
llm_config = load_config()

# 获取当前提供商的配置
llm_model = llm_config.models[llm_config.provider]

# 创建 LLM
llm = ChatOpenAI(
    model=llm_model.model,
    api_key=llm_model.api_key,
    base_url=llm_model.base_url,
    temperature=llm_model.temperature
)

# 绑定工具
llm_with_tools = llm.bind_tools(tools)
```

---

## 8. 关键概念总结

### 工具调用三要素

1. **定义工具** (`@tool`)
2. **绑定工具** (`bind_tools()`)
3. **执行工具** (`ToolNode`)

### LLM 在工具调用中的角色

```
LLM = 决策者
- 判断是否需要调用工具
- 选择哪个工具
- 提取工具参数

ToolNode = 执行者
- 执行工具
- 返回结果
```

---

## 9. 常见问题

### Q1: LLM 不调用工具？

**检查**：
- 工具的文档字符串是否清晰？
- 工具的参数类型注解是否正确？
- 用户输入是否明确需要工具？

### Q2: ToolNode 报错？

**检查**：
- 工具列表是否正确？
- `tool_call_id` 是否匹配？

### Q3: 如何切换 LLM 提供商？

**方法**：修改 YAML 配置文件
```yaml
llm:
  provider: openai  # 从 zhipu 改为 openai
```

---

## 10. 练习检查清单

- [ ] 能使用 `@tool` 定义工具
- [ ] 能配置不同的 LLM 提供商
- [ ] 能使用 `bind_tools()` 绑定工具
- [ ] 能实现 LLM 节点
- [ ] 能使用 ToolNode
- [ ] 能实现条件函数（should_continue）
- [ ] 能构建完整的工具调用 Agent
- [ ] 能使用 YAML + Pydantic 管理配置

---

**下一步**：学习 [04_configuration.md](./04_configuration.md) 📖
