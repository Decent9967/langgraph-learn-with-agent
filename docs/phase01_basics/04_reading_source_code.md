# 第一阶段：阅读源码技巧讲义

> 学习时间：2025-02-08
> 状态：✅ 已掌握

---

## 1. 查看源码的方法

### 方法1：IDE 跳转（最常用）

**VSCode / PyCharm**：

1. 光标放在函数名上
2. 按 **F12**（或 Ctrl+点击）
3. 跳转到源码定义

**示例**：
```python
graph.add_conditional_edges("llm", should_continue)
     ^^^ 光标放在这里，按 F12
```

---

### 方法2：`help()` 函数

在 Python 交互式终端：

```python
>>> from langgraph.graph import StateGraph
>>> help(StateGraph.add_conditional_edges)
```

**输出**：
```
Help on function add_conditional_edges:

add_conditional_edges(source, path, path_map=None)
    Add conditional edges from a node to any number of destination nodes.
```

---

### 方法3：`inspect` 模块

```python
import inspect
from langgraph.graph import StateGraph

# 查看函数签名
print(inspect.signature(StateGraph.add_conditional_edges))
# 输出：(source, path, path_map=None)

# 查看完整源码
print(inspect.getsource(StateGraph.add_conditional_edges))
```

---

### 方法4：IDE 悬停提示

**VSCode**：
- 鼠标悬停在函数名上
- 显示参数列表和文档字符串

---

## 2. 解读函数签名

### 基础结构

```python
def function_name(
    param1: type1,              # 位置参数
    param2: type2 = default,    # 可选参数
    *,                          # ← 关键符号
    kw_param: type3,            # 关键字参数
    **kwargs: Any               # 可变关键字参数
) -> return_type:
    """文档字符串"""
    pass
```

---

### 示例1：invoke()

```python
def invoke(
    self,
    input: InputT | Command | None,      # 第1个参数：input
    config: RunnableConfig | None = None,
    *,                                    # ← 关键！
    context: ContextT | None = None,      # ← keyword-only
    stream_mode: StreamMode = "values",
    **kwargs: Any,
) -> dict[str, Any] | Any:
```

**关键点**：

1. **第一个参数是 `input`，不是 `context`**
   ```python
   # ✅ 正确
   app.invoke({"messages": [...]})

   # ❌ 错误
   app.invoke(context="...")
   ```

2. **`*` 符号后面的参数必须用关键字**
   ```python
   # ✅ 正确
   app.invoke({"messages": [...]}, context=...)

   # ❌ 错误
   app.invoke({"messages": [...}, ...])
   ```

3. **类型注解：`InputT | Command | None`**
   - `InputT` = 输入类型（泛型）
   - `|` = 或（Python 3.10+）
   - 可以是三种类型之一

---

### 示例2：add_conditional_edges()

```python
def add_conditional_edges(
    self,
    source: str,                                          # 第1个参数
    path: Callable[..., Hashable | Sequence[Hashable]]
        | Callable[..., Awaitable[Hashable | Sequence[Hashable]]]
        | Runnable[Any, Hashable | Sequence[Hashable]],   # 第2个参数
    path_map: dict[Hashable, str] | list[str] | None = None,  # 第3个参数
) -> Self:
```

**关键点**：

1. **第三个参数的类型**：
   ```python
   path_map: dict[Hashable, str] | list[str] | None
   ```
   - 可以是字典：`{"tools": "tools"}`
   - 可以是列表：`["tools", END]`
   - 可以是 `None`（省略）

2. **第二个参数的复杂类型**：
   ```python
   path: Callable[..., Hashable | Sequence[Hashable]]
         | Runnable[Any, Hashable | Sequence[Hashable]]
   ```
   - `Callable` = 函数
   - `Runnable` = LangChain 的可运行对象
   - `Hashable | Sequence[Hashable]` = 返回单个值或列表

---

## 3. 类型注解读法

### 基础类型

```python
x: int                    # 整数
x: str                    # 字符串
x: bool                   # 布尔
x: float                  # 浮点数
x: Any                    # 任何类型
```

### 容器类型

```python
x: list[int]              # 整数列表
x: dict[str, int]         # 键是字符串，值是整数
x: tuple[str, int]        # 元组：(字符串, 整数)
x: set[str]               # 字符串集合
```

### 联合类型

```python
# 新写法（Python 3.10+）
x: str | int              # 字符串 或 整数
x: str | None             # 字符串 或 None

# 旧写法（Python 3.9）
from typing import Union, Optional
x: Union[str, int]        # 等价于 str | int
x: Optional[str]          # 等价于 str | None
```

### 泛型

```python
T = TypeVar('T')

def func(x: T) -> T:       # 泛型函数
    return x
```

**在 LangGraph 中**：
```python
class StateGraph(StateType):
    def invoke(self, input: StateType, ...):
        # StateType 是泛型，创建图时指定
        pass
```

---

## 4. 特殊符号

### `*` 符号

```python
def func(a, *, b):
    pass

func(1, b=2)   # ✅
func(1, 2)     # ❌ b 必须用关键字
```

**作用**：`*` 后面的参数必须用关键字传递

### `**kwargs` 符号

```python
def func(a, **kwargs):
    pass

func(1, b=2, c=3)  # ✅ b 和 c 被收集到 kwargs
```

**作用**：接收任意数量的关键字参数

### `...` 符号（Ellipsis）

```python
def func(...):
    pass

x: Callable[..., int]  # 接受任意参数，返回 int
```

**作用**：表示"任意参数"

---

## 5. 如何判断参数类型

### 技巧1：看参数名

```python
def func(state, ...):           # state 通常是字典
def func(messages, ...):        # messages 通常是列表
def func(config, ...):          # config 通常是字典
def func(source, ...):          # source 通常是字符串（节点名）
```

### 技巧2：看类型注解

```python
def func(input: dict[str, Any]):  # 明确是字典
    pass

def func(messages: list):         # 明确是列表
    pass
```

### 技巧3：看默认值

```python
def func(x: str = "default"):      # 默认值是字符串
def func(x: Optional[str] = None): # 默认值是 None
```

### 技巧4：看文档字符串

```python
def add_node(
    self,
    node_name: str,
    node: Callable,
):
    """
    Add a node to the graph.

    Args:
        node_name: The name of the node (string)
        node: The function to run (callable)
    """
```

---

## 6. 实战案例

### 案例1：你之前遇到的错误

**错误代码**：
```python
app.invoke(context="3 乘以 5")
```

**如何通过源码发现错误？**

1. 按 F12 查看 `invoke` 源码
2. 看到第一个参数是 `input: InputT | Command | None`
3. 看到 `context` 在 `*` 后面
4. 得出结论：第一个参数应该是 `input`（字典），`context` 是可选关键字参数

**正确代码**：
```python
app.invoke({"messages": [HumanMessage("3 乘以 5")]})
```

---

### 案例2：path_map 参数

**你的疑问**：为什么可以传列表？

**通过源码确认**：

```python
path_map: dict[Hashable, str] | list[str] | None = None
```

类型注解说可以是：
- `dict[Hashable, str]`
- `list[str]`
- `None`

所以三种写法都对：
```python
# 写法1：不传
graph.add_conditional_edges("llm", should_continue)

# 写法2：传列表
graph.add_conditional_edges("llm", should_continue, ["tools", END])

# 写法3：传字典
graph.add_conditional_edges("llm", should_continue, {"tools": "tools"})
```

---

## 7. Python 版本差异

### Union 语法

```python
# Python 3.9
from typing import Union
x: Union[str, int]

# Python 3.10+
x: str | int
```

### 类型注解

```python
# Python 3.9
from typing import List, Dict
x: List[str]
x: Dict[str, int]

# Python 3.9+
x: list[str]
x: dict[str, int]
```

---

## 8. 学习建议

### 优先级

1. **看函数签名**（第一行）- 了解参数
2. **看文档字符串**（`"""..."""`）- 了解用途
3. **看类型注解** - 了解类型
4. **看实现** - 最后才看

### 工具推荐

- **IDE 跳转**（F12）- 最快
- **悬停提示** - 最方便
- `help()` - 最详细
- `inspect` - 最灵活

---

## 9. 练习检查清单

- [ ] 会使用 IDE 跳转查看源码
- [ ] 能读懂函数签名
- [ ] 能解读类型注解
- [ ] 理解 `*` 符号的作用
- [ ] 理解 `|` 符号的含义
- [ ] 能通过源码找到正确的参数类型
- [ ] 理解泛型的概念

---

**下一步**：学习 [05_complete_example.md](./05_complete_example.md) 📖
