# Quiz Markdown 格式规范

> 本文档定义 Quiz（测试题）Markdown 文件的编写规范。**严格遵守此规范确保测试题能被系统正确解析。**

**解析器**: `web/app.py` 的 `parse_quiz()` 函数
**模板文件**: `examples/phase01_basics/quizzes/TEMPLATE_QUIZ.md`

---

## 核心格式规则

### 1. 题目标题（必须）

使用三级标题 `###`，支持以下格式：

```markdown
### [类型:choice] 题目1：问题文本
### [类型:open] 题目2：问题文本
```

**题型标记**：
- `choice` - 选择题
- `open` - 开放性问题
- 如果不指定，系统会自动检测（有A/B/C/D选项→choice）

**支持变体**：
```markdown
### 题目1：xxx
### 问题1：xxx
### Question 1: xxx
```

### 2. 选择题格式

```markdown
### [类型:choice] 题目1：MessagesState 预定义了哪个字段？

A. `input`
B. `messages`
C. `output`
D. `state`

**正确答案**：B
**解析**：MessagesState 预定义了 messages 字段。
```

**关键规则**：
- ✅ 选项必须是 `A.` `B.` `C.` `D.` 格式（大写字母+点号）
- ✅ 正确答案：`**正确答案**：字母`
- ✅ 解析：`**解析**：内容`
- ❌ 不要使用 `a.` `A)` `A、` 等其他格式
- ❌ 不要在选项中添加 `**你的答案**：___A`

### 3. 开放题格式

```markdown
### [类型:open] 题目2：解释 State 的作用

**你的答案**：
_（写下你的理解）_


**正确答案**：

State 是共享的数据结构，在节点之间传递。

- 作用：存储对话历史
- 传递：各个节点之间
- 更新：节点返回更新的字段

**代码示例**：
```python
class MyState(MessagesState):
    pass
```
```

### 4. 题目分隔（推荐）

题目之间使用分隔线：

```markdown
**解析**：xxx

---

### 下一题...
```

---

## 完整示例

```markdown
# 核心概念测试

> 题型：选择题
> 题量：3 题

---

### [类型:choice] 题目1：MessagesState 预定义了哪个字段？

A. `input`
B. `messages`
C. `output`
D. `state`

**正确答案**：B
**解析**：MessagesState 预定义了 messages 字段。

---

### [类型:choice] 题目2：哪个消息类型包含 tool_calls？

A. HumanMessage
B. AIMessage
C. ToolMessage
D. SystemMessage

**正确答案**：B
**解析**：tool_calls 只在 AIMessage 中存在。

---

### [类型:open] 题目3：State 的作用是什么？

**你的答案**：
_（写下你的理解）_


**正确答案**：

State 在节点之间传递数据，存储应用状态。
```

---

## 解析规则说明

### 题目识别
```regex
###\s*(?:\[类型:(\w+)\])?\s*(?:题目|Question|问题)\s*\d+[:：]?\s*
```

### 选项识别
```regex
^[A-D]\.\s*(.+)
```
只匹配 `A.` `B.` `C.` `D.` 格式

### 答案识别
从包含 `**正确答案**` 或 `正确答案：` 的行中提取字母

### 题型推断
1. 优先使用 `[类型:xxx]` 标记
2. 否则自动检测：有 A/B/C/D 选项 → `choice`

---

## 常见错误

| ❌ 错误 | ✅ 正确 |
|--------|--------|
| `a. xxx` | `A. xxx` |
| `A) xxx` | `A. xxx` |
| `A、xxx` | `A. xxx` |
| `**你的答案**：___A` | `A. xxx` |
| `正确答案：a` | `**正确答案**：A` |

---

## 文件结构

```
# 标题

> 元数据

---

## 题目部分

### 题目1：xxx
内容

---

### 题目2：xxx
内容

---

## 答案汇总（可选）
```

---

## AI 生成提示

当让 AI 生成 Quiz 时，使用以下提示：

```
请严格按照以下格式生成 Quiz：

题目标题：### [类型:choice] 题目N：问题
选项格式：A. xxx B. xxx C. xxx D. xxx
答案格式：**正确答案**：A
解析格式：**解析**：详细说明
题目分隔：---

生成一套关于 [主题] 的测试题，包含 5 道选择题。
```

---

## 验证

创建 Quiz 后，启动服务器验证：

```bash
cd web
python app.py
# 访问 http://localhost:5000
```

检查：
- [ ] 题目数量正确
- [ ] 选项显示完整
- [ ] 答案正确
- [ ] 解析显示正常

---

**版本**: v1.0
**最后更新**: 2025-02-08
