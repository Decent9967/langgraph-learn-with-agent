# 第一阶段复习选择题

> 复习时间：2025-02-08
> 目的：快速巩固第一阶段核心知识

---

## 📝 使用说明

1. **先做题**：在每题的"你的答案"处填写选项（A/B/C/D）
2. **做完再查看答案**：滚动到文档最后，查看正确答案和解析
3. **统计得分**：看看自己得了多少分

---

## 第一部分：核心概念（5题）

### 题目1：State 的作用是什么？

A. 存储用户的输入
B. 存储对话历史（用户消息、AI消息、工具结果）
C. 存储工具的定义
D. 存储图的配置信息

**你的答案**：___B

---

### 题目2：在以下哪个类比中，Nodes 被形容为"工人"？

A. Nodes = 传送带
B. Nodes = 包裹
C. Nodes = 工厂里的工人
D. Nodes = 路径

**你的答案**：___B

---

### 题目3：`tool_call_id` 的作用是什么？

A. 标识工具的名称
B. 匹配工具调用和结果
C. 标识用户的会话
D. 标识图的执行顺序

**你的答案**：___B

---

### 题目4：ToolNode 是做什么的？

A. 判断是否需要调用工具
B. 执行工具并返回结果
C. 定义新的工具
D. 连接不同的节点

**你的答案**：___B

---

### 题目5：ToolNode 需要连接边吗？

A. 不需要，自动判断
B. 只需要普通边
C. 只需要条件边
D. 两种边都需要（普通边 + 条件边）

**你的答案**：___D

---

## 第二部分：API 使用（5题）

### 题目6：创建一个图，使用 StateGraph，正确的写法是？

A. `graph = StateGraph()`
B. `graph = StateGraph(MyState)`
C. `graph = StateGraph.create(MyState)`
D. `graph = new StateGraph(MyState)`

**你的答案**：___B

---

### 题目7：添加一个节点，节点名是 "process"，函数是 my_function，正确的写法是？

A. `graph.add_node(my_function, "process")`
B. `graph.add("process", my_function)`
C. `graph.add_node("process", my_function)`
D. `graph.node("process", my_function)`

**你的答案**：___C

---

### 题目8：节点函数应该返回什么？

A. 完整的 State 字典
B. 只返回需要更新的字段
C. 只能返回一个字段
D. 不需要返回值

**你的答案**：___B

---

### 题目9：连接节点 A 到节点 B，正确的写法是？

A. `graph.connect(A, B)`
B. `graph.add_edge("A", "B")`
C. `graph.link("A", "B")`
D. `graph.add_path(A, B)`

**你的答案**：___B

---

### 题目10：编译并运行图，正确的流程是？

A. `app = graph.run()` 然后 `app.invoke(state)`
B. `app = graph.compile()` 然后 `app.invoke(state)`
C. `app = graph.start()` 然后 `app.run(state)`
D. `app = graph.create()` 然后 `app.execute(state)`

**你的答案**：___B

---

## 第三部分：工具和 LLM（5题）

### 题目11：`bind_tools()` 的作用是什么？

A. 创建新的工具
B. 删除工具
C. 告诉 LLM 有哪些工具可用
D. 执行工具

**你的答案**：___C

---

### 题目12：LLM 决定调用工具时，会在哪个消息类型中包含 `tool_calls`？

A. HumanMessage
B. AIMessage
C. ToolMessage
D. SystemMessage

**你的答案**：___B

---

### 题目13：ToolMessage 必须包含哪个字段来匹配工具调用？

A. `tool_name`
B. `tool_args`
C. `tool_call_id`
D. `tool_response`

**你的答案**：___C

---

### 题目14：使用第三方 LLM（如智谱）时，需要设置哪个参数？

A. `provider`
B. `api_url`
C. `base_url`
D. `endpoint`

**你的答案**：___C

---

### 题目15：配置第三方 LLM 时，应该使用哪个类？

A. `ChatAnthropic`
B. `ChatGoogleGenerativeAI`
C. `ChatOpenAI`（因为兼容 OpenAI API）
D. `ChatZhipu`

**你的答案**：___C

---

## 第四部分：类型注解（5题）

### 题目16：`str | int` 在类型注解中是什么意思？

A. 字符串和整数都要有
B. 字符串或整数
C. 字符串转换成整数
D. 整数转换成字符串

**你的答案**：___B

---

### 题目17：函数签名中的 `*` 符号表示什么？

A. 乘法运算
B. 通配符
C. 后面的参数必须用关键字传递
D. 可变参数

**你的答案**：___C

---

### 题目18：`Optional[str]` 等价于哪个类型注解？

A. `str`
B. `str | None`
C. `str | int`
D. `str | bool`

**你的答案**：___B

---

### 题目19：检查对象是否有某个属性，应该用什么函数？

A. `getattr()`
B. `hasattr()`
C. `setattr()`
D. `delattr()`

**你的答案**：___B

---

### 题目20：`list[str]` 表示什么？

A. 字符串列表
B. 列表或字符串
C. 列表的字符串
D. 字符串转换成列表

**你的答案**：___A

---

## 📊 正确答案与解析

### 第一部分：核心概念

**题目1：B**
- **解析**：State 存储对话历史（messages），包含 HumanMessage、AIMessage、ToolMessage

**题目2：C**
- **解析**：Nodes = 工厂里的工人，负责处理数据；Edges = 传送带的路径，决定下一步去哪

**题目3：B**
- **解析**：`tool_call_id` 用于匹配工具调用和结果，确保结果对应正确的调用

**题目4：B**
- **解析**：ToolNode 自动执行工具并返回结果

**题目5：D**
- **解析**：ToolNode 需要两种边：普通边（tools → llm）和条件边（llm → tools）

### 第二部分：API 使用

**题目6：B**
- **解析**：`StateGraph(MyState)` 传入状态类作为参数

**题目7：C**
- **解析**：`graph.add_node("节点名", 函数)` - 节点名在前，函数在后

**题目8：B**
- **解析**：节点函数只返回需要更新的字段，不是整个 State

**题目9：B**
- **解析**：`graph.add_edge("A", "B")` 连接两个节点

**题目10：B**
- **解析**：`graph.compile()` 编译图，`app.invoke()` 运行图

### 第三部分：工具和 LLM

**题目11：C**
- **解析**：`bind_tools()` 告诉 LLM 有哪些工具可用

**题目12：B**
- **解析**：LLM 在 AIMessage 中包含 `tool_calls`

**题目13：C**
- **解析**：ToolMessage 必须包含 `tool_call_id` 来匹配工具调用

**题目14：C**
- **解析**：第三方 LLM 使用 `base_url` 参数指定 API 地址

**题目15：C**
- **解析**：使用 `ChatOpenAI` 配合 `base_url` 可以调用兼容 OpenAI API 的服务

### 第四部分：类型注解

**题目16：B**
- **解析**：`str | int` 表示"字符串或整数"（Python 3.10+ 语法）

**题目17：C**
- **解析**：`*` 符号后面的参数必须用关键字传递

**题目18：B**
- **解析**：`Optional[str]` 等价于 `str | None`

**题目19：B**
- **解析**：`hasattr()` 检查对象是否有某个属性

**题目20：A**
- **解析**：`list[str]` 表示字符串列表

---

## 📈 成绩统计

### 答案卡（快速对答案）

1. B | 2. C | 3. B | 4. B | 5. D
6. B | 7. C | 8. B | 9. B | 10. B
11. C | 12. B | 13. C | 14. C | 15. C
16. B | 17. C | 18. B | 19. B | 20. A

---

### 评分标准

**得分**：___ /20

**正确率**：___%

**评价**：
- ✅ **18-20分**：优秀！第一阶段知识掌握牢固
- ⚠️ **15-17分**：良好！大部分概念已掌握
- 📝 **12-14分**：及格，建议复习错题对应的知识点
- 📚 **0-11分**：需要重新学习第一阶段内容

---

## 🎯 错题复习指南

**做错的题目**：
- 题目__：____________________
- 题目__：____________________
- 题目__：____________________

### 针对性复习

**如果做错题目 1-5**（核心概念）：
→ 复习 [01_core_concepts.md](../../docs/phase01_basics/01_core_concepts.md)

**如果做错题目 6-10**（API 使用）：
→ 复习 [02_api_usage.md](../../docs/phase01_basics/02_api_usage.md)

**如果做错题目 11-15**（工具和 LLM）：
→ 复习 [03_tools_and_llm.md](../../docs/phase01_basics/03_tools_and_llm.md)

**如果做错题目 16-20**（类型注解）：
→ 复习 [04_reading_source_code.md](../../docs/phase01_basics/04_reading_source_code.md)
