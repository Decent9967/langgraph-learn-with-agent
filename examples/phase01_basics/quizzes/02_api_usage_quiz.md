# API 使用测试题

> 测试时间：2025-02-08
> 结果：满分 5/5 ✅

---

## 📝 测试题目

### 题目 1
**创建一个图，使用 StateGraph，正确的写法是？**

A. `graph = StateGraph()`
B. `graph = StateGraph(MyState)`
C. `graph = StateGraph.create(MyState)`
D. `graph = new StateGraph(MyState)`

**正确答案**: B
**你的答案**: B ✅

---

### 题目 2
**添加一个节点，节点名是 "process"，函数是 my_function，正确的写法是？**

A. `graph.add_node(my_function, "process")`
B. `graph.add("process", my_function)`
C. `graph.add_node("process", my_function)`
D. `graph.node("process", my_function)`

**正确答案**: C
**你的答案**: C ✅

---

### 题目 3
**节点函数应该返回什么？**

A. 完整的 State 字典
B. 只返回需要更新的字段
C. 只能返回一个字段
D. 不需要返回值

**正确答案**: B
**你的答案**: B ✅

---

### 题目 4
**连接节点 A 到节点 B，正确的写法是？**

A. `graph.connect(A, B)`
B. `graph.add_edge("A", "B")`
C. `graph.link("A", "B")`
D. `graph.add_path(A, B)`

**正确答案**: B
**你的答案**: B ✅

---

### 题目 5
**编译并运行图，正确的流程是？**

A. `app = graph.run()` 然后 `app.invoke(state)`
B. `app = graph.compile()` 然后 `app.invoke(state)`
C. `app = graph.start()` 然后 `app.run(state)`
D. `app = graph.create()` 然后 `app.execute(state)`

**正确答案**: B
**你的答案**: B ✅

---

## 📊 测试总结

**总分**: 5/5
**正确率**: 100%

### 掌握情况

| API | 状态 |
|-----|------|
| `StateGraph()` | ✅ 掌握 |
| `add_node()` | ✅ 掌握 |
| `add_edge()` | ✅ 掌握 |
| `compile()` | ✅ 掌握 |
| `invoke()` | ✅ 掌握 |
| 节点返回值 | ✅ 掌握 |

---

## 🎯 需要复习的点

暂无！所有 API 都已掌握 ✅
