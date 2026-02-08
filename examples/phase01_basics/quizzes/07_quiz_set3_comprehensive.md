# 第一阶段：综合测试（第3套）

> 测试时间：2025-02-08
> 重点：综合应用和实战场景

---

## 📝 使用说明

1. **先做题**：在每题的"你的答案"处填写选项（A/B/C/D）
2. **做完再查看答案**：滚动到文档最后，查看正确答案和解析
3. **统计得分**：看看自己得了多少分

---

## 第一部分：场景理解（5题）

### 题目1：用户说"3乘以5等于多少？"，Agent 首先会做什么？

A. 直接回答"15"
B. 调用 multiply 工具
C. 询问用户需要什么运算
D. 返回错误

**你的答案**：___B

---

### 题目2：Agent 调用 multiply(3, 5) 后，ToolNode 会返回什么？

A. AIMessage
B. ToolMessage
C. HumanMessage
D. 字典

**你的答案**：___D

---

### 题目3：ToolNode 执行完后，为什么需要回到 LLM 节点？

A. 调用下一个工具
B. 让 LLM 看到工具结果并生成最终回复
C. 重新执行工具
D. 结束流程

**你的答案**：___B

---

### 题目4：如果 LLM 不需要调用工具，should_continue 函数应该返回什么？

A. "tools"
B. "llm"
C. END
D. "continue"

**你的答案**：___C

---

### 题目5：整个工具调用流程中，messages 字段最后包含多少条消息？

A. 2条（用户输入 + AI回复）
B. 3条（用户输入 + 工具调用 + 工具结果）
C. 4条（用户输入 + 工具调用 + 工具结果 + 最终回复）
D. 5条（包括中间状态）

**你的答案**：___C

---

## 第二部分：代码实现（5题）

### 题目6：定义一个继承自 MessagesState 的状态类，正确的是？

A. `class MyState(MessagesState): messages = []`
B. `class MyState(MessagesState): return messages`
C. `class MyState(MessagesState): pass`
D. `class MyState(MessagesState) -> MessagesState:`

**你的答案**：___C

---

### 题目7：创建 LLM 并绑定工具，正确的代码是？

A. `llm.bind(tools)`
B. `llm.bind_tools(tools)`
C. `llm.tools(tools)`
D. `llm.attach(tools)`

**你的答案**：___B

---

### 题目8：检查消息是否有 tool_calls 并判断，正确的代码是？

A. `if msg.tool_calls: return "tools"`
B. `if hasattr(msg, "tool_calls"): return "tools"`
C. `if hasattr(msg, "tool_calls") and msg.tool_calls: return "tools"`
D. 以上都对

**你的答案**：___C

---

### 题目9：添加从 "tools" 节点回到 "llm" 节点的边，正确的是？

A. `graph.connect("tools", "llm")`
B. `graph.add_edge("tools", "llm")`
C. `graph.link("tools", "llm")`
D. `graph.path("tools", "llm")`

**你的答案**：___B

---

### 题目10：调用图时传入正确的参数是？

A. `app.invoke("用户输入")`
B. `app.invoke({"input": "用户输入"})`
C. `app.invoke({"messages": [HumanMessage("用户输入")]})`
D. `app.invoke("用户输入", config={})`

**你的答案**：___C

---

## 第三部分：配置和类型（5题）

### 题目11：在 YAML 配置中，`base_url` 字段应该配置什么？

A. 文件路径
B. API 地址
C. 端口号
D. 函数名

**你的答案**：___B

---

### 题目12：`dict[str, LLMModelConfig]` 表示什么？

A. 字符串或 LLMModelConfig
B. 键是字符串、值是 LLMModelConfig 的字典
C. LLMModelConfig 或字符串
D. 字典的字符串

**你的答案**：___B

---

### 题目13：`**data` 在 `LLMConfig(**data)` 中的作用是？

A. 创建新字典
B. 解包字典为参数
C. 复制字典
D. 删除字典

**你的答案**：___B

---

### 题目14：`temperature: 0` 在 LLM 配置中表示什么？

A. 随机性最高
B. 随机性最低
C. 中等随机性
D. 没有影响

**你的答案**：___D我还真不知道

---

### 题目15：`model: glm-4-flash` 中的 "glm-4-flash" 是什么？

A. API 地址
B. 模型名称
C. 函数名
D. 工具名

**你的答案**：___B

---

## 第四部分：调试和错误（5题）

### 题目16：如果 `invoke()` 报错 "argument 'input' is positional-only"，说明什么？

A. 第一个参数位置错了
B. 第一个参数用了关键字传递
C. 缺少必需参数
D. 参数类型错误

**你的答案**：___A

---

### 题目17：如果工具没有执行，可能的原因是？

A. LLM 没有选择这个工具
B. 工具定义错误
C. 条件边配置错误
D. 以上都有可能

**你的答案**：___D

---

### 题目18：`hasattr(obj, "attr")` 返回 False 表示什么？

A. 对象没有这个属性
B. 属性值为 None
C. 属性值为 False
D. 对象为 None

**你的答案**：___A

---

### 题目19：如果节点函数返回 `return state` 而不是 `return {"key": value}`，会怎样？

A. 正常工作
B. 会报错
C. 会重复添加消息
D. 会覆盖整个状态

**你的答案**：___D

---

### 题目20：如何查看函数的源码？

A. 按 F3
B. 按 F12
C. 按 Ctrl+C
D. 按 F1

**你的答案**：___B

---

## 📊 正确答案与解析

### 第一部分：场景理解

**题目1：B**
- **解析**：Agent 会先调用 multiply 工具，因为用户明确说了"乘以"

**题目2：B**
- **解析**：ToolNode 返回 ToolMessage，包含工具执行结果

**题目3：B**
- **解析**：工具执行完必须回到 LLM，让 LLM 看到结果并生成最终回复

**题目4：C**
- **解析**：不需要工具时，返回 END 结束流程

**题目5：C**
- **解析**：完整流程包含4条消息：用户输入 → 工具调用 → 工具结果 → 最终回复

### 第二部分：代码实现

**题目6：C**
- **解析**：`class MyState(MessagesState): pass` 正确继承

**题目7：B**
- **解析**：`llm.bind_tools(tools)` 绑定工具

**题目8：C**
- **解析**：需要同时检查属性存在且不为空

**题目9：B**
- **解析**：`graph.add_edge("tools", "llm")` 添加边

**题目10：C**
- **解析**：`invoke()` 接收状态字典，包含 messages 字段

### 第三部分：配置和类型

**题目11：B**
- **解析**：`base_url` 配置 API 地址

**题目12：B**
- **解析**：字典的键是字符串，值是 LLMModelConfig 类型

**题目13：B**
- **解析**：`**data` 解包字典为关键字参数

**题目14：B**
- **解析**：temperature=0 表示随机性最低，输出最确定

**题目15：B**
- **解析**：`glm-4-flash` 是模型名称

### 第四部分：调试和错误

**题目16：A**
- **解析**：positional-only 参数不能用关键字传递

**题目17：D**
- **解析**：多个原因都可能导致工具不执行

**题目18：A**
- **解析**：返回 False 表示对象没有这个属性

**题目19：D**
- **解析**：会覆盖整个状态，导致消息重复添加

**题目20：B**
- **解析**：F12 可以跳转到定义

---

## 📈 成绩统计

### 答案卡（快速对答案）

1. B | 2. B | 3. B | 4. C | 5. C
6. C | 7. B | 8. C | 9. B | 10. C
11. B | 12. B | 13. B | 14. B | 15. B
16. A | 17. D | 18. A | 19. D | 20. B

---

### 评分标准

**得分**：___ /20

**正确率**：___%

**评价**：
- ✅ **18-20分**：优秀！完全掌握第一阶段
- ⚠️ **15-17分**：良好！可以开始进阶学习
- 📝 **12-14分**：及格，建议复习并多练习
- 📚 **0-11分**：需要重新学习

---

## 🎯 学习建议

### 根据得分选择下一步

**18-20分**：
- 可以进入第二阶段
- 尝试构建更复杂的 Agent
- 学习 RAG 和多 Agent 系统

**15-17分**：
- 复习错题对应的知识点
- 重新运行你的计算器 Agent
- 尝试修改代码

**12-14分**：
- 重点复习讲义
- 重新做练习题
- 多运行代码看效果

**0-11分**：
- 系统重新学习第一阶段
- 从基础概念开始
- 完成所有练习题
