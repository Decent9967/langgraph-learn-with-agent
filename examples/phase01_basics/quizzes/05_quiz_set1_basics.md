# 第一阶段：基础概念强化测验（第1套）

> 测试时间：2025-02-08
> 重点：核心概念理解

---

## 📝 使用说明

1. **先做题**：在每题的"你的答案"处填写选项（A/B/C/D）
2. **做完再查看答案**：滚动到文档最后，查看正确答案和解析
3. **统计得分**：看看自己得了多少分

---

## 第一部分：State 与消息（5题）

### 题目1：MessagesState 预定义了哪个字段？

A. `input`
B. `messages`
C. `output`
D. `state`

**你的答案**：___B

---

### 题目2：哪个消息类型可以包含 `tool_calls` 字段？

A. HumanMessage
B. AIMessage
C. ToolMessage
D. SystemMessage

**你的答案**：___B

---

### 题目3：ToolMessage 必须包含什么字段来匹配对应的工具调用？

A. `tool_name`
B. `tool_args`
C. `tool_call_id`
D. `tool_result`

**你的答案**：___C

---

### 题目4：继承 MessagesState 的正确写法是？

A. `class MyState(MessagesState): pass`
B. `class MyState(MessagesState): return messages`
C. `class MyState(MessagesState): def __init__(self): pass`
D. `class MyState extends MessagesState: pass`

**你的答案**：___A

---

### 题目5：MessagesState 中的 `messages` 字段是什么类型？

A. `str`
B. `dict`
C. `list[AnyMessage]`
D. `tuple`

**你的答案**：___C

---

## 第二部分：Nodes 与 Edges（5题）

### 题目6：节点函数应该返回什么？

A. 完整的 State 字典
B. 只返回需要更新的字段
C. 返回字符串
D. 不需要返回值

**你的答案**：___B

---

### 题目7：普通边和条件边的区别是什么？

A. 普通边固定路由，条件边动态选择
B. 普通边动态选择，条件边固定路由
C. 没有区别，名字不同而已
D. 普通边用于节点，条件边用于边

**你的答案**：___A

---

### 题目8：`add_conditional_edges()` 的第二个参数是什么？

A. 源节点名称
B. 目标节点名称
C. 条件函数
D. 边的权重

**你的答案**：___C

---

### 题目9：START 和 END 是什么？

A. 节点名称
B. 特殊常量，表示起点和终点
C. 函数名称
D. 边的类型

**你的答案**：___B

---

### 题目10：如何创建一个从 START 到 "node_a" 的边？

A. `graph.connect(START, "node_a")`
B. `graph.add_edge(START, "node_a")`
C. `graph.link("node_a", START)`
D. `graph.create_edge("node_a", START)`

**你的答案**：___B

---

## 第三部分：工具调用（5题）

### 题目11：`@tool` 装饰器的作用是什么？

A. 创建节点
B. 定义工具
C. 创建边
D. 编译图

**你的答案**：___B

---

### 题目12：ToolNode 的作用是什么？

A. 判断是否需要调用工具
B. 执行工具并返回结果
C. 定义工具
D. 连接节点

**你的答案**：___B

---

### 题目13：`bind_tools()` 的返回值是什么？

A. 一个新的 LLM 实例
B. 工具列表
C. 节点函数
D. 图对象

**你的答案**：___A

---

### 题目14：工具调用的完整流程中，ToolNode 执行完后的下一步是什么？

A. 直接结束
B. 回到 LLM 节点
C. 去条件边
D. 调用下一个工具

**你的答案**：___B

---

### 题目15：为什么需要条件边（should_continue）？

A. 判断 LLM 是否返回了 tool_calls
B. 判断工具执行是否成功
C. 判断用户是否满意
D. 判断是否需要添加新节点

**你的答案**：___A

---

## 第四部分：类型注解（5题）

### 题目16：`dict[str, int]` 表示什么？

A. 字符串或整数
B. 键是字符串、值是整数的字典
C. 字符串和整数的列表
D. 字典或整数

**你的答案**：___B

---

### 题目17：`Optional[str]` 等价于？

A. `str`
B. `str | None`
C. `str | int`
D. `str | bool`

**你的答案**：___B

---

### 题目18：函数签名中的 `*` 符号后面是什么？

A. 必填参数
B. 可选参数
C. 必须用关键字传递的参数
D. 可变参数

**你的答案**：___C

---

### 题目19：`hasattr(obj, "attr")` 的返回值是什么？

A. 属性的值
B. 属性的类型
C. True 或 False
D. 属性的名称

**你的答案**：___C

---

### 题目20：`list[str]` 表示什么？

A. 字符串列表
B. 列表或字符串
C. 字符串转列表
D. 列表的字符串

**你的答案**：___A

---

## 📊 正确答案与解析

### 第一部分：State 与消息

**题目1：B**
- **解析**：MessagesState 预定义了 `messages` 字段，用于存储对话历史

**题目2：B**
- **解析**：只有 AIMessage 可以包含 `tool_calls`，表示 LLM 想要调用工具

**题目3：C**
- **解析**：ToolMessage 必须包含 `tool_call_id` 来匹配对应的工具调用

**题目4：A**
- **解析**：`class MyState(MessagesState): pass` 是正确的继承写法

**题目5：C**
- **解析**：`messages` 是 `list[AnyMessage]` 类型，存储消息列表

### 第二部分：Nodes 与 Edges

**题目6：B**
- **解析**：节点函数只返回需要更新的字段，不是整个 State

**题目7：A**
- **解析**：普通边固定路由（A→B），条件边根据状态动态选择（A→B 或 A→C）

**题目8：C**
- **解析**：第二个参数是条件函数，返回目标节点名称

**题目9：B**
- **解析**：START 和 END 是特殊常量，表示图的起点和终点

**题目10：B**
- **解析**：`graph.add_edge(START, "node_a")` 创建从起点到节点的边

### 第三部分：工具调用

**题目11：B**
- **解析**：`@tool` 装饰器用于定义工具函数

**题目12：B**
- **解析**：ToolNode 自动执行工具并返回结果

**题目13：A**
- **解析**：`bind_tools()` 返回一个新的 LLM 实例，绑定了工具列表

**题目14：B**
- **解析**：工具执行完必须回到 LLM 节点，让 LLM 看到结果并生成最终回复

**题目15：A**
- **解析**：条件函数判断 LLM 是否返回了 tool_calls，决定是否去工具节点

### 第四部分：类型注解

**题目16：B**
- **解析**：`dict[str, int]` 表示键是字符串、值是整数的字典

**题目17：B**
- **解析**：`Optional[str]` 等价于 `str | None`

**题目18：C**
- **解析**：`*` 后面的参数必须用关键字传递

**题目19：C**
- **解析**：`hasattr()` 返回 True 或 False，表示是否有某个属性

**题目20：A**
- **解析**：`list[str]` 表示字符串列表

---

## 📈 成绩统计

### 答案卡（快速对答案）

1. B | 2. B | 3. C | 4. A | 5. C
6. B | 7. A | 8. C | 9. B | 10. B
11. B | 12. B | 13. A | 14. B | 15. A
16. B | 17. B | 18. C | 19. C | 20. A

---

### 评分标准

**得分**：___ /20

**正确率**：___%

**评价**：
- ✅ **18-20分**：优秀！基础概念掌握牢固
- ⚠️ **15-17分**：良好！大部分概念已掌握
- 📝 **12-14分**：及格，建议复习错题对应的知识点
- 📚 **0-11分**：需要重新学习第一阶段内容
