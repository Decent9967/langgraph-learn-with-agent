# LangGraph 学习项目

> 从零开始学习 LangGraph 框架，构建智能 Agent 应用
>
> 学习时间: 2025-02-07 开始
> 当前状态: ✅ 第一阶段已完成 (96.7%)

---

## 📖 项目简介

这是一个**AI Agent 辅助学习**的 LangGraph 框架系统化教程项目，采用创新的学习模式帮助你从零掌握 LangGraph。

### 🤖 AI-Agent 辅助学习模式

本项目核心特色是将 AI Agent（Claude Code）深度融入学习全流程，提供：

- 🎯 **智能学习路径规划** - AI 根据学习进度动态调整计划
- 💬 **实时答疑解惑** - 遇到问题随时向 AI 提问，获得详细解释
- ✍️ **代码生成与审查** - AI 辅助编写练习代码，并进行代码审查
- 📝 **自动生成测试题** - AI 按照规范生成 Quiz 文档，验证学习成果
- 🔍 **源码阅读助手** - AI 帮助理解 LangGraph 源码逻辑
- 🛠️ **调试支持** - AI 分析错误、提供修复建议

### 🌐 Web 学习平台

内置精美的 Web 学习平台，提供现代化的学习体验：

**核心功能**：
- 📖 **优雅的讲义阅读** - GitHub 风格的 Markdown 渲染，支持深色/浅色主题
- 📝 **智能测试系统** - 支持选择题和开放题，实时保存答案到本地存储
- 🎨 **主题切换** - 一键切换深色/浅色模式，自动同步到所有页面
- 🗂️ **折叠导航** - 按学习阶段分组，可折叠展开，节省空间
- 📊 **学习进度追踪** - 自动保存答题状态，随时继续学习
- 🔄 **双模式测试** - 支持"一题一页"专注模式和"全部显示"总览模式

**技术亮点**：
- 响应式设计，适配桌面和移动设备
- 无框架纯 JavaScript，轻量快速
- LocalStorage 持久化，刷新不丢失数据
- 平滑动画过渡，提升用户体验

### 📚 三位一体学习法

```
理论 → 实践 → 测试
  ↓       ↓       ↓
讲义    练习    Quiz
  ↓       ↓       ↓
理解    掌握    验证
```

1. **📖 系统化讲义** - 按阶段整理的核心概念文档
2. **💻 动手实践** - 从简单到复杂的渐进式练习
3. **✅ 测试验证** - 多套测试题确保每个知识点都掌握

### 🎯 学习目标

通过本项目的学习，你将能够：
- ✅ 理解 LangGraph 的核心概念（State、Nodes、Edges）
- ✅ 构建工具调用 Agent
- ✅ 实现持久化和检查点机制
- ✅ 掌握流式输出和人机协作
- ✅ 构建 RAG Agent 和多 Agent 系统
- ✅ 部署生产级 Agent 应用

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
├── docs/                      # 📚 讲义文档
│   ├── phase01_basics/        # 第一阶段：基础概念
│   ├── QUIZ_MARKDOWN_SPEC.md  # Quiz 格式规范（AI 生成参考）
│   └── README.md              # 文档说明
│
├── examples/                  # 💻 示例和练习
│   └── phase01_basics/
│       ├── demos/             # 演示代码（10个示例）
│       ├── exercises/         # 练习代码（5个练习）
│       └── quizzes/           # 测试题（6套测试）
│           └── TEMPLATE_QUIZ.md  # Quiz 模板
│
├── web/                       # 🌐 Web 学习平台
│   ├── app.py                 # Flask 应用主程序
│   ├── templates/             # Jinja2 模板
│   │   ├── base.html          # 基础模板
│   │   ├── home.html          # 主页
│   │   ├── lecture.html       # 讲义页面
│   │   └── quiz.html          # 测试页面
│   └── static/                # 静态资源
│       ├── css/               # 样式文件
│       │   ├── base.css           # 基础样式
│       │   ├── theme.css          # 主题变量
│       │   ├── github-markdown.css # GitHub MD 样式
│       │   └── markdown-theme.css  # MD 主题适配
│       └── js/                # JavaScript
│           ├── navigation.js      # 导航功能
│           └── quiz.js            # 测试系统
│
├── config.example.yaml        # LLM 配置模板
├── main.py                    # 项目入口
├── LEARNING_PLAN.md           # 完整学习计划
├── PROGRESS.md                # 学习进度跟踪
├── CLAUDE.md                  # Claude Code 使用指南
└── README.md                  # 项目说明（本文件）
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

5. **启动 Web 学习平台（推荐）**

   这是一个专为 LangGraph 学习设计的 Web 应用，提供沉浸式学习体验：

   ```bash
   cd web
   python app.py
   ```

   访问 http://localhost:5000 开始学习：

   **📖 讲义阅读功能**：
   - 优雅的 GitHub 风格 Markdown 渲染
   - 代码语法高亮
   - 深色/浅色主题无缝切换
   - 响应式布局，支持移动设备

   **📝 测试系统功能**：
   - 选择题：点击选项自动保存，显示正确答案和详细解析
   - 开放题：文本框输入，自动保存到本地存储
   - 双模式切换：
     - `一题一页`：专注模式，逐题作答，支持键盘导航
     - `全部显示`：总览模式，所有题目一览无余
   - 题目导航：快速跳转到任意题目
   - 进度追踪：实时显示答题进度

   **🎨 界面特性**：
   - 主题切换：右上角按钮切换深色/浅色模式
   - 折叠导航：侧边栏和主页支持按阶段折叠展开
   - 状态持久化：答题进度和主题偏好自动保存
   - 平滑动画：所有交互都有流畅的过渡效果

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

## 🤖 AI 辅助学习指南

### 如何利用 AI Agent 提升学习效率

**1. 学习前的准备**
```
向 AI 说：
"我想学习 LangGraph 的 [具体主题]，请帮我制定学习计划"
```

**2. 阅读讲义时**
```
遇到不理解的概念：
"请解释一下 LangGraph 中的 State 是什么？"
"能用简单的例子说明 Nodes 和 Edges 的区别吗？"
```

**3. 做练习时**
```
需要帮助编写代码：
"请帮我创建一个简单的计算器 Agent，支持加减乘除"
"这段代码有错误吗？请帮我分析一下"
```

**4. 阅读源码时**
```
想要深入理解：
"请帮我分析 LangGraph 的 add_node 方法是如何实现的"
"这个 reducer 函数的作用是什么？"
```

**5. 做测试题时**
```
验证学习成果：
"请根据 QUIZ_MARKDOWN_SPEC.md 规范生成一套关于 [主题] 的测试题"
"这题为什么选 B？请详细解释一下"
```

**6. 调试问题时**
```
遇到错误：
"运行这段代码时出现错误：[错误信息]，请问如何修复？"
"Agent 没有按预期调用工具，可能是什么原因？"
```

### AI 辅助学习最佳实践

- ✅ **具体化问题** - 提供完整的上下文和代码片段
- ✅ **渐进式提问** - 从基础概念开始，逐步深入
- ✅ **要求解释** - 不仅要求答案，还要理解原理
- ✅ **验证学习** - 让 AI 出题测试你的理解程度
- ✅ **代码审查** - 写完代码后请 AI review，发现潜在问题
- ❌ **避免直接复制** - 理解 AI 生成的代码，不要盲目复制粘贴

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
