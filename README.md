# LangGraph 学习项目

> 从零开始学习 LangGraph 框架，构建智能 Agent 应用
>
> 学习时间: 2025-02-07 开始
> 当前状态: ✅ 第一阶段已完成 (96.7%)

---

## 📖 项目简介

这是一个系统学习 LangGraph 框架的项目，通过：
- 📚 **系统化讲义** - 按阶段整理的学习文档
- 💻 **动手实践** - 从简单到复杂的练习代码
- ✅ **测试验证** - 多套测试题确保掌握程度

帮助你从零开始掌握 LangGraph，最终能够构建复杂的 AI Agent 应用。

---

## 🎯 学习成果

### 第一阶段：基础概念 ✅ 已完成

**学习时间**: 2025-02-07 至 2025-02-08

**测试成绩**: 87/100 (96.7%)

**掌握技能**:
- ✅ State、Nodes、Edges 核心概念
- ✅ LangGraph API 使用
- ✅ 工具调用完整流程
- ✅ LLM 配置（智谱 GLM）
- ✅ YAML + Pydantic 配置管理
- ✅ 源码阅读技巧

详细内容请查看 [学习进度跟踪](PROGRESS.md)

---

## 📁 项目结构

```
langgraph-learn/
├── docs/                   # 📚 讲义文档
│   └── phase01_basics/     # 第一阶段讲义
│
├── examples/               # 💻 示例和练习
│   ├── demos/              # 演示代码
│   ├── exercises/          # 练习代码
│   └── quizzes/            # 测试题
│
├── web/                    # 🌐 Web 学习平台
│   ├── app.py             # Flask 应用
│   ├── templates/         # HTML 模板
│   └── static/            # CSS/JS 静态资源
│
├── config.yaml             # LLM 配置文件
├── main.py                 # 项目入口
├── LEARNING_PLAN.md        # 学习计划
└── PROGRESS.md             # 学习进度跟踪
```

---

## 🚀 快速开始

### 环境要求

- Python 3.10+
- pip 或 uv

### 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd langgraph-learn
   ```

2. **安装依赖**
   ```bash
   # 使用 uv（推荐）
   uv sync

   # 或使用 pip
   pip install -r requirements.txt
   ```

3. **配置 LLM**

   编辑 `config.yaml`，填入你的 API key：
   ```yaml
   llm:
     provider: zhipu  # 或 openai、anthropic、google
     models:
       zhipu:
         model: glm-4-flash
         api_key: your_api_key_here
         base_url: https://open.bigmodel.cn/api/paas/v4/
         temperature: 0
   ```

4. **运行示例**
   ```bash
   python examples/phase01_basics/exercises/05_calculator_agent.py
   ```

5. **启动 Web 学习平台（可选）**
   ```bash
   cd web
   python app.py
   ```

   然后访问 http://localhost:5000 在浏览器中学习：
   - 📖 阅读讲义（美观的网页版）
   - 📝 做测试题（实时保存答案）
   - 🌙 切换深色/浅色主题

---

## 📚 学习路径

### 第一阶段：基础概念 ✅

**内容**:
1. 核心概念（State、Nodes、Edges）
2. API 使用
3. 工具和 LLM
4. 阅读源码技巧
5. 完整示例

**讲义**: [docs/phase01_basics/](docs/phase01_basics/)

**练习**: [examples/phase01_basics/exercises/](examples/phase01_basics/exercises/)

**测试**: [examples/phase01_basics/quizzes/](examples/phase01_basics/quizzes/)

### 第二阶段：核心功能（待学习）

**计划内容**:
- 持久化与检查点（Persistence）
- 流式输出（Streaming）
- 人机协作（Human-in-the-loop）

### 第三阶段：进阶模式（待学习）

**计划内容**:
- RAG Agent
- 多 Agent 系统
- 并行执行与复杂流程控制

详细计划请查看 [学习计划](LEARNING_PLAN.md)

---

## 💡 学习建议

### 学习方法

1. **理论 → 实践 → 测试**
   - 先阅读讲义理解概念
   - 再动手写代码练习
   - 最后用测试验证掌握程度

2. **循序渐进**
   - 按阶段顺序学习
   - 不要跳过基础内容
   - 遇到问题及时查阅讲义

3. **动手实践**
   - 每个概念都亲手写代码
   - 不要只看不练
   - 多做练习巩固知识

### 调试技巧

1. **使用 IDE 快捷键**
   - F12: 跳转到定义
   - Ctrl+点击: 查看引用

2. **阅读源码**
   - 先看函数签名
   - 再看类型注解
   - 最后看实现逻辑

3. **打印调试**
   - print() 打印中间结果
   - 查看消息列表的内容
   - 分析执行流程

---

## 📊 学习进度

| 阶段 | 状态 | 完成时间 | 成绩 |
|------|------|----------|------|
| 第一阶段：基础概念 | ✅ 已完成 | 2025-02-08 | 96.7% |
| 第二阶段：核心功能 | ⏸️ 未开始 | - | - |
| 第三阶段：进阶模式 | ⏸️ 未开始 | - | - |

详细进度请查看 [学习进度跟踪](PROGRESS.md)

---

## 🛠️ 技术栈

- **语言**: Python 3.14.3
- **框架**: LangGraph 1.0.8
- **LLM**: 智谱 GLM-4-flash
- **配置管理**: YAML + Pydantic
- **开发工具**: VSCode + Claude Code

---

## 📝 学习资源

### 官方文档
- [LangGraph Python Docs](https://docs.langchain.com/oss/python/langgraph)
- [LangChain Concepts](https://docs.langchain.com/oss/python/concepts)

### 社区资源
- [LangChain Community GitHub](https://github.com/langchain-ai/langgraph)
- [LangChain Discord](https://discord.gg/langchain)

---

## 🎓 学习成果展示

### 已完成的项目

1. **计算器 Agent**
   - 支持加减乘除运算
   - 使用真实 LLM（智谱 GLM）
   - 完整的工具调用流程
   - 代码: [examples/phase01_basics/exercises/05_calculator_agent.py](examples/phase01_basics/exercises/05_calculator_agent.py)

2. **配置管理系统**
   - YAML 配置文件
   - Pydantic 数据验证
   - 支持多个 LLM 提供商
   - 代码: [examples/phase01_basics/demos/09_create_llm_from_config.py](examples/phase01_basics/demos/09_create_llm_from_config.py)

### 测试成绩

- **基础知识**: 5/5 (100%) ✅
- **API 使用**: 5/5 (100%) ✅
- **复习选择题**: 19/20 (95%) ✅
- **基础知识强化**: 20/20 (100%) ✅
- **API 实践练习**: 19/20 (95%) ✅
- **综合测试**: 18/20 (90%) ✅

---

## 🔧 开发环境

### 推荐工具

- **IDE**: VSCode
- **Python 环境**: uv
- **AI 助手**: Claude Code
- **API 测试**: 智谱 GLM

### 依赖包

```
langgraph>=1.0.0
langchain>=0.3.0
langchain-openai>=0.2.0
pydantic>=2.0.0
pyyaml>=6.0.0
```

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📮 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 GitHub Issue
- 发送邮件

---

**祝你学习愉快！** 🎉

如有任何问题，随时查阅项目文档或提交 Issue。
